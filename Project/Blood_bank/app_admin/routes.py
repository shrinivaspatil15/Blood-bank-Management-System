from flask import Blueprint, abort, render_template, flash, redirect, url_for
from flask_login import login_user, current_user, logout_user, login_required
from Blood_bank.app_admin.forms import BloodbankRegistrationForm
from Blood_bank.app_admin.utils import send_bloodbank_registration_email
from Blood_bank import db
from Blood_bank.models import Bloodbank
import requests
import phonenumbers

app_admin = Blueprint('app_admin', __name__)

@app_admin.route("/register_bloodbank", methods=['GET', 'POST'])
@login_required
def register_bloodbank():
	if current_user.role != 'app_admin':
		abort(403)
	form = BloodbankRegistrationForm()
	if form.validate_on_submit():
		contact_no = phonenumbers.parse(form.contact_no.data, "IN")
		contact_no = phonenumbers.format_number(contact_no, phonenumbers.PhoneNumberFormat.E164)
		loc_det = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address='\
							 + form.address.data\
							 + '&key=AIzaSyDEVlxGElqrqiRf74X3Ii-E2eF2S-TJVPY').json()
		lat = float(loc_det['results'][0]['geometry']['location']['lat'])
		lng = float(loc_det['results'][0]['geometry']['location']['lng'])
		bloodbank = Bloodbank(name=form.name.data,\
							  address=form.address.data,\
							  contact_no=contact_no,\
							  email=form.email.data,\
							  latitude=lat,\
							  longitude=lng,\
							  geom='SRID=4326; POINT(' + str(lng) + ' ' + str(lat) + ')')
		db.session.add(bloodbank)
		db.session.commit()
		send_bloodbank_registration_email(form.admin_name.data,\
											form.admin_email.data,\
											form.admin_contact_no.data,\
											"bloodbank_admin",\
											bloodbank.id)
		flash('Email has been sent with instructions to register', 'info')
		return redirect(url_for('main.home'))
	return render_template("register_bloodbank.html", title='Register Bloodbank', form=form)