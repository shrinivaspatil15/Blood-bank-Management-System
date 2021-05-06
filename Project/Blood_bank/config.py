import os

class Config:
	SECRET_KEY = 'ba3063fc18c772259fb550e4bf90919d'
	SQLALCHEMY_DATABASE_URI = 'postgresql://shri:1234@localhost/bloodbank'
	MAIL_SERVER = 'smtp.googlemail.com'
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	MAIL_USERNAME = os.environ.get('EMAIL_USER')
	MAIL_PASSWORD = os.environ.get('EMAIL_PASS')