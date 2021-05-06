from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
import phonenumbers
from flask_login import current_user
from Blood_bank.models import App_user


class EmailRegistrationForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	submit = SubmitField('Register')

	def validate_email(self, email):
		user = App_user.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('Account already exists with that Email-ID. Please choose a different email!')


class RegistrationForm(FlaskForm):
	name = StringField('Name', validators=[DataRequired(), Length(min=2, max=30)])
	contact_no = StringField('Contact No', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
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
		# user = App_user.query.filter_by(contact_no=contact_no.data).first()
		if user:
			raise ValidationError('Account already exists with that contact number. Please try another number!')

	def validate_email(self, email):
		user = App_user.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('Account already exists with that Email-ID. Please choose a different email!')

class LoginForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
	name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	contact_no = StringField('Contact No', validators=[DataRequired()])
	picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
	submit = SubmitField('Update')

	# def validate_username(self, username):
	# 	if name.data != current_user.username:
	# 		user = User.query.filter_by(username=username.data).first()
	# 		if user:
	# 			raise ValidationError('That username is already taken. Please choose a different username!')

	def validate_contact_no(self,contact_no):
		if len(contact_no.data) > 13:
			raise ValidationError('Invalid phone number.')
		input_number = phonenumbers.parse(contact_no.data, "IN")
		if not (phonenumbers.is_valid_number(input_number)):
			raise ValidationError('Invalid phone number.')
		db_contact_no = phonenumbers.parse(contact_no.data, "IN")
		db_contact_no = phonenumbers.format_number(db_contact_no, phonenumbers.PhoneNumberFormat.E164)
		user = App_user.query.filter_by(contact_no=db_contact_no).first()
		# user = App_user.query.filter_by(contact_no=contact_no.data).first()
		if user:
			raise ValidationError('Account already exists with that contact number. Please try another number!')

	def validate_email(self, email):
		if email.data != current_user.email:
			user = App_user.query.filter_by(email=email.data).first()
			if user:
				raise ValidationError('That email is already taken. Please choose a different email!')


class RequestResetForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	submit = SubmitField('Request Password Reset')

	def validate_email(self, email):
		user = App_user.query.filter_by(email=email.data).first()
		if user is None:
			raise ValidationError('There is no accout with this email. You must Register first')

class ResetPasswordForm(FlaskForm):
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Reset Password')

class RequestBloodForm(FlaskForm):
	bg = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
	blood_group = SelectField(u'Blood Group', choices=bg, validators=[DataRequired()])
	units = IntegerField('Number of Units', validators=[DataRequired()])
	submit = SubmitField('Submit')