import requests, datetime, time, sys, os, csv, arcpy
from datetime import timedelta, date

def parseRecs(myText, excludeHeaders=True):
    resultIDBlank = ''
    pagesBlank = ['','']
    recordsBlank = ''
    try:
        lines = resp.text.split('\n')
        resultID = lines[0].split(':')[-1] #This is used for paging through results
        pages = lines[1].split()
        pages=[int(pages[1]),int(pages[-1])] # causes 'IndexError: list index out of range'
        if excludeHeaders:
            startline = 4
        else:
            startline = 3
        records=lines[startline:-2] #exclude the overall classification
        return resultID,pages[0],pages[1],records
    except:
        return resultIDBlank,pagesBlank[0],pagesBlank[1],recordsBlank
    
def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)


#------------------------------------------------------------------seawatch autoquery--------------------------------------------------------------------------------------------

baseURL="http://---etc---"
pageSize=1000 #can be up to 1000

#enter your main date range here
start_date = date(2015,1,1) 
end_date = date(2015,1,31)

#pull seawatch data for each day in range
for single_date in daterange(start_date, end_date): 
    
    single_dateVar = single_date.strftime("%Y,%m,%d")
    startDateList = str(single_dateVar).split(",")

    print "processing: " + single_dateVar

    startDate=datetime.datetime(int(startDateList[0]),int(startDateList[1]),int(startDateList[2]))
    endDate=datetime.datetime(int(startDateList[0]),int(startDateList[1]),int(startDateList[2]))

    #create/overwrite output CSV
    outputfilePath = "C:\\Shared\\----etc----"
    outputfilename=  outputfilePath + single_dateVar + "_APPENDME.csv"   
 
    with open(outputfilename, 'w') as output:
        writer = csv.writer(output, lineterminator = '\n')
        writer.writerows([])
            
    #this is one long list made up of tuples. This could have been a dict however the repeating value sfTypeSelect[] needed this format
    form = [("fromdate",startDate.strftime("%Y-%m-%d")),("todate",endDate.strftime("%Y-%m-%d")),("service","positlookup"), 
            ("classificationOperator","equal"),("classificationValues",""),("classification",""),
			
			#etc
			
            ("northLatitude",""),("westLongitude",""),("southLatitude",""),("eastLongitude",""),("centerLatitude",""),("centerLongitude",""),("miles","0"),
            ("pagesize",str(pageSize)),
            ("format","csv")]  #You can change to txt for fixed width text), or xml), or atom etc.

    
    sesh = requests.Session() #keep cookies
    tries=1
    success=False
    while tries < 20 and not success: #loop to retry get request. usually goes after 1 or 2 tries
        try:
            resp=sesh.get(baseURL,params=form,timeout=None)
            success=True
        except:
            print 'retrying get request. Retry #' + str(tries)
            tries+=1
            time.sleep(1)
                        
    rID,this_page,max_page,recs = parseRecs(resp.text,False)  #the False here says don't skip the header row
    print single_dateVar, ' queryID:', rID, 'page',this_page,'of',max_page,'. Rows:',len(recs)


    #create new csv and append 1st page to csv
    with open(outputfilename, 'w') as outfile:
        for row in recs:
            outfile.write(row + '\n')
            

    #Get the remaining pages
    pageForm={"heading":"Posit+Report",
        "format":"csv",
        "resultskey":rID,
        "sortcolumns":"",
        "pagesize":str(pageSize),
        "service":"positlookup",
        "resultcolumns":"securityClassification, --etc--" #same as column headers
        "version":"2",
        "nav":"N"}  #the 'nav':'N' means next page, I believe 'nav':'P' will return previous page


    with open(outputfilename, 'a') as outfile: #reopen csv for append. iterate through remaining seawatch pages and dump into csv
        while this_page < max_page:
            resp = sesh.get(baseURL,params=pageForm,timeout=None,verify=False)
            rID,this_page,max_page,recs = parseRecs(resp.text) #There's no False here, so we'll skip the header row

            for row in recs:
                outfile.write(row + '\n')
            print single_dateVar, ' queryID:',rID, 'page',this_page,'of',max_page,'. Rows:',len(recs)

##    time.sleep(1)

print "done with pull"




