from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, IntegerField, StringField, SelectField
from wtforms.validators import DataRequired, EqualTo, NumberRange, Email, AnyOf

class AdminRegistrationForm(FlaskForm):
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Sign Up')

class UpdateAvailabilityForm(FlaskForm):
	a_positive = IntegerField('A+', validators=[DataRequired(), NumberRange(min=0)])
	a_negative = IntegerField('A-', validators=[DataRequired(), NumberRange(min=0)])
	b_positive = IntegerField('B+', validators=[DataRequired(), NumberRange(min=0)])
	b_negative = IntegerField('B-', validators=[DataRequired(), NumberRange(min=0)])
	ab_positive = IntegerField('AB+', validators=[DataRequired(), NumberRange(min=0)])
	ab_negative = IntegerField('AB-', validators=[DataRequired(), NumberRange(min=0)])
	o_positive = IntegerField('O+', validators=[DataRequired(), NumberRange(min=0)])
	o_negative = IntegerField('O-', validators=[DataRequired(), NumberRange(min=0)])
	submit = SubmitField('Update')

class ReceivedBloodForm(FlaskForm):
	name = StringField('Donor Name', validators=[DataRequired()])
	email = StringField('Donor Email-ID', validators=[DataRequired(), Email()])
	contact_no = StringField('Donor Contact No.', validators=[DataRequired()])
	bg = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
	blood_group = SelectField(u'Blood Group', choices=bg, validators=[DataRequired()])
	units = IntegerField('Number of Units', validators=[DataRequired()])
	submit = SubmitField('Submit')

class UtilisedBloodForm(FlaskForm):
	bg = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
	blood_group = SelectField(u'Blood Group', choices=bg, validators=[DataRequired()])
	units = IntegerField('Number of Units', validators=[DataRequired()])
	submit = SubmitField('Submit')
