import csv, sys, os, requests, re, mechanize, cookielib
##reload(sys)
##sys.setdefaultencoding("utf-8")


csvOutput = os.path.abspath('PRIS_pull.csv')
##csvHeaders = ['Country@Facility@Reactor Type@Status@Location@Model@Owner@Operator@Reference Unit Power (net capacity)@Design Net Capacity@Gross Capacity@Thermal Capacity@Construction Start@First Criticality@Construction Suspended@Construction Restarted@First Grid Connection@Commercial Operation@Grid Connection@Long Term Shutdown@Restart@Permanent Shutdown@Country URL']
csvHeaders = ['Country','Facility','Reactor Type','Status','Location','Model','Model2','Owner','Operator','Reference Unit Power (net capacity)','Design Net Capacity',
              'Gross Capacity','Thermal Capacity','Construction Start','First Criticality','Construction Suspended','Construction Restarted','First Grid Connection',
              'Commercial Operation','Grid Connection','Long Term Shutdown','Restart','Permanent Shutdown','Country URL']

with open(csvOutput, 'w') as output:
    writer = csv.writer(output, lineterminator = '\n')
    writer.writerows([csvHeaders])


Referer = 'https://www.iaea.org/pris/CountryStatistics/CountryDetails.aspx?current='
##countryInitials = ['DE']
countryInitials = ['AR','AM','BY','BE','BR','BG','CA','CN','CZ','FI','FR','DE','HU','IN','IR','IT','JP','KZ','KR','LT','MX','NL','PK','RO','RU','SK','SI','ZA','ES','SE','CH','UA','AE','GB','US']

#-------------------------------------------------------------------------------------------------------1 country get

for item in countryInitials:
    print 'crawling ' + Referer + item + '...'
    
    countryURL = Referer + item
    resp = requests.get(countryURL)

    #for fac POST                                      VS                                     EV                                                  country
    VIEWSTATE_EVENTVAL = re.search('VIEWSTATE" value="(.*?)" \/>(.*?)EVENTVALIDATION" value="(.*?)" \/>(.*?)MainContent_MainContent_lblCountryName">(.*?)<', resp.content, re.MULTILINE|re.IGNORECASE|re.DOTALL)
    VIEWSTATE = VIEWSTATE_EVENTVAL.group(1)
    EVENTVAL = VIEWSTATE_EVENTVAL.group(3)
    Country = VIEWSTATE_EVENTVAL.group(5)

    
                        #         1jvs      2--    3name     4--       5type       6--       7status     8--       9loc
    for m in re.finditer('\(&#39;(.*?)&#39;(.*?)">(.*?)<\/a>(.*?)left">(.*?)<\/td>(.*?)left">(.*?)<\/td>(.*?)left">(.*?)<\/td>', resp.content, re.MULTILINE|re.IGNORECASE|re.DOTALL):
        tempListFac = []
        joinedList = []
        
        
        JS_postback = m.group(1).strip() #0 JS postback
        tempListFac.append(Country)
        tempListFac.append(m.group(3).strip())#1 fac name
        tempListFac.append(m.group(5).strip())#2 type
        tempListFac.append(m.group(7).strip())#3 status
        tempListFac.append(m.group(9).strip())#4 location
        

