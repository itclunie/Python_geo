import arcpy, os, sys, csv


csvinputdata = os.path.abspath('testwritinggeo.csv')
output_gdb = os.path.abspath('output.gdb')
testpoints2_shp__2_ = os.path.abspath('testpoints2.shp')
testwritinggeo = os.path.abspath('output.gdb\\testwritinggeo')
projectWGS1984 = "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119522E-09;0.001;0.001;IsHighPrecision"


arcpy.CreateFeatureclass_management(output_gdb, "testwritinggeo", "POINT", testpoints2_shp__2_, "DISABLED", "DISABLED", projectWGS1984, "", "0", "0", "0")


with open(csvinputdata, 'r') as output:
    reader = csv.reader(output, lineterminator = '\n')
    reader.next()
    csvlist = list(reader)
output.close()

Fieldzpre = arcpy.ListFields(testwritinggeo)
Fieldz = []
Fieldz.append('SHAPE@XY')
for f in Fieldzpre:
    Fieldz.append(f.name)

##for item in csvlist:
##    print(((float(item[3]),float(item[4])),item[0],item[1],item[2],item[3],item[4]))
##sys.exit()

with arcpy.da.InsertCursor(testwritinggeo,['SHAPE@XY','OBJECTID','Shape','CID','POINT_X','POINT_Y']) as rows:
    for item in csvlist:
        rows.insertRow(((float(item[3]),float(item[4])),item[0],item[1],item[2],item[3],item[4]))
        
##cursor.insertRow(((-111.0449838888, 32.657),"Name","Size"))
