import psycopg2
import random
import string

conn = psycopg2.connect("host=localhost dbname=bloodbank user=flaskblog password=flaskapp")
cur = conn.cursor()

def makeName():
	namelen = random.randint(1,20)
	name = ''.join(random.choice(string.ascii_lowercase) for _ in range(namelen))
	return name

def makeEmail():
	extensions = ['com','net','org','gov']
	domains = ['gmail','yahoo','comcast','verizon','charter','hotmail','outlook','frontier']

	ext = extensions[random.randint(0,len(extensions)-1)]
	dom = domains[random.randint(0,len(domains)-1)]

	acclen = random.randint(1,20)

	acc = ''.join(random.choice(string.ascii_lowercase) for _ in range(acclen))

	email = acc + "@" + dom + "." + ext
	return email


def makeContact_no():
	contact_no = "+91" + str(random.randint(7,9)) + str(random.randint(10**8,10**9-1))
	return contact_no

def makeBG():
	blood_groups = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
	bg = blood_groups[random.randint(0, len(blood_groups)-1)]
	return bg

def makeDate():
	month = random.randint(1,12)
	if month==2:
		date = random.randint(1,28)
	elif month in [4, 6, 9, 11]:
		date = random.randint(1,30)
	else:
		date = random.randint(1,31)
	year = 2020
	Date = psycopg2.Date(year, month, date)
	return Date



for donor_id in range(1, 6001):
	name = makeName()
	email = makeEmail()
	contact_no = makeContact_no()
	blood_group = makeBG()
	last_date = makeDate()

	insert_st = "INSERT INTO donor VALUES ({}, '{}', '{}', '{}', '{}', {})".format(1, name, email, contact_no, blood_group, last_date)

	cur.execute(insert_st)

conn.commit()
cur.close()
conn.close()