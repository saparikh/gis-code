from dbfread import DBF
from geopy import geocoders
import time
import csv
import copy

google_maps_apikey = 'YOUR_GOOGLE_API_KEY'
DB_FILE = 'Export_Output.dbf' #Fox base database file
outfile = 'output_file.csv'

g = geocoders.GoogleV3(google_maps_apikey)
csv_data = dict()
out_csv = list(dict())

for record in DBF(DB_FILE):
    address = "{},{},{},{},USA".format(record['ADDRESS'], record['CITY'], record['STATE'], record['ZIP'])
    # google API sucks and keeps timing out, so cannot use the default timeout for the query
    # But still need to catch any error and retry. this method is hacky, but worked
    try:
        place, (lat, lng) = g.geocode(address, timeout=3)
    except:
        time.sleep(2)
        place, (lat, lng) = g.geocode(address, timeout=5)

    csv_data['OBJECTID'] = record["OBJECTID"]
    csv_data['INTPTLAT10'] = lat
    csv_data['INTPTLON10'] = lng
    csv_data['NAME'] = record['NAME']
    csv_data['ADDRESS'] = address
    csv_data['PLACE'] = place

    # important to append a copy of the dictionary, not the dictionary itself
    # the dictionary itself is being overwritten each time thru the loop
    # if you just append the dictionary, functionality you are just appending the pointer
    # so all of the list entries end up with the same data
    out_csv.append(csv_data.copy())
    print(record)

print(len(out_csv))

keys = out_csv[0].keys()
with open(outfile, 'w') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(out_csv)


