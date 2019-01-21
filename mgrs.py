import csv
import mgrs

# This script converts lat and long to a MGRS (Military Grid Reference Systems) reference
out_csv = list(dict())
file = 'in_file'
outfile = 'out_file.csv'

with open(file, mode='r') as infile:
    reader = csv.reader(infile)
    count = 0
    for rows in reader:
        print(rows)
        #first row in CSV is header, so need to handle this case
        if count == 0:
            header = rows
            header.append('MGRS')
        else:
            lat = float(rows[1])
            long = float(rows[2])
            m = mgrs.MGRS()
            c = m.toMGRS(lat, long)
            print(c)
            # this is of type(byte), so need to convert to string as below
            rows.append(c.decode("utf-8"))
        count += 1
        out_csv.append(rows)


with open(outfile, 'w') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    for rows in out_csv:
        wr.writerow(rows)
