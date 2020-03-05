from sys import exit

from re import sub as regexReplace
from re import match as regexMatch

def getPageTable(pageSoup):
    return pageSoup.body.find('div', class_='body-content').find('table')

def getSongRows(pageTable):
    return [row for row in pageTable.find_all('tr')[1:]]

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

def checkColumnLabels(pageTable, expectedColumns):
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

