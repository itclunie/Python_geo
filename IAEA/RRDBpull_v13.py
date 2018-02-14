# encoding=utf8

import time, os, re, csv, sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

reload(sys)
sys.setdefaultencoding("utf-8")

# driver = webdriver.Ie("C:\\Users\\User\\Downloads\\IEDriverServer_x64_2.42.0\\IEDriverServer.exe") #also add https://nucleus.iaea.org to trusted sites
driver = webdriver.Chrome("C:\\Users\\User\\Downloads\\chromedriver_win32\\chromedriver.exe")
csvOutput = os.path.abspath('RRDBpull.csv')
csvHeaders = ['IAEA code','Owner','Operating Organization','Regulatory Body','International Safeguards',
              'POC name','POC division','POC dir','POC tel','POC street 1','POC post code 1','POC province','POC email','POC dir title','POC street2','POC city','POC post code 2',
              'Staff operators','Staff total','History start construc','History 1st criticality','Annual cost (m US$)','URL'
              
              'Reactor','IAEA code','Reactor type','Therm Power Steady (kW)', 'Therm Power Puls(MW)','Max Flux SS, Thermal (n/cm2-s)','Max Flux Puls, Thermal (n/cm2-s)','Max flux SS, Fast (n/cm2-s)','Max Flux Puls, Fast (n/cm2-s)','Moderator Material','Coolant Material',

              'Hours per Day','Days per Week','Weeks per Year','MW Days per Year',

              'Planned Decommission Start','Planned Decommission Completed','Current Decommission Start','Completed Decommission Year']

with open(csvOutput, 'w') as output:
    writer = csv.writer(output, lineterminator = '\n')
    writer.writerows([csvHeaders])
    

