
# coding: utf-8

# In[1]:


import os, sys
import ogr
import shapefile as shp
from math import ceil
from shapely.geometry import Point
from shapely.geometry import Polygon
from rtree import index
import pandas as pd
from datetime import datetime

startTime = datetime.now() #0:00:42.883936


# In[2]:


#user inputs
outPath = "/Users/itclunie/Desktop/ECON/find industry/ChinaVIIRS/" #folder to dump results
pointfeat = '/Users/itclunie/Desktop/ECON/find industry/ChinaVIIRS/ChinaVIIRS.shp' #starting points
# outPath = "/Users/itclunie/Desktop/ECON/find industry/speedTest/" #folder to dump results
# pointfeat = '/Users/itclunie/Desktop/ECON/find industry/speedTest/chinaTest.shp' #starting points
polyfeat = outPath + 'outGrid2.shp' #name your output grid

dateColNum = 5 #in the csv/shapefile, which column is the date column? 1st col is 0, 2nd is 1, etc.
gridCutoff = 10 #gridcell has to have n num of months with values to be flagged
gridHeight = .02 #.015 = 1.5km
gridWidth = .02


# In[3]:


def makeGrid(outputGridfn,xmin,xmax,ymin,ymax,gridHeight,gridWidth):
    # convert sys.argv to float
    xmin = float(xmin)
    xmax = float(xmax)
    ymin = float(ymin)
    ymax = float(ymax)
    gridWidth = float(gridWidth)
    gridHeight = float(gridHeight)

    # get rows
    rows = ceil((ymax-ymin)/gridHeight)
    # get columns
    cols = ceil((xmax-xmin)/gridWidth)

    # start grid cell envelope
    ringXleftOrigin = xmin
    ringXrightOrigin = xmin + gridWidth
    ringYtopOrigin = ymax
    ringYbottomOrigin = ymax-gridHeight

    # create output file
    outDriver = ogr.GetDriverByName('ESRI Shapefile')
    if os.path.exists(outputGridfn):
        os.remove(outputGridfn)
        
    outDataSource = outDriver.CreateDataSource(outputGridfn)
    outLayer = outDataSource.CreateLayer(outputGridfn,geom_type=ogr.wkbPolygon )
    featureDefn = outLayer.GetLayerDefn()

    # create grid cells
    countcols = 0
    while countcols < cols:
        countcols += 1

        # reset envelope for rows
        ringYtop = ringYtopOrigin
        ringYbottom =ringYbottomOrigin
        countrows = 0

        while countrows < rows:
            countrows += 1
            ring = ogr.Geometry(ogr.wkbLinearRing)
            ring.AddPoint(ringXleftOrigin, ringYtop)
            ring.AddPoint(ringXrightOrigin, ringYtop)
            ring.AddPoint(ringXrightOrigin, ringYbottom)
            ring.AddPoint(ringXleftOrigin, ringYbottom)
            ring.AddPoint(ringXleftOrigin, ringYtop)
            poly = ogr.Geometry(ogr.wkbPolygon)
            poly.AddGeometry(ring)

            # add new geom to layer
            outFeature = ogr.Feature(featureDefn)
            outFeature.SetGeometry(poly)
            outLayer.CreateFeature(outFeature)
            outFeature.Destroy

            # new envelope for next poly
            ringYtop = ringYtop - gridHeight
            ringYbottom = ringYbottom - gridHeight

        # new envelope for next poly
        ringXleftOrigin = ringXleftOrigin + gridWidth
        ringXrightOrigin = ringXrightOrigin + gridWidth

    # Close DataSources
    outDataSource.Destroy()


# In[4]:


#make grid
pointfeatExtent = shp.Reader(pointfeat)

xmin = pointfeatExtent.bbox[0]
xmax = pointfeatExtent.bbox[2]
ymin = pointfeatExtent.bbox[1]
ymax = pointfeatExtent.bbox[3]

makeGrid(polyfeat,xmin,xmax,ymin,ymax,gridHeight,gridWidth)


# In[5]:


#A Load the shapefile of polygons and convert it to shapely polygon objects
polygons_sf = shp.Reader(polyfeat)
polygon_shapes = polygons_sf.shapes()
polygon_points = [q.points for q in polygon_shapes ]
polygons = [Polygon(q) for q in polygon_points]
poly_records = polygons_sf.records()


