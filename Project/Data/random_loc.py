import random
import sys
import math
import requests

# outfile = open("randomLatLong.txt", "w")

# radius = 10000                         #Choose your own radius
# radiusInDegrees=radius/111300            
# r = radiusInDegrees
# x0 = 73.82388
# y0 = 18.469621300000004

# for i in range(1,100):                 #Choose number of Lat Long to be generated

#   u = float(random.uniform(0.0,1.0))
#   v = float(random.uniform(0.0,1.0))

#   w = r * math.sqrt(u)
#   t = 2 * math.pi * v
#   x = w * math.cos(t) 
#   y = w * math.sin(t)
  
#   xLat  = x + x0
#   yLong = y + y0
#   outfile.write (str(xLat) + "," + str(yLong) + '\n')

r = requests.get('https://maps.googleapis.com/maps/api/geocode/json?latlng=40.714224,-73.961452&key=AIzaSyDEVlxGElqrqiRf74X3Ii-E2eF2S-TJVPY')

print(r.json())