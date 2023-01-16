# -*- coding: utf-8 -*-
"""
Extracting AFDs and sorting by time
"""
import re
import os
from datetime import datetime
#import numpy as np
#import pandas as pd

# https://mesonet.agron.iastate.edu/wx/afos/old.phtml
# https://mesonet.agron.iastate.edu/wx/afos/#AFDGRR-200

#url = "https://mesowest.utah.edu/cgi-bin/droman/meso_table_mesodyn.cgi?stn=MC093&unit=0&time=LOCAL&year1=&month1=&day1=0&hour1=00&hours=24&past=0&order=1"
#url = "https://kamala.cod.edu/mi/latest.fxus63.KGRR.html"
#url = "https://forecast.weather.gov/product.php?site=GRR&issuedby=GRR&product=AFD&format=ci&version=1&glossary=0"

def hrFix(h,ap):
    if len(str(h)) > 4:
        return 0
    if h == 12:
        if ap == 'AM':
            return 0
        else:
            return 12
    if ap == 'AM':
        return h
    else:
        return h + 12
    
def issueTime(section,sec):
    S = 0
    reg = re.compile('\d\d\d.*\s20\d\d')
    m = re.search(reg, section)
    dateStr = m.group(0)
    #print (dateStr)
    #dateStr = '300 AM EST Mon Mar 4 2019'
    timeSec = dateStr.split(' ')
    HM = str(timeSec[0])
    if len(HM) < 5:
        Htemp = int(HM[0:-2])
        M = int(HM[-2:])
        ap = timeSec[1]
        #print(ap)
        H = hrFix(Htemp,ap)
    else:
        M = 0
        H = 0
    yr = int(timeSec[-1])  #YYYY
    mon = int(monDict[timeSec[-3]])
    date = int(timeSec[-2])
    dt = datetime(yr,mon,date,H,M,S)
    dtStr = datetime.strftime(dt, "%Y%m%d%H%M%S")
    return dtStr,dt

def cleanText(srcFile,dstFile):
    stripped = lambda s: "".join(i for i in s if 31 < ord(i) < 127)
    dst = open(dstFile, 'w')
    infile = open(srcFile, 'r')
    for lines in infile.readlines():
        fixed = stripped(str(lines))
        dst.write(fixed + '\n')
    dst.close()
    infile.close()

def identifyFcstr(fcstrSec):
    dictFcstrs = {}
    mets = fcstrSec.split('\n')
    for metName in range(0,len(mets)):
        fcstLine = mets[metName]
        ids = fcstLine.split('...')
        if len(ids) > 1:
            dictFcstrs[ids[0]] = ids[1]
    if 'SHORT TERM' in dictFcstrs:
        dictFcstrs['DISCUSSION'] = 'NA'
    return dictFcstrs



from bs4 import BeautifulSoup
import requests

for version in range(1,50):
    if version < 10:
        verStr = "0" + str(version)
    else:
        verStr = str(version)
    
    url = "https://forecast.weather.gov/product.php?site=GRR&issuedby=GRR&product=AFD&format=ci&version=" + str(version) + "&glossary=0"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    nws = soup.pre
    nwsStr = nws.string
#section_lines = [line for line in nwsStr.split('\n') if "DISCUSSION" in line]
#print section_lines
    sections = nws.string.split("&&")

fnum = {'04': 'Felver', 'MJS': 'Sekelsky', 'TJT': 'Turnage', 'Borchardt': 'Borchardt',
        'Ostuno': 'Ostuno' }

base_dir = 'C:/data'
srcFile = 'afos2.txt'
fixedFile = 'fixed2.txt'
srcFile = os.path.join(base_dir,'afos2.txt')
fixedFile = os.path.join(base_dir,'afos2.txt')
cleanText(srcFile, fixedFile)
separator = '  ----------------------  '
masterList = []

monDict =  {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}

if 2 > 1:
    again = open(fixedFile, 'r')
    data_read = again.read()
    dataStr = str(data_read)
    afds = dataStr.split('AFDGRR')
    for a in range(0,len(afds)):
        thisAFD = afds[a]
        getfids = thisAFD.split("$$")
        if len(getfids) > 0:
            fids = getfids[-1]
            fdict = identifyFcstr(fids)
            justAFD = getfids[0]
            getSecs = thisAFD.split("&&")
            for sec in range(0,len(getSecs)):
                s = getSecs[sec]
                if len(getSecs[sec]) > 0:  
                    if re.compile("\.UPDATE...").search(s,1):
                        tStr, tObj = issueTime(s,0)
                        secType = '4-update'
                        fcstr = fdict['UPDATE']
                        masterList.append([tStr,secType,fcstr,s])
                    elif re.compile("\.DISCUSSION...").search(s,1):
                        tStr, tObj = issueTime(s,45)
                        secType = '2-discussion'
                        fcstr = fdict['DISCUSSION']
                        masterList.append([tStr,secType,fcstr,s])
                    elif re.compile("\.AVIATION...").search(s,1):
                        tStr, tObj = issueTime(s,0)
                        secType = '3-aviation'
                        fcstr = fdict['AVIATION']      
                        masterList.append([tStr,secType,fcstr,s])
                    elif re.compile("Synopsis").search(s,1):
                        tStr, tObj = issueTime(s,0)
                        justSyn = s.split('.SYNOPSIS...')
                        s = '\n\n.SYNOPSIS...\n' + justSyn[1]
                        secType = '1-synopsis'
                        fcstr = fdict['SYNOPSIS']
                        masterList.append([tStr,secType,fcstr,s])
                    else:
                        pass

    uniqueList = []
    finalList = []
    
    # eliminate duplicates
    for i in range(0,len(masterList)):
        sample = masterList[i]
        check = sample[0] + sample[1]
        #print (check)
        if check not in uniqueList:
            uniqueList.append(check)
            finalList.append(sample)
        else:
            pass
                                
    d = sorted(finalList, reverse=True)


    #da = np.array(d)
    #dts = da[:,0]
    #dsecType, dfcstr, dtext = da[:,-3], da[:,-2], da[:,-1]
    #D = pd.DataFrame({'type':dsecType, 'fid':dfcstr, 'text':dtext}, index=dts)   
    #selector = ((D.index.month == 2) & (D.fid == 'WDM'))
    complete2 = os.path.join(base_dir,'complete2.txt')
    complete = open(complete2, 'w')
    for j in range(0,len(d)):
        thisText = d[j]
        times = str(thisText[0])
        secType = str(thisText[1])        
        fcstr = str(thisText[2])
        text = str(thisText[3])

        if (secType != '3-aviation') and (secType != '1-synopsis'):
            justThese = "   " + separator + fcstr + separator + text
            complete.write(justThese)
    
complete.close()