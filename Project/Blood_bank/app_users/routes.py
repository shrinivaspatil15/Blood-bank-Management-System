from flask import render_template, url_for, flash, redirect, request, Blueprint, current_app
from flask_login import login_user, current_user, logout_user, login_required
import phonenumbers
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from Blood_bank import db, bcrypt
from Blood_bank.models import App_user, Bloodbank, Request
from Blood_bank.app_users.forms import (EmailRegistrationForm, RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm, RequestBloodForm)
from Blood_bank.app_users.utils import save_picture, send_reset_email, send_registration_email, send_request
from datetime import datetime, date
import pytz
from geoalchemy2.functions import ST_Distance, ST_SetSRID, ST_Point

users = Blueprint('users', __name__)

@users.route("/register", methods=['GET', 'POST'])
def register_email():
	form = EmailRegistrationForm()
	if form.validate_on_submit():
		send_registration_email(form.email.data)
		flash('Email has been sent with instructions to register', 'info')
		return redirect(url_for('users.login'))
	return render_template("register_email.html", title='Register', form=form)

@users.route("/register/<token>", methods=['GET', 'POST'])
def register(token):
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = RegistrationForm()
	if form.validate_on_submit():
		s = Serializer(current_app.config['SECRET_KEY'])
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		contact_no = phonenumbers.parse(form.contact_no.data, "IN")
		contact_no = phonenumbers.format_number(contact_no, phonenumbers.PhoneNumberFormat.E164)
		user = App_user(name=form.name.data, email=s.loads(token)['email_id'], password=hashed_password, contact_no=contact_no)
		db.session.add(user)
		db.session.commit()
		flash(f'Account created for {form.name.data}!', 'success')
		return redirect(url_for('users.login'))
	return render_template('register.html', title="Register", form=form)

@users.route("/login", methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = App_user.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('main.home'))
		else:
			flash('Login failed! Please check email and password', 'danger')
	return render_template('login.html', title="Login", form=form)


@users.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('main.home'))

@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
	form = UpdateAccountForm()
	if form.validate_on_submit():
		if form.picture.data:
			picture_file = save_picture(form.picture.data)
			current_user.image_file = picture_file
		current_user.name = form.name.data
		current_user.email = form.email.data
		contact_no = phonenumbers.parse(form.contact_no.data, "IN")
		contact_no = phonenumbers.format_number(contact_no, phonenumbers.PhoneNumberFormat.E164)
		current_user.contact_no = contact_no
		db.session.commit()
		flash('Your account has been updated', 'success')
		return redirect(url_for('users.account'))
	elif request.method == 'GET':
		form.name.data = current_user.name
		form.email.data = current_user.email
		form.contact_no.data = current_user.contact_no
	image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
	return render_template('account.html', title="Account", image_file=image_file, form=form)	

# @users.route("/user/<string:username>")
# def user_posts(username):
# 	page = request.args.get('page', 1, type=int)
# 	user = User.query.filter_by(username=username).first_or_404()
# 	posts = Post.query.filter_by(author=user)\
# 		.order_by(Post.date_posted.desc())\
# 		.paginate(page=page, per_page=5)
# 	return render_template("user_posts.html", posts=posts, user=user)


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
	if current_user.is_authenticated:
		send_reset_email(current_user)
		flash('Email has been sent with instructions to reset your password', 'info')
		return redirect(url_for('users.login'))
		# return redirect(url_for('main.home'))
	form = RequestResetForm()
	if form.validate_on_submit():
		user = App_user.query.filter_by(email=form.email.data).first()
		send_reset_email(user)
		flash('Email has been sent with instructions to reset your password', 'info')
		return redirect(url_for('users.login'))
	return render_template("reset_request.html", title='Reset Password', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	user = App_user.verify_reset_token(token)
	if user is None:
		flash('That is an invalid or expired token', 'warning')
		return redirect(url_for('users.reset_request'))
	form = ResetPasswordForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user.password = hashed_password
		db.session.commit()
		flash(f'Your password has been updated successfully!', 'success')
		return redirect(url_for('users.login'))
	return render_template("reset_token.html", title='Reset Password', form=form)

@users.route("/request_blood", methods=['GET', 'POST'])
@login_required
def request_blood():
	form = RequestBloodForm()
	if form.validate_on_submit():
		req = Request(user_id=current_user.id,\
						  date=datetime.now(pytz.timezone('Asia/Kolkata')),\
						  blood_group=form.blood_group.data,\
						  units=form.units.data)
		# bloodbank.stats.edit(str(form.blood_group.data), int(form.units.data)*(-1))
		db.session.add(req)
		db.session.commit()
		latitude = request.args.get('latitude', 0, type=float)
		longitude = request.args.get('longitude', 0, type=float)
		blood_banks = Bloodbank.query\
						.order_by(ST_Distance(Bloodbank.geom, ST_SetSRID(ST_Point(longitude, latitude), 4326)).asc())\
						.limit(5)
		email_list = list()
		for bloodbank in blood_banks:
			email_list.append(str(bloodbank.email))
		send_request(email_list, form.blood_group.data, form.units.data, current_user)
		msg = 'Request Sent!'
		flash(msg, 'success')
		return redirect(url_for('main.home'))
	return render_template("request_blood.html", title='Request Blood', form=form)
