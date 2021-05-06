from flask import Blueprint, abort, render_template, flash, redirect, url_for, current_app, request
from flask_login import login_user, current_user, logout_user, login_required
from Blood_bank.bloodbank_admin.forms import AdminRegistrationForm, UpdateAvailabilityForm, ReceivedBloodForm, UtilisedBloodForm
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from Blood_bank import db, bcrypt
from Blood_bank.models import App_user, Bloodbank, Bloodbank_stats, Donor, Donation, Utilisation
import phonenumbers
from datetime import datetime, date
import pytz

bloodbank_admin = Blueprint('bloodbank_admin', __name__)

@bloodbank_admin.route("/register_bloodbank/<token>", methods=['GET', 'POST'])
def register_admin(token):
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = AdminRegistrationForm()
	if form.validate_on_submit():
		s = Serializer(current_app.config['SECRET_KEY'])
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		contact_no = phonenumbers.parse(s.loads(token)['contact_no'], "IN")
		contact_no = phonenumbers.format_number(contact_no, phonenumbers.PhoneNumberFormat.E164)
		user = App_user(name=s.loads(token)['name'],\
						email=s.loads(token)['email_id'],\
						password=hashed_password,\
						contact_no=contact_no,\
						role=s.loads(token)['role'],\
						bloodbank_id=s.loads(token)['bloodbank_id'])
		stats = Bloodbank_stats(bloodbank_id=s.loads(token)['bloodbank_id'],\
								a_positive=0,\
								a_negative=0,\
								b_positive=0,\
								b_negative=0,\
								ab_positive=0,\
								ab_negative=0,\
								o_positive=0,\
								o_negative=0,)
								# date=datetime.now(pytz.timezone('Asia/Kolkata')))
		db.session.add(stats)
		db.session.add(user)
		db.session.commit()
		msg = 'Account created for ' + s.loads(token)['name'] + '!'
		flash(msg, 'success')
		return redirect(url_for('users.login'))
	return render_template('register_admin.html', title="Register Admin", form=form)

@bloodbank_admin.route("/update-availability", methods=['GET', 'POST'])
@login_required
def blood_availability():
	if current_user.role!='bloodbank_admin':
		abort(403)
	form = UpdateAvailabilityForm()
	bloodbank = Bloodbank.query.get(current_user.bloodbank_id)
	if form.validate_on_submit():
		bloodbank.stats.a_positive = form.a_positive.data
		bloodbank.stats.a_negative = form.a_negative.data
		bloodbank.stats.b_positive = form.b_positive.data
		bloodbank.stats.b_negative = form.b_negative.data
		bloodbank.stats.ab_positive = form.ab_positive.data
		bloodbank.stats.ab_negative = form.ab_negative.data
		bloodbank.stats.o_positive = form.o_positive.data
		bloodbank.stats.o_negative = form.o_negative.data
		db.session.commit()
		msg = 'Blood Availability has been updated successfully!'
		flash(msg, 'success')
		return redirect(url_for('bloodbanks.bloodbank', bloodbank_id=bloodbank.id))
	elif request.method=='GET':
		# stats = Bloodbank_stats.query.filter_by(bloodbank_id=bloodbank.id).order_by(Bloodbank_stats.date.desc()).first()
		stats = Bloodbank_stats.query.get(bloodbank.id)
		if stats:
			form.a_positive.data = stats.a_positive
			form.a_negative.data = stats.a_negative
			form.b_positive.data = stats.b_positive
			form.b_negative.data = stats.b_negative
			form.ab_positive.data = stats.ab_positive
			form.ab_negative.data = stats.ab_negative
			form.o_positive.data = stats.o_positive
			form.o_negative.data = stats.o_negative
	return render_template('update_availability.html', title="Blood Availability", form=form)


@bloodbank_admin.route("/update-received-blood", methods=['GET', 'POST'])
@login_required
def received_blood():
	if current_user.role!='bloodbank_admin':
		abort(403)
	form = ReceivedBloodForm()
	bloodbank = Bloodbank.query.get(current_user.bloodbank_id)
	if form.validate_on_submit():
		donor = Donor.query.filter_by(email=form.email.data).first()
		if donor is None:
			donor = Donor(name=form.name.data,\
						  email=form.email.data,\
						  contact_no=form.contact_no.data,\
						  blood_group=form.blood_group.data,\
						  last_donation=date.today())
			db.session.add(donor)
			db.session.commit()
		donation = Donation(donor_id=donor.id,\
							bloodbank_id=bloodbank.id,\
							date=date.today(),\
							units=form.units.data)
		bloodbank.stats.edit(str(form.blood_group.data), int(form.units.data))
		db.session.add(donation)
		db.session.commit()
		msg = 'Donation Added!'
		return redirect(url_for('bloodbanks.bloodbank', bloodbank_id=bloodbank.id))
	return render_template('received_blood.html', title="Received Blood", form=form)

@bloodbank_admin.route("/update-utilised-blood", methods=['GET', 'POST'])
@login_required
def utilised_blood():
	if current_user.role!='bloodbank_admin':
		abort(403)
	form = UtilisedBloodForm()
	bloodbank = Bloodbank.query.get(current_user.bloodbank_id)
	if form.validate_on_submit():
		# donor = Donor.query.filter_by(email=form.email.data).first()
		# if donor is None:
		# 	donor = Donor(name=form.name.data,\
		# 				  email=form.email.data,\
		# 				  contact_no=form.contact_no.data,\
		# 				  blood_group=form.blood_group.data,\
		# 				  last_donation=date.today())
		# 	db.session.add(donor)
		# 	db.session.commit()
		utilisation = Utilisation(bloodbank_id=bloodbank.id,\
								  date_time=datetime.now(pytz.timezone('Asia/Kolkata')),\
								  blood_group=form.blood_group.data,\
								  units=form.units.data
								  )
		bloodbank.stats.edit(str(form.blood_group.data), int(form.units.data)*(-1))
		db.session.add(utilisation)
		db.session.commit()
		msg = 'Utilisation Added!'
		return redirect(url_for('bloodbanks.bloodbank', bloodbank_id=bloodbank.id))
	return render_template('utilised_blood.html', title="Received Blood", form=form)
