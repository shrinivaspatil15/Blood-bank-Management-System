import os
import secrets
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from Blood_bank import mail


def save_picture(form_picture):
	random_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = random_hex + f_ext
	picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
	output_size = (125, 125)
	i = Image.open(form_picture)
	i.thumbnail(output_size)
	i.save(picture_path)
	return picture_fn


def get_registration_token(email):
		s = Serializer(current_app.config['SECRET_KEY'])
		return s.dumps({'email_id': email}).decode('utf-8')

def send_registration_email(email):
	token = get_registration_token(email)
	msg = Message('Blood Bank Registration Link', sender='noreply@demo.com', recipients=[email])
	msg.body = f'''To register in bloodbank visit following link:
{url_for('users.register', token=token, _external=True)}
'''
	mail.send(msg)

def send_reset_email(user):
	token = user.get_reset_token()
	msg = Message('Password Reset Link', sender='noreply@demo.com', recipients=[user.email])
	msg.body = f'''To reset your password visit following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request then ignore this mail and no changes will be made.
'''
	mail.send(msg)


def send_request(email_list, blood_group, units, user):
	msg = Message('Request for Blood', sender='noreply@demo.com', recipients=email_list)
	msg.body = f'''There is need for {units} units of blood group {blood_group} in nearby area.

	
Contact Details:
Name: {user.name}
Contact no.: {user.contact_no}
Email-id: {user.email}
'''
	mail.send(msg)