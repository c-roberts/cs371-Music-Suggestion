from sys import exit

from bs4 import BeautifulSoup
from requests import get as getHTML


dataBaseSiteBaseURL = "https://www.music4dance.net/song"


# Make HTTP request
try:
    dataBaseSiteResponse = getHTML(dataBaseSiteBaseURL)
except:
    print("!! Error: Retrieving Music 4 Dance database unsuccessfull.")
    exit(0)
else:
    print("## Status: Retrieved Music 4 Dance database.")


# Parse HTML 
dataBaseSiteSoup = BeautifulSoup(dataBaseSiteResponse.text,
                                 features="html.parser"
                                )
def getPageTable(pageSoup):
    return pageSoup.body.find('div', class_='body-content').find('table')

pageSongTable = getPageTable(dataBaseSiteSoup)

def getColumnIndices(pageTable):
    indices = {}
    index = 0
    for colLabel in pageTable.thead.tr.find_all('th'):
        if 'title' in colLabel.attrs:
            title = colLabel.attrs['title'].split(':')[0]
            indices[title] = index
            print(index, title)
        else:
            print(index, "[no title]")
        index += 1
    return indices

def getSongRows(pageTable):
    return pageTable.find_all('tr')


# Print result
print(getSongRows(pageSongTable))

print(getColumnIndices(pageSongTable))
