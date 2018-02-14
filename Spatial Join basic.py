import arcpy

talleyHo = []
pointCount = 0
pointCountK = 0

pointfeat = r".shp"
polyfeat  = r".shp"
arcpy.AddSpatialIndex_management(pointfeat)
arcpy.AddSpatialIndex_management(polyfeat)

for point in arcpy.da.SearchCursor(pointfeat):
    pointCount += 1
    if pointCount == 1000:
        pointCountK += 1
        pointCount = 0
        print pointCountK

    pointFeature = point.shape #set the comparison geometry to each pnt

    polycount = 0
    for polygon in arcpy.da.SearchCursor(polyfeat):
        polyFeature = polygon.shape #set base geom to each polygon

        if polyFeature.contains(pointFeature) == True:
            polycount += 1

    tempStr = str(polygon.FID) + "@" + str(polycount)
    talleyHo.append(tempStr)

for item in talleyHo:
    print item
