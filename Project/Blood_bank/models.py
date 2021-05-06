from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from Blood_bank import db, login_manager
from flask_login import UserMixin
from geoalchemy2.types import Geometry
from sqlalchemy import func
from datetime import datetime
import pytz

@login_manager.user_loader
def load_user(user_id):
	return App_user.query.get(int(user_id))

class Bloodbank(db.Model):
	__tablename__ = "bloodbank"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(150), nullable=False)
	address = db.Column(db.String(1000), nullable=False)
	contact_no = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), nullable=False)
	latitude = db.Column(db.Float(20), nullable=False)
	longitude = db.Column(db.Float(20), nullable=False)
	geom = db.Column(Geometry('Point'), nullable=False)
	admin = db.relationship("App_user",	uselist=False, backref='bloodbank')
	donors = db.relationship("Donation", back_populates="bloodbanks")
	stats = db.relationship("Bloodbank_stats", uselist=False, backref="bloodbank")
	utilised_blood = db.relationship("Utilisation", backref="bloodbank", lazy=True)

class App_user(db.Model, UserMixin):
	__tablename__ = "app_user"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(30), nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
	password = db.Column(db.String(60), nullable=False)
	contact_no = db.Column(db.String(15), unique=True, nullable=False)
	role = db.Column(db.String(15), nullable=False, default='app_user')
	bloodbank_id = db.Column(db.Integer, db.ForeignKey(Bloodbank.id))
	requests = db.relationship("Request", backref="user", lazy=True)

	def get_reset_token(self, expires_sec=1800):
		s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
		return s.dumps({'user_id': self.id}).decode('utf-8')

	@staticmethod
	def verify_reset_token(token):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			user_id = s.loads(token)['user_id']
		except:
			return None
		return App_user.query.get(user_id)

	def __repr__(self):
		return f"User('{self.name}', '{self.email}', '{self.image_file}', '{self.contact_no}')"


class Request(db.Model):
	__tablename__ = "request"
	user_id = db.Column(db.Integer, db.ForeignKey(App_user.id), primary_key=True)
	date = db.Column(db.DateTime, nullable=False, default=datetime.now(pytz.timezone('Asia/Kolkata')), primary_key=True)
	blood_group = db.Column(db.String(5), nullable=False)
	units = db.Column(db.Integer, nullable=False, default=1)


class Donor(db.Model):
	__tablename__ = "donor"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(30), nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	contact_no = db.Column(db.String(15), unique=True, nullable=False)
	# address = db.Column(db.String(1000), nullable=False)
	blood_group = db.Column(db.String(5), nullable=False)
	last_donation = db.Column(db.Date, nullable=False, default=func.current_date())
	bloodbanks = db.relationship("Donation", back_populates="donors")


class Donation(db.Model):
	__tablename__ = "donation"
	donor_id = db.Column(db.Integer, db.ForeignKey(Donor.id), primary_key=True)
	bloodbank_id = db.Column(db.Integer, db.ForeignKey(Bloodbank.id), primary_key=True)
	date = db.Column(db.Date, nullable=False, default=func.current_date(), primary_key=True)
	units = db.Column(db.Integer, nullable=False, default=1)
	bloodbanks = db.relationship("Bloodbank", back_populates="donors")
	donors = db.relationship("Donor", back_populates="bloodbanks")


class Utilisation(db.Model):
	__tablename__ = "utilisation"
	bloodbank_id = db.Column(db.Integer, db.ForeignKey(Bloodbank.id), primary_key=True)
	date_time = db.Column(db.DateTime, nullable=False, default=datetime.now(pytz.timezone('Asia/Kolkata')), primary_key=True)
	blood_group = db.Column(db.String(5), nullable=False)
	units = db.Column(db.Integer, nullable=False, default=1)


class Bloodbank_stats(db.Model):
	__tablename__ = "bloodbank_stats"
	bloodbank_id = db.Column(db.Integer, db.ForeignKey(Bloodbank.id), primary_key=True)
	a_positive = db.Column(db.Integer, nullable=False)
	a_negative = db.Column(db.Integer, nullable=False)
	b_positive = db.Column(db.Integer, nullable=False)
	b_negative = db.Column(db.Integer, nullable=False)
	ab_positive = db.Column(db.Integer, nullable=False)
	ab_negative = db.Column(db.Integer, nullable=False)
	o_positive = db.Column(db.Integer, nullable=False)
	o_negative = db.Column(db.Integer, nullable=False)
	# date = db.Column(db.DateTime, nullable=False, default=datetime.now(pytz.timezone('Asia/Kolkata')), primary_key=True)

	def edit(self, bg, units):
		bg_name = { 
					'A+':'a_positive',
					'A-':'a_negative',
					'B+':'b_positive',
					'B-':'b_negative',
					'AB+':'ab_positive',
					'AB-':'ab_negative',
					'O+':'o_positive',
					'O-':'o_negative'
				   }
		method = getattr(self, "edit_" + str(bg_name[str(bg)]), lambda:"Invalid Blood Group")
		return method(units)

	def edit_a_positive(self, units):
		self.a_positive = self.a_positive + int(units)

	def edit_a_negative(self, units):
		self.a_negative = self.a_negative + int(units)

	def edit_b_positive(self, units):
		self.b_positive = self.b_positive + int(units)

	def edit_b_negative(self, units):
		self.b_negative = self.b_negative + int(units)
	
	def edit_ab_positive(self, units):
		self.ab_positive = self.ab_positive + int(units)

	def edit_ab_negative(self, units):
		self.ab_negative = self.ab_negative + int(units)
	
	def edit_o_positive(self, units):
		self.o_positive = self.o_positive + int(units)

	def edit_o_negative(self, units):
		self.o_negative = self.o_negative + int(units)
		

	# blood_bank = db.relationship("Bloodbank", backref=backref("stats", uselist=False))