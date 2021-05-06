from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
import phonenumbers
from Blood_bank.models import App_user

class BloodbankRegistrationForm(FlaskForm):
	name = StringField('Name', validators=[DataRequired(), Length(min=2, max=150)])
	address = StringField('Address', validators=[DataRequired(), Length(min=2, max=1000)])
	contact_no = StringField('Contact No', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(), Email()])
	admin_name = StringField('Admin Name', validators=[DataRequired(), Length(min=2, max=30)])
	admin_email = StringField('Admin Email', validators=[DataRequired(), Email()])
	admin_contact_no = StringField('Admin Contact No', validators=[DataRequired()])
	submit = SubmitField('Sign Up')

	# def validate_username(self, username):
	# 	user = User.query.filter_by(username=username.data).first()
	# 	if user:
	# 		raise ValidationError('That username is already taken. Please choose a different username!')

	def validate_contact_no(self,contact_no):
		if len(contact_no.data) > 13:
			raise ValidationError('Invalid phone number.')
		input_number = phonenumbers.parse(contact_no.data, "IN")
		if not (phonenumbers.is_valid_number(input_number)):
			raise ValidationError('Invalid phone number.')
		db_contact_no = phonenumbers.parse(contact_no.data, "IN")
		db_contact_no = phonenumbers.format_number(db_contact_no, phonenumbers.PhoneNumberFormat.E164)
		user = App_user.query.filter_by(contact_no=db_contact_no).first()
		if user:
			raise ValidationError('Account already exists with that contact number. Please try another number!')

	def validate_admin_email(self, admin_email):
		user = App_user.query.filter_by(email=admin_email.data).first()
		if user:
			raise ValidationError('Account already exists with that Email-ID. Please choose a different email!')
