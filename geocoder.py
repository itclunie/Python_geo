import requests, csv, os

csvPath = os.path.abspath("sampleAddress.csv")
csvOutput = os.path.abspath("AddressOutput.csv")

csvHeaders = ['street adrs','lat','lng','name']

with open(csvPath, 'r') as output:
    reader = csv.reader(output, lineterminator = '\n')
    addresses = list(reader)

addCoords = []
for item in addresses:
    if item[0] != "":

        noSpaces = item[0].replace(" ","+")

        try:
            try:
                r = requests.get("https://maps.google.com/maps/api/geocode/json?address=" + noSpaces)

                newJSON = r.json()

                lat = newJSON['results'][0]['geometry']['location']['lat']
                lng = newJSON['results'][0]['geometry']['location']['lng']

                addCoords.append([item[0],lat,lng,item[1]])
            except:
                addCoords.append([item[0], 'failed', 'google'])

        except:
            print('using OSM ', item[0])
            try:
                r = requests.get("https://nominatim.openstreetmap.org/search?format=json&polygon=1&addressdetails=1&q=" + noSpaces)
                newJSON = r.json()
                lat = newJSON[0]['lat']
                lon = newJSON[0]['lon']
                print(lat,lon)
                addCoords.append([item[0], lat, lng, item[1]])
            except:
                addCoords.append([item[0], 'failed', 'osm'])


with open(csvOutput, 'w') as output:
    writer = csv.writer(output, lineterminator = '\n')
    writer.writerows([csvHeaders])

    for item in addCoords:
        writer.writerows([item])