import os
import secrets
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import url_for, current_app
from flask_mail import Message
from Blood_bank import mail

def get_registration_token(name, email, contact_no, role, bloodbank_id):
		s = Serializer(current_app.config['SECRET_KEY'])
		return s.dumps({'name': name,\
						'email_id': email,\
						'contact_no': contact_no,\
						'role': role,\
						'bloodbank_id': bloodbank_id}).decode('utf-8')

def send_bloodbank_registration_email(name, email, contact_no, role, bloodbank_id):
	token = get_registration_token(name, email, contact_no, role, bloodbank_id)
	msg = Message('Blood Bank Admin Registration Link', sender='noreply@demo.com', recipients=[email])
	msg.body = f'''To activate account of your bloodbank visit following link:
{url_for('bloodbank_admin.register_admin', token=token, _external=True)}
'''
	mail.send(msg)