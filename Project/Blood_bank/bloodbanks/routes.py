import io
from flask import Blueprint, render_template, request, Response, abort
from flask_login import login_required, current_user
from Blood_bank.models import Bloodbank, Bloodbank_stats, Donation, Donor, Utilisation
from Blood_bank.main.utils import create_bar, create_pie
from geoalchemy2.functions import ST_Distance, ST_SetSRID, ST_Point
from sqlalchemy import Date, cast, func
from datetime import date, datetime, timedelta
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib import pyplot as pyplot

bloodbanks = Blueprint('bloodbanks', __name__)

@bloodbanks.route("/bloodbanks_nearby")
def bloodbanks_nearby():
	page = request.args.get('page', 1, type=int)
	latitude = request.args.get('latitude', 0, type=float)
	longitude = request.args.get('longitude', 0, type=float)
	blood_banks = Bloodbank.query\
					.order_by(ST_Distance(Bloodbank.geom, ST_SetSRID(ST_Point(longitude, latitude), 4326)).asc())\
					.limit(15).from_self()\
					.paginate(page=page, per_page=5)
	return render_template("bloodbanks_nearby.html", blood_banks=blood_banks, longitude=longitude, latitude=latitude)

@bloodbanks.route("/bloodbank/<int:bloodbank_id>")
def bloodbank(bloodbank_id):
	blood_bank = Bloodbank.query.get_or_404(bloodbank_id)
	yesterday = date.today() - timedelta(days=1)
	# stats = Bloodbank_stats.query.filter_by(bloodbank_id=bloodbank_id).order_by(Bloodbank_stats.date.desc()).first()
	stats = Bloodbank_stats.query.get(blood_bank.id)
	return render_template("bloodbank.html", blood_bank=blood_bank, stats=stats, date=str(yesterday))

@bloodbanks.route("/bloodbank/<int:bloodbank_id>/available_blood.png")
def available_blood(bloodbank_id):
	blood_bank = Bloodbank.query.get_or_404(bloodbank_id)
	stats = Bloodbank_stats.query.get(blood_bank.id)
	unit = [int(stats.a_positive), int(stats.a_negative), int(stats.b_positive), int(stats.b_negative), 
			int(stats.ab_positive), int(stats.ab_negative), int(stats.o_positive), int(stats.o_negative)]
	bg = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
	fig = create_pie(unit, bg)
	output = io.BytesIO()
	FigureCanvas(fig).print_png(output)
	return Response(output.getvalue(), mimetype='image/png')

@bloodbanks.route("/bloodbank/<int:bloodbank_id>/received_blood.png")
@login_required
def received_blood(bloodbank_id):
	blood_bank = Bloodbank.query.get_or_404(bloodbank_id)
	if current_user.role!='app_admin':
		if current_user.id!=blood_bank.admin.id:
			abort(403)
	received = {'A+':0, 'A-':0,\
				'B+':0, 'B-':0,\
				'AB+':0, 'AB-':0,\
				'O+':0, 'O-':0}
	donation = Donation.query.filter_by(date=func.current_date()).filter_by(bloodbank_id=bloodbank_id).all()
	for row in donation:
		donor = Donor.query.get(row.donor_id)
		bg = str(donor.blood_group)
		received[bg] = received[bg] + int(row.units)
	fig = create_bar(list(received.keys()), list(received.values()), "Today's Donations", 'Blood Group', 'Units')
	output = io.BytesIO()
	FigureCanvas(fig).print_png(output)
	return Response(output.getvalue(), mimetype='image/png')


@bloodbanks.route("/bloodbank/<int:bloodbank_id>/utilised_blood.png")
@login_required
def utilised_blood(bloodbank_id):
	blood_bank = Bloodbank.query.get_or_404(bloodbank_id)
	if current_user.role!='app_admin':
		if current_user.id!=blood_bank.admin.id:
			abort(403)
	utilised = {'A+':0, 'A-':0,\
				'B+':0, 'B-':0,\
				'AB+':0, 'AB-':0,\
				'O+':0, 'O-':0}
	utilisation = Utilisation.query.filter(cast(Utilisation.date_time, Date)==date.today()).filter_by(bloodbank_id=bloodbank_id).all()
	for row in utilisation:
		bg = str(row.blood_group)
		utilised[bg] = utilised[bg] + int(row.units)
	fig = create_bar(list(utilised.keys()), list(utilised.values()), "Today's Utilisation", 'Blood Group', 'Units')
	output = io.BytesIO()
	FigureCanvas(fig).print_png(output)
	return Response(output.getvalue(), mimetype='image/png')
