from geoalchemy2.types import Geometry
import psycopg2

conn = psycopg2.connect("host=localhost dbname=bloodbank user=shri password=1234")
cur = conn.cursor()
cur.execute("CREATE EXTENSION postgis")
conn.commit()
cur.close()
conn.close()