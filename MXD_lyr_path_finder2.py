# -*- coding: utf-8 -*-

import arcpy, os, csv


def main(folder, outputfile):
    with open(outputfile, "wb") as f:
        w = csv.writer(f)
        header = ("Map Document", "MXD Path", "DataFrame Name", "DataFrame Description", "Layer name", "Layer Datasource")
        w.writerow(header)
        rows = crawlmxds(folder)
        w.writerows(rows)


def crawlmxds(folder):
    for root, dirs, files in os.walk(folder):

        for f in files:

            try:
                if f.lower().endswith(".mxd"):
                    mxdName = os.path.splitext(f)[0]
                    mxdPath = os.path.join(root, f)
                    mxd = arcpy.mapping.MapDocument(mxdPath)
                    dataframes = arcpy.mapping.ListDataFrames(mxd)
                    
                    for df in dataframes:
                        dfDesc = df.description if df.description != "" else "None"
                        layers = arcpy.mapping.ListLayers(mxd, "", df)
                        
                        for lyr in layers:
                            lyrName = lyr.name
                            lyrDatasource = lyr.dataSource if lyr.supports("dataSource") else "N/A"
                            seq = (mxdName, mxdPath, df.name, dfDesc, lyrName, lyrDatasource);
                            yield seq
                    del mxd
            except:
                pass


if __name__ == "__main__":
    folderPath = r"J:\Shared\J2-5-8R\J20\CIIC\Geospatial" # or arcpy.GetParameterAsText(0)
    output = r"H:\MXDpathListNIPR.csv" # or arcpy.GetParameterAsText(1)
    main(folderPath, output)
