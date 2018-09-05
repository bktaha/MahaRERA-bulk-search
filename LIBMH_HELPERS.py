import logging
import requests
import bs4

import LIB_LOGCFG as liblog

liblog.setup_logging()

'''
POST Form Data
State: Maharashtra
Division: Konkan
'''
'''
Type:Promoter
ID:0
pageTraverse:1
Project:
Promoter:
CertiNo:
State:27
Division:6
District:
Taluka:
Village:
CompletionDate_From:
CompletionDate_To:
PType:
btnSearch:Search
'''
global lnone

lnone = {
    'District': ''
}

def dictifySearchResults(allResults):
    dictified = []
    prjList = allResults['projects']
    prjLinks = allResults['prjlinks']
    prjPromoters = allResults['promoters']
    prjModifiedDate = allResults['lastModifiedDates']
    for counter in range(len(prjList)):
        mDict = {}
        mDict['_value_'+str(counter)] = prjList[counter].string
        mDict['_rlink_'+str(counter)] = prjLinks[counter]['href']
        mDict['_mprom_'+str(counter)] = prjPromoters[counter]
        mDict['_mdate_'+str(counter)] = prjModifiedDate[counter]
        dictified.append(mDict)
    return dictified

def searchResults(projectName, promoterName='', state=27, division=6, locality=lnone):
    raws = requests.post('https://maharerait.mahaonline.gov.in/SearchList/Search', verify=False, data={
        'Type':'Promoter',
        'ID':0,
        'pageTraverse':1,
        'Project':projectName,
        'Promoter':promoterName,
        'State':state,
        'Division':division,
        'District':locality['District'],
        'btnSearch':'Search'
    })
    raws.raise_for_status()
    misalSoup = bs4.BeautifulSoup(raws.text, 'html.parser')
    # totalRecords = misalSoup.select('input[name="TotalRecords"]')[0]['value']
    projects = misalSoup.select('td[data-name="Project"]')
    promoters = misalSoup.select('td[data-name="Name"]')
    prjlinks = misalSoup.select('td > a[target="_blank"]')
    lastModifiedDates = misalSoup.select('td[data-name="lastModifiedDate"]')
    allResults = {
        'projects': projects,
        'promoters': promoters,
        'prjlinks': prjlinks,
        'lastModifiedDates': lastModifiedDates
    }
    logging.info(allResults)
    return dictifySearchResults(allResults) if len(projects) else None