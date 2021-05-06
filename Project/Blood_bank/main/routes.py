import io
from flask import Blueprint, Response, render_template, abort
from flask_login import login_required, current_user
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
# from Blood_bank import db
from Blood_bank.main.utils import create_bar#, create_line
from Blood_bank.models import Donation, Donor, Utilisation
from sqlalchemy import func

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
	return render_template('home.html', title='Blood Buddy')


# @main.route("/total-units-donated.png")
# @login_required
# def total_donation_line_plot():
# 	if current_user.role!='app_admin':
# 		abort(403)
# 	# donation = Donation.query.all()
# 	donation = db.session.query(Donation.date, func.sum(Donation.units)).group_by(Donation.date)
# 	dates = list()
# 	units = list()
# 	for row in donation:
# 		dates.append(row.date)
# 		units.append(row[1])
# 	fig = create_line(dates, units, 'Total Donations', 'Time', 'Units')
# 	output = io.BytesIO()
# 	FigureCanvas(fig).print_png(output)
# 	return Response(output.getvalue(), mimetype='image/png')



@main.route("/donations.png")
@login_required
def total_donation_bar_plot():
	if current_user.role!='app_admin':
		abort(403)
	received = {'A+':0, 'A-':0,\
				'B+':0, 'B-':0,\
				'AB+':0, 'AB-':0,\
				'O+':0, 'O-':0}
	donation = Donation.query.all()
	for row in donation:
		donor = Donor.query.get(row.donor_id)
		bg = str(donor.blood_group)
		received[bg] = received[bg] + int(row.units)
	fig = create_bar(list(received.keys()), list(received.values()), 'Total Donations', 'Blood Group', 'Units')
	output = io.BytesIO()
	FigureCanvas(fig).print_png(output)
	return Response(output.getvalue(), mimetype='image/png')

@main.route("/utilisation.png")
@login_required
def total_utilisation_bar_plot():
	if current_user.role!='app_admin':
		abort(403)
	utilised = {'A+':0, 'A-':0,\
				'B+':0, 'B-':0,\
				'AB+':0, 'AB-':0,\
				'O+':0, 'O-':0}
	# utilisation = Utilisation.query.filter(cast(Utilisation.date_time, Date)==date.today()).filter_by(bloodbank_id=bloodbank_id).all()
	utilisation = Utilisation.query.all()
	for row in utilisation:
		bg = str(row.blood_group)
		utilised[bg] = utilised[bg] + int(row.units)
	fig = create_bar(list(utilised.keys()), list(utilised.values()), "Total Utilisation", 'Blood Group', 'Units')
	output = io.BytesIO()
	FigureCanvas(fig).print_png(output)
	return Response(output.getvalue(), mimetype='image/png')
