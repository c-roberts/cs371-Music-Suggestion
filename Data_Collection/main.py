from sys import exit
from pprint import pprint
from os import path
from pickle import dump as pdump
from pickle import load as pload	

from bs4 import BeautifulSoup
from requests import get as getHTML

from re import sub as regexReplace
from re import match as regexMatch

dataBaseSiteBaseURL = "https://www.music4dance.net/song"
dataBaseSiteHTMLDumpPath = "site_HTML.pickle"

# In expected order
expectedColumns = ['Like/Play',
                   'Song Title',
                   'Artist',
                   'Tempo (in Beats Per Minute)',
                   'Strength of the beat',
                   'Energy of the song',
                   'Mood of the song',
                   'Dance Style Tags',
                   'Tags',
                   'Modified'
                  ]

if path.exists(dataBaseSiteHTMLDumpPath):
    print("## Status: Found cached copy of Music 4 Dance website.")
    dataBaseSiteHTML = pload(open(dataBaseSiteHTMLDumpPath, "rb"))
else:
    # Make HTTP request
    try:
        dataBaseSiteHTML = getHTML(dataBaseSiteBaseURL).text
    except:
        print("!! Error: Retrieving Music 4 Dance website unsuccessfull.")
        exit(0)
    else:
        print("## Status: Retrieved Music 4 Dance website.")

    # Save for later
    pdump(dataBaseSiteHTML, open(dataBaseSiteHTMLDumpPath, "wb"))
    print("## Status: Cached copy of Music 4 Dance website for later.")

# Parse HTML 
dataBaseSiteSoup = BeautifulSoup(dataBaseSiteHTML,
                                 features="html.parser"
                                )

# Get song table
def getPageTable(pageSoup):
    return pageSoup.body.find('div', class_='body-content').find('table')

def getSongRows(pageTable):
    return [row for row in pageTable.find_all('tr')[1:]]

pageSongTable = getPageTable(dataBaseSiteSoup)
songRows = getSongRows(pageSongTable)

# Parse table columns
def sanitizeColumnTitle(raw_title):
    title = raw_title.strip()
    title = title.split(':')[0]
    title = regexReplace("Click to sort by [\w ]+\.", "",
                         title
                        )
    title = regexReplace("\([\w ]+ icons represent [\w ]+\)\.", "",
                         title
                        )
    title = title.strip()
    return title

def checkColumnLabels(pageTable):
    foundColTitles = []
    for colLabel in pageTable.thead.tr.find_all('th'):
        if 'title' in colLabel.attrs:
            foundColTitles.append(sanitizeColumnTitle(colLabel.attrs['title']))
        else:
            title_text = sanitizeColumnTitle(colLabel.text)
            if title_text != '':
                foundColTitles.append(title_text)
            else:
                for img in colLabel.find_all('img'):
                    foundColTitles.append(sanitizeColumnTitle(img.attrs['title']))
    missing = []
    for colIndex in range(len(expectedColumns)):
        if expectedColumns[colIndex] != foundColTitles[colIndex]:
            missing.append(expectedColumns[colIndex])
               
    if len(missing):
        print("!! Error: Website table is missing the following expected labels:", missing)
        print("!!        Please update the data collection program to the new website format.")
        print("!!        Note that the expected label list must be correctly ordered.")
        exit(0)
    else:
        print("## Status: Found all expected website table column labels in expected order.")

checkColumnLabels(pageSongTable)

def songTitle(songRow):
    return songRow.find_all('td')[1].a.text

def songArtist(songRow):
    return songRow.find_all('td')[2].a.text

def songTempo(songRow):
    return int(songRow.find_all('td')[3].a.text)

def songBeatStrength(songRow):
    return float(regexMatch("This song has a beat strength of (\d{1,2}\.\d{1,2})",
                            songRow.find_all('td')[4]
                                   .find_all('a')[0]
                                   .img.attrs['title']
                           ).group(1)
                )

def songEnergy(songRow):
    return float(regexMatch("This song has an energy level of (\d{1,2}\.\d{1,2})",
                            songRow.find_all('td')[4]
                                   .find_all('a')[1]
                                   .img.attrs['title']
                           ).group(1)
                )

def songMood(songRow):
    return float(regexMatch("This song has a mood level of (\d{1,2}\.\d{1,2})",
                            songRow.find_all('td')[4]
                                   .find_all('a')[2]
                                   .img.attrs['title']
                           ).group(1)
                )

def songDanceStyles(songRow):
    styles = []
    for a in songRow.find_all('td')[5].select("a[data-dance-name]"):
        if a.attrs['data-dance-name']:
            styles.append(a.attrs['data-dance-name'])
    return styles

def songTags(songRow):
    tags = []
    for a in songRow.find_all('td')[6].select("a[data-tag-value]"):
        if a.attrs['data-tag-value']:
            tags.append(a.attrs['data-tag-value'])
    return tags

print(songTitle(songRows[0]))
print(songArtist(songRows[0]))
print(songTempo(songRows[0]))
print(songBeatStrength(songRows[0]))
print(songEnergy(songRows[0]))
print(songMood(songRows[0]))
print(songDanceStyles(songRows[0]))
print(songDanceStyles(songRows[-5]))
print(songTags(songRows[1]))