#-------------------------------------------------------------------------------------------------------2 fac post

        params = {}
        params = {"ToolkitScriptManager1_HiddenField":"",
                  "__EVENTTARGET":JS_postback, #0 JS postback
                  "__EVENTARGUMENT":"",
                  "__VIEWSTATE":VIEWSTATE,
                  "__VIEWSTATEGENERATOR":"",
                  "__EVENTVALIDATION":EVENTVAL}

        #fac POST
        print 'crawling ' + tempListFac[1] + '...'
        resp2 = requests.post(countryURL, data=params)
        html2 = resp2.content


        for m2 in re.finditer('lblType">(.*?)<\/',resp2.content, re.MULTILINE|re.IGNORECASE|re.DOTALL):
            tempListFac.append(m2.group(1).strip().replace('\n',''))
        for m2 in re.finditer('lblModel">(.*?)<\/',resp2.content, re.MULTILINE|re.IGNORECASE|re.DOTALL):
            tempListFac.append(m2.group(1).strip().replace('\n',''))


    #hypOwnUrl hypOperatorUrl problem --, ++, ow+ op-, ow- op+
        OwnerPresent = html2.find('hypOwnerUrl')
        OperatorPresent = html2.find('hypOperatorUrl')
        
        if OwnerPresent > -1 and OperatorPresent > -1: #++
            for m2 in re.finditer('hypOwnerUrl(.*?)>(.*?)<\/(.*?)hypOperatorUrl(.*?)>(.*?)<\/',html2, re.MULTILINE|re.IGNORECASE|re.DOTALL):
                tempListFac.append(m2.group(2).strip().replace('\n','').replace('\r',''))
                tempListFac.append(m2.group(5).strip().replace('\n','').replace('\r',''))
                print '++'
        if OwnerPresent == -1 and OperatorPresent == -1: #--
            for m2 in re.finditer('lblModel(.*?)<h5>(.*?)<\/h5>(.*?)<h5>(.*?)<\/h5>',html2, re.MULTILINE|re.IGNORECASE|re.DOTALL):#  1- 2own 3- 4op
                tempListFac.append(m2.group(2).strip().replace('\n','').replace('\r',''))
                tempListFac.append(m2.group(4).strip().replace('\n','').replace('\r',''))
                print '--'
        if OwnerPresent > -1 and OperatorPresent == -1: #ow+ op-
            for m2 in re.finditer('hypOwnerUrl(.*?)>(.*?)<\/(.*?)<h5>(.*?)<\/h5>',html2, re.MULTILINE|re.IGNORECASE|re.DOTALL): #  1- 2own 3- 4op
                tempListFac.append(m2.group(2).strip().replace('\n','').replace('\r',''))
                tempListFac.append(m2.group(4).strip().replace('\n','').replace('\r',''))
                print '+-'
        if OwnerPresent == -1 and OperatorPresent > -1: #ow- op+
            for m2 in re.finditer('lblModel(.*?)<h5>(.*?)<\/h5>(.*?)hypOperatorUrl(.*?)">(.*?)<\/a',html2, re.MULTILINE|re.IGNORECASE|re.DOTALL): #  1- 2own 3- 4- 5op
                tempListFac.append(m2.group(2).strip().replace('\n','').replace('\r',''))
                tempListFac.append(m2.group(5).strip().replace('\n','').replace('\r',''))
                print '-+'

         
        for m2 in re.finditer('lblNetCapacity">(.*?)<\/',resp2.content, re.MULTILINE|re.IGNORECASE|re.DOTALL):
            tempListFac.append(m2.group(1).strip().replace('\n','').replace('\r',''))
        for m2 in re.finditer('lblDesignNetCapacity">(.*?)<\/',resp2.content, re.MULTILINE|re.IGNORECASE|re.DOTALL):
            tempListFac.append(m2.group(1).strip().replace('\n','').replace('\r',''))
        for m2 in re.finditer('lblGrossCapacity">(.*?)<\/',resp2.content, re.MULTILINE|re.IGNORECASE|re.DOTALL):
            tempListFac.append(m2.group(1).strip().replace('\n','').replace('\r',''))
        for m2 in re.finditer('lblThermalCapacity">(.*?)<\/',resp2.content, re.MULTILINE|re.IGNORECASE|re.DOTALL):
            tempListFac.append(m2.group(1).strip().replace('\n','').replace('\r',''))


        for m2 in re.finditer('lblConstructionStartDate">(.*?)<\/',resp2.content, re.MULTILINE|re.IGNORECASE|re.DOTALL):
            tempListFac.append(m2.group(1).strip().replace('\n','').replace('\r',''))
        for m2 in re.finditer('lblFirstCriticality">(.*?)<\/',resp2.content, re.MULTILINE|re.IGNORECASE|re.DOTALL):            
            tempListFac.append(m2.group(1).strip().replace('\n','').replace('\r',''))
        for m2 in re.finditer('lblConstrSuspendedDate">(.*?)<\/',resp2.content, re.MULTILINE|re.IGNORECASE|re.DOTALL):
            tempListFac.append(m2.group(1).strip().replace('\n','').replace('\r',''))
        for m2 in re.finditer('lblConstrRestartDate">(.*?)<\/',resp2.content, re.MULTILINE|re.IGNORECASE|re.DOTALL):
            tempListFac.append(m2.group(1).strip().replace('\n','').replace('\r',''))
            

        for m2 in re.finditer('lblGridConnectionDate">(.*?)<\/',resp2.content, re.MULTILINE|re.IGNORECASE|re.DOTALL):
            tempListFac.append(m2.group(1).strip().replace('\n','').replace('\r',''))
        for m2 in re.finditer('lblCommercialOperationDate">(.*?)<\/',resp2.content, re.MULTILINE|re.IGNORECASE|re.DOTALL):            
            tempListFac.append(m2.group(1).strip().replace('\n','').replace('\r',''))
        for m2 in re.finditer('lblLongTermShutdownDate">(.*?)<\/',resp2.content, re.MULTILINE|re.IGNORECASE|re.DOTALL):
            tempListFac.append(m2.group(1).strip().replace('\n','').replace('\r',''))
        for m2 in re.finditer('lblRestartDate">(.*?)<\/',resp2.content, re.MULTILINE|re.IGNORECASE|re.DOTALL):            
            tempListFac.append(m2.group(1).strip().replace('\n','').replace('\r',''))
        for m2 in re.finditer('lblPermanentShutdownDate">(.*?)<\/',resp2.content, re.MULTILINE|re.IGNORECASE|re.DOTALL):            
            tempListFac.append(m2.group(1).strip().replace('\n','').replace('\r',''))
                                                                
        tempListFac.append(countryURL)

##        joinString = "@".join(tempListFac)
##        joinedList.append(joinString)


        with open(csvOutput, 'a') as output:
            writer = csv.writer(output, lineterminator = '\n')
            writer.writerows([tempListFac])


print 'done'

