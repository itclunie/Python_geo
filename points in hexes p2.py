
import arcpy, os, sys, csv

inputCSV = r"J:\Shared\--etc-- \_2015-01-01_2015-01-31.csv" #the csv path with coordinates
projectWGS1984 = "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]], --etc--"

feat2fillname = 'test'#name of new feature class
feat2fillpath = 'J:\\Shared\\--etc--\\CSVs\\' #path to new feat
fullPath = feat2fillpath + feat2fillname + '.shp'

#----------------------------------------------------------------------------fill empty .shp with csv coords-----------------------------------------------------------------------------
         
arcpy.CreateFeatureclass_management(feat2fillpath, feat2fillname, "POINT", "", "DISABLED", "DISABLED", projectWGS1984, "", "0", "0", "0") #create blank feature class 
Thousand = 0
count = 0
with open(inputCSV, 'r') as opener:
    reader = csv.reader(opener)
    reader.next()

    with arcpy.da.InsertCursor(fullPath,["SHAPE@XY"]) as cursor: #writing xy geometries
        for item in reader:
            xy = ()
            xy = (float(item[1]),float(item[0])) #item[n] and item[n] have to match up to lon lat
            cursor.insertRow([xy])
            
            Thousand += 1
            count += 1
            if Thousand == 1000:
                Thousand = 0
                print str(count) + ' points created'

print 'created feature class from points'

#----------------------------------------------------------------------------join new .shp w/ OceanHexes. Clean, add % total, & dissolve---------------------------------------------

print 'joining feature class with OceanHexes'

OceanHexes = r"J:\Shared\--etc--\OceanHexes.shp" #regular hexigon polygons covering the oceans. Coords are aggregated within them
JoinFeature = feat2fillpath + feat2fillname + '_join.shp'
arcpy.SpatialJoin_analysis(OceanHexes, fullPath, JoinFeature, "JOIN_ONE_TO_ONE", "KEEP_ALL", "","INTERSECT", "", "") #spatial join
arcpy.AddField_management(JoinFeature, "Perc", "FLOAT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "") #add empty field to .shp

print 'cleaning null values'
Fieldz = []
for f in arcpy.ListFields(JoinFeature):
    Fieldz.append(f.name)

sumofpoints = 0
with arcpy.da.UpdateCursor(JoinFeature, Fieldz) as cursor:
    for row in cursor:
        if row[2] == 0:
            cursor.deleteRow()
        else:
            sumofpoints = sumofpoints + row[2]
            
print 'calculating percent total for each hexigon'

with arcpy.da.UpdateCursor(JoinFeature, Fieldz) as cursor:
    for row in cursor:
        print row
        PercIn = (float(row[2]) / float(sumofpoints)) * 100
        row[6] = PercIn 
        cursor.updateRow(row)


print 'dissolving repeat hexes'
dissolveFeature = feat2fillpath + feat2fillname + '_dissolve.shp'
arcpy.Dissolve_management(JoinFeature, dissolveFeature, "Join_Count", "", "MULTI_PART", "DISSOLVE_LINES")

print 'done'