for i in range(794,850): #795
    if i != 0:
        url = 'https://nucleus.iaea.org/RRDB/RR/GeneralInfo.aspx?RId=795' #+ str(i)
        driver.get(url)
        try:
            element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "txtOwner"))) #might need to change
            
        finally:
            facLinks = []
            
            emptyCheck = re.search('reactorContent"(.*?)\/span>',driver.page_source, re.MULTILINE|re.IGNORECASE|re.DOTALL)
            emptyCheck = emptyCheck.group(1)
            if '><' in emptyCheck:
                pass
                print i
            else:
        
                IAEAcode = re.search('_ctl5_lblIAEACode(.*?)">(.*?)<\/span',driver.page_source, re.MULTILINE|re.IGNORECASE|re.DOTALL)
                facLinks.append(IAEAcode.group(2).strip().replace('\n','').replace('\r',''))                    
        
                Owner__ = re.search('name="txtOwner"(.*?)txtOwner',driver.page_source, re.MULTILINE|re.IGNORECASE|re.DOTALL)
                Owner__ = Owner__.group(1).strip().replace('\n','').replace('\r','')
                if 'value=' in Owner__:
                    Owner = re.search('name="txtOwner"(.*?)value="(.*?)" maxlength',driver.page_source, re.MULTILINE|re.IGNORECASE|re.DOTALL)
                    facLinks.append(Owner.group(2).strip().replace('\n','').replace('\r',''))                    
                else:
                    facLinks.append(' ')
        
                OperatingOrg__ = re.search('name="txtOperator"(.*?)txtOperator',driver.page_source, re.MULTILINE|re.IGNORECASE|re.DOTALL)
                OperatingOrg__ = OperatingOrg__.group(1).strip().replace('\n','').replace('\r','')
                if 'value=' in OperatingOrg__:
                    OperatingOrg = re.search('name="txtOperator"(.*?)value="(.*?)" maxlength',driver.page_source, re.MULTILINE|re.IGNORECASE|re.DOTALL)
                    facLinks.append(OperatingOrg.group(2).strip().replace('\n','').replace('\r',''))                    
                else:
                    facLinks.append(' ')                        
        
                RegBody__ = re.search('name="txtLicensing"(.*?)textarea',driver.page_source, re.MULTILINE|re.IGNORECASE|re.DOTALL)
                RegBody__ = RegBody__.group(1).strip().replace('\n','').replace('\r','')
                if '><' in RegBody__:
                    RegBody = re.search('id="txtLicensing"(.*?)">(.*?)<\/textarea',driver.page_source, re.MULTILINE|re.IGNORECASE|re.DOTALL)
                    facLinks.append(RegBody.group(2).strip().replace('\n','').replace('\r',''))                    
                else:
                    facLinks.append(' ')
        
                SafeGuard__ = re.search('name="cboSafeguards"(.*?)<\/select',driver.page_source, re.MULTILINE|re.IGNORECASE|re.DOTALL)
                SafeGuard__ = SafeGuard__.group(1).strip().replace('\n','').replace('\r','')
                if 'selected=' in SafeGuard__:
                    SafeGuard = re.search('id="cboSafeguards"(.*?)selected"(.*?)">(.*?)</',driver.page_source, re.MULTILINE|re.IGNORECASE|re.DOTALL)
                    facLinks.append(SafeGuard.group(3).strip().replace('\n','').replace('\r',''))
                else:
                    facLinks.append(' ')                        
        
        #POC
                POCnametest = re.search('name="txtRAdminName"(.*?)txtRAdminName',driver.page_source, re.MULTILINE|re.IGNORECASE|re.DOTALL)
                POCnametest = POCnametest.group(1).strip().replace('\n','').replace('\r','')
                if 'value=' in POCnametest:
                    POCname = re.search('name="txtRAdminName"(.*?)value="(.*?)" maxlength',driver.page_source, re.MULTILINE|re.IGNORECASE|re.DOTALL)
                    facLinks.append(POCname.group(2).strip().replace('\n','').replace('\r',''))
                else:
                    facLinks.append(' ')
               
                POCdivtest = re.search('name="txtRAdminDiv"(.*?)txtRAdminDiv',driver.page_source, re.MULTILINE|re.IGNORECASE|re.DOTALL)
                POCdivtest = POCdivtest.group(1).strip().replace('\n','').replace('\r','')
                if 'value=' in POCdivtest:
                    POCdiv = re.search('name="txtRAdminDiv"(.*?)value="(.*?)" maxlength',driver.page_source, re.MULTILINE|re.IGNORECASE|re.DOTALL)
                    facLinks.append(POCdiv.group(2).strip().replace('\n','').replace('\r',''))
                else:
                    facLinks.append(' ')
        
                POCdirtest = re.search('name="txtRAdminDir"(.*?)id="txtRAdminDir',driver.page_source, re.MULTILINE|re.IGNORECASE|re.DOTALL)
                POCdirtest = POCdirtest.group(1).strip().replace('\n','').replace('\r','')
                if 'value=' in POCdivtest:
                    POCdir = re.search('name="txtRAdminDir"(.*?)value="(.*?)" maxlength',driver.page_source, re.MULTILINE|re.IGNORECASE|re.DOTALL)
                    facLinks.append(POCdir.group(2).strip().replace('\n','').replace('\r',''))
                else:
                    facLinks.append(' ')                  
                
                POCteltest = re.search('name="txtRAdminTel"(.*?)txtRAdminTel',driver.page_source, re.MULTILINE|re.IGNORECASE|re.DOTALL)
                POCteltest = POCteltest.group(1).strip().replace('\n','').replace('\r','')
                if 'value=' in POCteltest:
                    POCtel = re.search('name="txtRAdminTel"(.*?)value="(.*?)" maxlength',driver.page_source, re.MULTILINE|re.IGNORECASE|re.DOTALL)
                    facLinks.append(POCtel.group(2).strip().replace('\n','').replace('\r',''))
                else:
                    facLinks.append(' ')
                    
                POCstreet1__ = re.search('name="txtRAdminStr1"(.*?)txtRAdminStr1',driver.page_source, re.MULTILINE|re.IGNORECASE|re.DOTALL)
                POCstreet1__ = POCstreet1__.group(1).strip().replace('\n','').replace('\r','')
                if 'value=' in POCstreet1__:
                    POCstreet1 = re.search('name="txtRAdminStr1"(.*?)value="(.*?)" maxlength',driver.page_source, re.MULTILINE|re.IGNORECASE|re.DOTALL)
                    facLinks.append(POCstreet1.group(2).strip().replace('\n','').replace('\r',''))
                else:
                    facLinks.append(' ')
        
                POCpost1__ = re.search('name="txtRAdminPostalCodeBefore"(.*?)txtRAdminPostalCodeBefore',driver.page_source, re.MULTILINE|re.IGNORECASE|re.DOTALL)
                POCpost1__ = POCpost1__.group(1).strip().replace('\n','').replace('\r','')
                if 'value=' in POCpost1__:
                    POCpost1 = re.search('name="txtRAdminPostalCodeBefore"(.*?)value="(.*?)" maxlength',driver.page_source, re.MULTILINE|re.IGNORECASE|re.DOTALL)
                    facLinks.append(POCpost1.group(2).strip().replace('\n','').replace('\r',''))
                else:
                    facLinks.append(' ')
                    
                POCprovince__ = re.search('name="txtRAdminProvince"(.*?)txtRAdminProvince',driver.page_source, re.MULTILINE|re.IGNORECASE|re.DOTALL)
                POCprovince__ = POCprovince__.group(1).strip().replace('\n','').replace('\r','')
                if 'value=' in POCprovince__:
                    POCprovince = re.search('name="txtRAdminProvince"(.*?)value="(.*?)" maxlength',driver.page_source, re.MULTILINE|re.IGNORECASE|re.DOTALL)
                    facLinks.append(POCprovince.group(2).strip().replace('\n','').replace('\r',''))
                else:
                    facLinks.append(' ')
                    
                POCemail__ = re.search('name="txtRAdminEmail"(.*?)txtRAdminEmail',driver.page_source, re.MULTILINE|re.IGNORECASE|re.DOTALL)
                POCemail__ = POCemail__.group(1).strip().replace('\n','').replace('\r','')
                if 'value=' in POCemail__:
                    POCemail = re.search('name="txtRAdminEmail"(.*?)value="(.*?)" maxlength',driver.page_source, re.MULTILINE|re.IGNORECASE|re.DOTALL)
                    facLinks.append(POCemail.group(2).strip().replace('\n','').replace('\r',''))
                else:
                    facLinks.append(' ')                    
                    
                POCdirTitle__ = re.search('name="txtRAdminDirTitle"(.*?)txtRAdminDirTitle',driver.page_source, re.MULTILINE|re.IGNORECASE|re.DOTALL)
                POCdirTitle__ = POCdirTitle__.group(1).strip().replace('\n','').replace('\r','')
                if 'value=' in POCdirTitle__:
                    POCdirTitle = re.search('name="txtRAdminDirTitle"(.*?)value="(.*?)" maxlength',driver.page_source, re.MULTILINE|re.IGNORECASE|re.DOTALL)
                    facLinks.append(POCdirTitle.group(2).strip().replace('\n','').replace('\r',''))
                else:
                    facLinks.append(' ')
        
                POCstreet2__ = re.search('name="txtRAdminStr2"(.*?)txtRAdminStr2',driver.page_source, re.MULTILINE|re.IGNORECASE|re.DOTALL)
                POCstreet2__ = POCstreet2__.group(1).strip().replace('\n','').replace('\r','')
                if 'value=' in POCstreet2__:
                    POCstreet2 = re.search('name="txtRAdminStr2"(.*?)value="(.*?)" maxlength',driver.page_source, re.MULTILINE|re.IGNORECASE|re.DOTALL)
                    facLinks.append(POCstreet2.group(2).strip().replace('\n','').replace('\r',''))
                else:
                    facLinks.append(' ')                    
        
                POCcity__ = re.search('name="txtRAdminCity"(.*?)txtRAdminCity',driver.page_source, re.MULTILINE|re.IGNORECASE|re.DOTALL)
                POCcity__ = POCcity__.group(1).strip().replace('\n','').replace('\r','')
                if 'value=' in POCcity__:
                    POCcity = re.search('name="txtRAdminCity"(.*?)value="(.*?)" maxlength',driver.page_source, re.MULTILINE|re.IGNORECASE|re.DOTALL)
                    facLinks.append(POCcity.group(2).strip().replace('\n','').replace('\r',''))
                else:
                    facLinks.append(' ')
                    
                POCpost2__ = re.search('name="txtRAdminPostalCodeAfter"(.*?)txtRAdminPostalCodeAfter',driver.page_source, re.MULTILINE|re.IGNORECASE|re.DOTALL)
                POCpost2__ = POCpost2__.group(1).strip().replace('\n','').replace('\r','')
                if 'value=' in POCpost2__:
                    POCpost2 = re.search('name="txtRAdminPostalCodeAfter"(.*?)value="(.*?)" maxlength',driver.page_source, re.MULTILINE|re.IGNORECASE|re.DOTALL)
                    facLinks.append(POCpost2.group(2).strip().replace('\n','').replace('\r',''))
                else:
                    facLinks.append(' ')                    
        
        #staff hist cost
                Staffop__ = re.search('name="txtOperatorsTotal"(.*?)txtOperatorsTotal',driver.page_source, re.MULTILINE|re.IGNORECASE|re.DOTALL)
                Staffop__ = Staffop__.group(1).strip().replace('\n','').replace('\r','')
                if 'value=' in Staffop__:
                    Staffop = re.search('name="txtOperatorsTotal"(.*?)value="(.*?)" maxlength',driver.page_source, re.MULTILINE|re.IGNORECASE|re.DOTALL)
                    facLinks.append(Staffop.group(2).strip().replace('\n','').replace('\r',''))                    
                else:
                    facLinks.append(' ')                        
                
                Stafftot__ = re.search('name="txtStaffTotal"(.*?)txtStaffTotal',driver.page_source, re.MULTILINE|re.IGNORECASE|re.DOTALL)
                Stafftot__ = Stafftot__.group(1).strip().replace('\n','').replace('\r','')
                if 'value=' in Stafftot__:
                    Stafftot = re.search('name="txtStaffTotal"(.*?)value="(.*?)" maxlength',driver.page_source, re.MULTILINE|re.IGNORECASE|re.DOTALL)
                    facLinks.append(Stafftot.group(2).strip().replace('\n','').replace('\r',''))                    
                else:
                    facLinks.append(' ')
                    
                HistStrt_construc__ = re.search('name="txtConstructionDate"(.*?)txtConstructionDate',driver.page_source, re.MULTILINE|re.IGNORECASE|re.DOTALL)
                HistStrt_construc__ = HistStrt_construc__.group(1).strip().replace('\n','').replace('\r','')
                if 'value=' in HistStrt_construc__:
                    HistStrt_construc = re.search('name="txtConstructionDate"(.*?)value="(.*?)" maxlength',driver.page_source, re.MULTILINE|re.IGNORECASE|re.DOTALL)
                    facLinks.append(HistStrt_construc.group(2).strip().replace('\n','').replace('\r',''))                    
                else:
                    facLinks.append(' ')                   
                
                Hist1st_crit__ = re.search('name="txtCriticalityDate"(.*?)txtCriticalityDate',driver.page_source, re.MULTILINE|re.IGNORECASE|re.DOTALL)
                Hist1st_crit__ = Hist1st_crit__.group(1).strip().replace('\n','').replace('\r','')
                if 'value=' in Hist1st_crit__:
                    Hist1st_crit = re.search('name="txtCriticalityDate"(.*?)value="(.*?)" maxlength',driver.page_source, re.MULTILINE|re.IGNORECASE|re.DOTALL)
                    facLinks.append(Hist1st_crit.group(2).strip().replace('\n','').replace('\r',''))                    
                else:
                    facLinks.append(' ')
                    
                AnnualCost__ = re.search('name="txtAnnualCost"(.*?)txtAnnualCost',driver.page_source, re.MULTILINE|re.IGNORECASE|re.DOTALL)
                AnnualCost__ = AnnualCost__.group(1).strip().replace('\n','').replace('\r','')
                if 'value=' in AnnualCost__:
                    AnnualCost = re.search('name="txtAnnualCost"(.*?)value="(.*?)" maxlength',driver.page_source, re.MULTILINE|re.IGNORECASE|re.DOTALL)
                    facLinks.append(AnnualCost.group(2).strip().replace('\n','').replace('\r',''))                    
                else:
                    facLinks.append(' ')                       
                
                
                
                
        
                        
          
                facLinks.append(url)
                
                print i
                print facLinks
                
                with open(csvOutput, 'a') as output:
                    writer = csv.writer(output, lineterminator = '\n')
                    writer.writerows([facLinks])


