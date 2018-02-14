#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 13:13:17 2018

@author: itclunie
"""

import arcpy, os, timeit, time, sys, csv, urllib2 , zipfile, shutil, inspect, random, string


#4------------------------------write geos--------------------------------------------------------------------------
#IMPORTANT: in arcmap, edit template_feature so that every field (except objectID & shape) are text/string type.
#Also needs to be empty of rows. Also some fields might need to be expanded to 255
template_feature = os.path.abspath('JoinTABLE_Table.gdb\\template_Feature')
projectWGS1984 = "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',  etc..."


#make headers list
OutFieldz = []
OutFieldz.append('SHAPE@XY')
fieeeelds = arcpy.ListFields(Facilities)
for f in fieeeelds[2:]:
    OutFieldz.append(f.name)

arcpy.CreateFeatureclass_management('Output_gdb', 'name', "POINT", template_feature,
                                    "DISABLED", "DISABLED", projectWGS1984, "", "0", "0", "0")
    
with arcpy.da.InsertCursor(emptyfeat,OutFieldz) as cursor:
    for item in somelist:
        xy = ()
        xy = (float(item[72]),float(item[73])) #make geo
        
        Appended2 = []
        Appended2.append(xy)
        
        for i in range(len(somelist))[2:]:
            Appended2.append(somelist[i])

        cursor.insertRow(Appended2)


#4.5------------------------------update geos--
splitted = []
with arcpy.da.UpdateCursor(DTRA, Fieldz) as cursor:
    for row in cursor:
        
        holdstr = str(row[21])
        splitted = holdstr.split('.0')
        row[22] = splitted[0]
        cursor.updateRow(row)