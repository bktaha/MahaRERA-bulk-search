import logging
import requests
import bs4
from datetime import datetime
from fuzzywuzzy import fuzz

class MahaSearch:
    def __init__(self):
        self.msession = requests.Session()
        self.state = 27
        self.division = 6
        self.locality = {
            'District': ''
        }
        self.initiated = datetime.now()
        self.dateformat = '%d/%m/%Y'

    def dictifySearchResults(self, allResults):
        dictified = []
        prjList = allResults['projects']
        prjLinks = allResults['prjlinks']
        prjPromoters = allResults['promoters']
        prjModifiedDate = allResults['lastModifiedDates']
        for counter in range(len(prjList)):
            mDict = {}
            mDict['_value_'] = prjList[counter].string
            mDict['_rlink_'] = prjLinks[counter]['href']
            mDict['_mprom_'] = prjPromoters[counter].string
            mDict['_mdate_'] = datetime.strptime(prjModifiedDate[counter].string, self.dateformat).isoformat()
            dictified.append(mDict)
        return dictified
    
    def searchResults(self, projectName, promoterName='', includeScores=True, includeHighest=False, comparator=None):
        raws = self.msession.post('https://maharerait.mahaonline.gov.in/SearchList/Search', verify=False, data={
            'Type':'Promoter',
            'ID':0,
            'pageTraverse':1,
            'Project':projectName,
            'Promoter':promoterName,
            'State':self.state,
            'Division':self.division,
            'District':self.locality['District'],
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
        
        try:
            properName = comparator['properName']
            label = comparator['label']
        except:
            properName = projectName
            label = '_value_'
        
        finResults = self.dictifySearchResults(allResults) if len(projects) else None
        scoredResults = self.getNameComparisonScores(finResults, properName, label) if includeScores else finResults
        filteredScores = self.selectHighestScore(scoredResults) if includeHighest else scoredResults
        return filteredScores
    
    def getNameComparisonScores(self, dictified, properName, label):
        newDictified = dictified
        for mresult in newDictified:
            mresult['score'] = fuzz.token_set_ratio(mresult[label], properName)
        return newDictified
    
    def selectHighestScore(self, dictified):
        try:
            allScores = [mresult['score'] for mresult in dictified]
            filterDict = [mresult for mresult in dictified if mresult['score'] == max(allScores)]
            return filterDict
        except:
            return dictified