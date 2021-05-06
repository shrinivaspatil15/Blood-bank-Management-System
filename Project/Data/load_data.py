import csv
import psycopg2
from random import randint
import phonenumbers

conn = psycopg2.connect("host=localhost dbname=bloodbank user=flaskblog password=flaskapp")

cur = conn.cursor()


modified_file = list()
with open('bloodbankdatamaha.csv', 'r') as f:
	reader = csv.reader(f)
	data = [r for r in reader]
	bloodbank_id = 2
	for bloodbank in data:
		if '' in bloodbank:
			continue
		address = bloodbank[4] + "," + bloodbank[3] + "-" + bloodbank[5] + "," + bloodbank[2] + "," + bloodbank[1]
		address = " ".join(address.split())
		contact_no = phonenumbers.parse(str(randint(7,9)) + str(randint(10**8,10**9-1)), "IN")
		contact_no = phonenumbers.format_number(contact_no, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
		latitude = float(bloodbank[7])
		longitude = float(bloodbank[8])
		insert_st = "INSERT INTO bloodbank VALUES ({}, '{}', '{}', '{}', '{}', {}, {}, st_setsrid(st_point({},{}),{}))" \
					  .format(bloodbank_id, bloodbank[0], address, contact_no, bloodbank[6], latitude, longitude, longitude, latitude, 4326)
		cur.execute(insert_st)
		bloodbank_id = bloodbank_id + 1
	
conn.commit()
cur.close()
