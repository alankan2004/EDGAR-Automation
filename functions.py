from selenium import webdriver
from bs4 import BeautifulSoup
import os
from urllib.request import urlopen
import time
import csv
try:
    from pip import main as pipmain
except:
    from pip._internal import main as pipmain

def install(package):
    # Installs the modules
    if hasattr(pipmain, 'main'):
        pipmain(['install', package])
    else:
        pipmain(['install', package])

def load13FRes(cik):
    # This function loads the page to the company 13F documents given a cik.

    # Locate where chromedriver is in the directory
    path = os.getcwd() + "/chromedriver"

    # Find and start the webdriver
    driver = webdriver.Chrome(executable_path = path)

    # Go to the EDGAR page
    driver.get("https://www.sec.gov/edgar/searchedgar/companysearch.html")

    # Put the CIK # in
    driver.find_element_by_id('cik').send_keys(cik)

    # Click on the search button
    driver.find_element_by_id('cik_find').click()

    # Sometimes it can cause reading errors if the window isn't maxmize
    driver.maximize_window()

    compName = driver.find_element_by_class_name('companyName').text

    idx = compName.index('CIK')

    # Get rid of uncessary contents
    compName = compName[:idx].strip()

    filing = '13F'

    # Find filter input to 13F filing only
    driver.find_element_by_xpath('//*[@id="type"]').send_keys(filing)

    # Click search for 13F format
    driver.find_element_by_xpath('//*[@id="contentDiv"]/div[2]/form/table/tbody/tr/td[6]/input[1]').click()

    # return the driver
    return driver, compName, filing

def cookTheSoup(data):
    # Creat the soup given the page data as xml format.
    soup = BeautifulSoup(data, features='xml')

    # Locate the table that have all the documents
    table = soup.find('table', {'class':'tableFile2'})

    # Find the table body
    table_body = table.find('tbody')

    # Find all the rows under the table
    rows = table_body.find_all('tr')

    # res is list of lists of each row's filing type and data recorded. EX: [13F, Documents, 2015-5-12].
    res = []
    # links is a list of each of the row's document url, can be access by index
    links = []

    # For some reason, the row in rows are super repetative, so I'm getting the same data over and over again.
    for row in rows:
        # Text = True to output text, find all the values in that row, under each column.
        cols = row.find_all('td', text=True)
        temp = []
        linkTemp =[]
        for el in cols:

            # If el is not None, which I don't understand why it would be None, but it happens.
            if el:
                temp.append(el.text.strip())
                # Look for the link, specifically the one with the correct id, so I don'tg et the wrong link for url.
                # Set href = True, so those links are shown.
                link = el.find('a', id = 'documentsbutton', href = True)

                # If link is not None.
                if link:
                    linkTemp.append(link['href'])
                res.append(temp)
                links.append(linkTemp)

    # So I only return the first list in res and links because the rest of the lists in res and links are redundant.
    # But I can't figure out why it's going through extra data.
    # res[0] and links[0] do include most recent and previous dates and links(well up to 40).
    return res[0], links[0]

def loadDoc(link, driver):
    # link is which ever one asked
    nUrl = "https://www.sec.gov"+ link

    # Return that url for webdriver to load
    driver.get(nUrl)

def loadXml(driver):
    # Find the button to click on after you in the Documents
    driver.find_element_by_xpath('//*[@id="formDiv"]/div/table/tbody/tr[5]/td[3]/a').click()

    # Gotta wait to get the current url, let the page load to xml first.
    time.sleep(5)

    xmlUrl = driver.current_url

    return xmlUrl

def readXml(xmlUrl):

    # Open the page where the infoTable.xml is.
    file = urlopen(xmlUrl)

    # Decode the data from bytes to string
    content = file.read().decode("utf-8")

    # Close the file when done reading.
    file.close()

    return content

def countNumOfComp(root):
    numOfComp = 0
    # Count number of companies, which is the child tags under the root tag.
    for child in root:
        numOfComp+=1

    return numOfComp

def getColNames(root, numOfComp):
    colNames = []

    # I'm going to attemp to use hashTable instead
    for i in range(numOfComp):
        d = {}
        for child in root[i]:
            # Clean up the tag name, becuase the column names have this link in front of them.
            tag = child.tag.replace('{http://www.sec.gov/edgar/document/thirteenf/informationtable}', '')
            if tag not in d:
                # Just signing the values to True for no reason.
                d[tag] = True
            for gChild in child:
                # Clean up the tag name, becuase the column names have this link in front of them.
                subTag = gChild.tag.replace('{http://www.sec.gov/edgar/document/thirteenf/informationtable}', '')

                # I'm just going to let it rewrite here, because I want to link the tag and subtag together,
                # So tags that have subtags will have a value of a list.
                if d[tag] is True:
                    d[tag] = [subTag]
                else:
                    d[tag].append(subTag)

    # Trying to group the tag and the sub-tags together.
    for key in d:
        temp = []
        if d[key] is not True:
            temp.append(key + ':')
            for val in d[key]:
                temp.append(val)
            colNames.append(tuple(temp))
        else:
            colNames.append(key)

    # Returns a list of column names
    return colNames

def writeTsv(fileName, fNameLs, root):
    numOfComp = countNumOfComp(root)
    colNames = getColNames(root, numOfComp)

    outputF = open(fileName,'w')

    # Make it an .tsv file
    tsvWriter = csv.writer(outputF, delimiter='\t')

    # Write the comp name, filling type and the data at the top.
    tsvWriter.writerow(fNameLs)

    # Writing the column names
    tsvWriter.writerow(colNames)

    # Write content under tags and content under sub-tags to tsv file.
    for i in range(numOfComp):
        text = []
        for child in root[i]:

            if child.text is None:
                # To change newline into ''
                d1 = child.text
            else:
                d1 = child.text.strip()
                # Not include ''
                if d1 is not '':
                    text.append(d1)
            for gChild in child:
                d2 = gChild.text.strip()
                if d2 is not '':
                    text.append(d2)

        tsvWriter.writerow(text)