# In[6]:


#B Load the shapefile of points and convert it to shapely point objects
points_sf = shp.Reader(pointfeat)
pntRecords = points_sf.shapeRecords()
point_coords = [q.shape.points[0] for q in pntRecords ]
points = [Point(q.shape.points[0]) for q in pntRecords ]


# In[7]:


#C structure tally dictionaries

def mnthYearChange(instring):
    if "-" in instring:
        dtObj = datetime.strptime(instring, '%Y-%m-%d')
    elif "/" in instring and len(instring) <= 8:
        dtObj = datetime.strptime(instring, '%m/%d/%y')
    elif "/" in instring and len(instring) >= 8:
        dtObj = datetime.strptime(instring, '%m/%d/%Y')
    else:
        print("check date format, did you specify the right column?")
        sys.exit()
    return str(dtObj.month) + "_" + str(dtObj.year)

GRIDdict = {}
subGRIDdict = {}
VIIRSdict = {}

#select which column is the date column
for i in pntRecords:
    mnthYR = mnthYearChange(i.record[dateColNum])
    
    #add keys (monthYear) to VIIRSdict & GRIDdict
    if mnthYR in VIIRSdict:
        VIIRSdict[mnthYR].append(i)
    else:
        VIIRSdict[mnthYR] = []
        VIIRSdict[mnthYR].append(i) #key: monthYear, value: shape and attributes
        
    GRIDdict[mnthYR] = []
    

for i in poly_records: #fill subGRIDdict.  
    subGRIDdict[i[0]] = None ##key= GRIDID, value= {GRIDid:0...    looks like {0:0, 1:0, 2:0 ...

for key in GRIDdict:  #fill GRIDdict. 
    GRIDdict[key] = dict(subGRIDdict)  #key= 8_2012  value=  copies of subGRIDdict  
    


# In[8]:


#D Build a spatial index based on the bounding boxes of the polygons
idx = index.Index()

[ idx.insert(i, polygon_shapes[i].bbox) for i in range(len(polygon_shapes)) ]


# In[9]:


#actual points in grid cells matching

countr=0
for key in VIIRSdict:
    tallyHO = []
    point_coords = [ q.shape.points[0] for q in VIIRSdict[key] ]
    points = [ Point(q.shape.points[0]) for q in VIIRSdict[key] ]    
    
    for i in range(len(VIIRSdict[key])): #Iterate through each point

        #Iterate only through the bounding boxes which contain the point. Verify that point is within the polygon itself not just the bounding box        
        for j in idx.intersection(point_coords[i]):
            #Verify that point is within the polygon itself not just the bounding box
            if points[i].within(polygons[j]):       
                tallyHO.append(poly_records[j][0]) 
                break 

    resultDict = dict([ (i,tallyHO.count(i)) for i in set(tallyHO) ])

    for rkey in resultDict:
        GRIDdict[key][rkey] = resultDict[rkey] 
            
    countr += 1
    print( countr, len( VIIRSdict.keys() ) )


# In[ ]:


#remove empty rows (ie empty grid squares), pick out hexes of interest, add centroids
dfClean = pd.DataFrame.from_dict(GRIDdict, orient='columns', dtype=None) #the dataframe is the grid 
dfClean['X'] = None
dfClean['Y'] = None

dropLst = []
for i in range(len(dfClean)):
    row = dfClean.iloc[i]    
    
    if row.count() >= gridCutoff:  #user input
        centroid = polygons[i].centroid
        cX = centroid.coords[0][0]
        cY = centroid.coords[0][1]
        dfClean.at[i,'X'] = cX
        dfClean.at[i,'Y'] = cY
    else:
        dropLst.append(i)

    if i % 10000 == 0:
        print( i, len(dfClean) )
    
    
df = dfClean.drop(dropLst)


# In[ ]:


#write output files

df.to_csv(outPath + 'industryFindR_wide.csv')
dfClean['GRIDid'] = dfClean.index
melted = dfClean.melt(id_vars=['GRIDid','X','Y']) 
melted.to_csv(outPath + 'industryFindR_long.csv')

print(datetime.now() - startTime)

