#    X  Y
#NE  +  +
#SW  -  -
#NW  -  +
#SE  +  -

#Easting_LatX
#Northing_LonY

#0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20
#2 5 0 1 5 7 0 6 0 N 1  2  1  3  2  2  3  0  4  0  E     DMS format

def coordconverter(coord):
    outlist = []

    if 'N' in coord and 'W' in coord: 
        degY = coord[0:2]
        minsY = coord[2:4]
        secY1 = coord[4:6]
        secY2 = coord[6:9]
        secY12 = coord[4:6] + "." + coord[6:9]
        secYDiv60 = float(coord[4:6] + "." + coord[6:9])/60
        Mmy = float(minsY) + float(secYDiv60)
        Mmy60 = Mmy/60
        LonY = int(degY) + Mmy60  

        degX = coord[10:13]
        minsX = coord[13:15]
        secX1 = coord[15:17]
        secX2 = coord[17:20]
        secX12 = coord[15:17] + "." + coord[17:20]
        secXDiv60 = float(coord[15:17] + "." + coord[17:20])/60
        MmX = float(minsX) + float(secXDiv60)
        MmX60 = MmX/60
        LatX = MmX60 + int(degX)
        
        rowAppend = [-LatX, LonY]
        outlist.append(rowAppend[0])
        outlist.append(rowAppend[1])
        
    elif 'N' in coord and 'E' in coord:
        degY = coord[0:2]
        minsY = coord[2:4]
        secY1 = coord[4:6]
        secY2 = coord[6:9]
        secY12 = coord[4:6] + "." + coord[6:9]
        secYDiv60 = float(coord[4:6] + "." + coord[6:9])/60
        Mmy = float(minsY) + float(secYDiv60)
        Mmy60 = Mmy/60
        LonY = int(degY) + Mmy60  

        degX = coord[10:13]
        minsX = coord[13:15]
        secX1 = coord[15:17]
        secX2 = coord[17:20]
        secX12 = coord[15:17] + "." + coord[17:20]
        secXDiv60 = float(coord[15:17] + "." + coord[17:20])/60
        MmX = float(minsX) + float(secXDiv60)
        MmX60 = MmX/60
        LatX = MmX60 + int(degX)
        
        rowAppend = [LatX, LonY]
        outlist.append(rowAppend[0])
        outlist.append(rowAppend[1])
        
    elif 'S' in coord and 'W' in coord:
        degY = coord[0:2]
        minsY = coord[2:4]
        secY1 = coord[4:6]
        secY2 = coord[6:9]
        secY12 = coord[4:6] + "." + coord[6:9]
        secYDiv60 = float(coord[4:6] + "." + coord[6:9])/60
        Mmy = float(minsY) + float(secYDiv60)
        Mmy60 = Mmy/60
        LonY = int(degY) + Mmy60  

        degX = coord[10:13]
        minsX = coord[13:15]
        secX1 = coord[15:17]
        secX2 = coord[17:20]
        secX12 = coord[15:17] + "." + coord[17:20]
        secXDiv60 = float(coord[15:17] + "." + coord[17:20])/60
        MmX = float(minsX) + float(secXDiv60)
        MmX60 = MmX/60
        LatX = MmX60 + int(degX)
        
        rowAppend = [-LatX, -LonY]
        outlist.append(rowAppend[0])
        outlist.append(rowAppend[1])
        
    elif 'S' in coord and 'E' in coord:
        degY = coord[0:2]
        minsY = coord[2:4]
        secY1 = coord[4:6]
        secY2 = coord[6:9]
        secY12 = coord[4:6] + "." + coord[6:9]
        secYDiv60 = float(coord[4:6] + "." + coord[6:9])/60
        Mmy = float(minsY) + float(secYDiv60)
        Mmy60 = Mmy/60
        LonY = int(degY) + Mmy60  

        degX = coord[10:13]
        minsX = coord[13:15]
        secX1 = coord[15:17]
        secX2 = coord[17:20]
        secX12 = coord[15:17] + "." + coord[17:20]
        secXDiv60 = float(coord[15:17] + "." + coord[17:20])/60
        MmX = float(minsX) + float(secXDiv60)
        MmX60 = MmX/60
        LatX = MmX60 + int(degX)
        
        rowAppend = [LatX, -LonY]
        outlist.append(rowAppend[0])
        outlist.append(rowAppend[1])

    return outlist
