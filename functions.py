from selenium import webdriver
from bs4 import BeautifulSoup
import os
from urllib.request import urlopen
import time

def loadCompRes(cik):
    # Locate where chromedriver is in the directory
    path = os.getcwd() + "/chromedriver"

    # Find and start the webdriver
    driver = webdriver.Chrome(executable_path = path)

    # Go to the EDGAR page
    driver.get("https://www.sec.gov/edgar/searchedgar/companysearch.html")

    # Put the CIK # in
    test = driver.find_element_by_id('cik').send_keys(cik)

    # Click on the search button
    driver.find_element_by_id('cik_find').click()

    # Sometimes it can cause reading errors if the window isn't maxmize
    driver.maximize_window()

    # Find filter input to 13F format only
    driver.find_element_by_xpath('//*[@id="type"]').send_keys('13F')

    # Click search for 13F format
    driver.find_element_by_xpath('//*[@id="contentDiv"]/div[2]/form/table/tbody/tr/td[6]/input[1]').click()

    # return the driver
    return driver

def cookTheSoup(data):
    # Creat the soup given the page data as xml format.
    soup = BeautifulSoup(data, features='xml')

    # Locate the table
    table = soup.find('table', {'class':'tableFile2'})


    table_body = table.find('tbody')

    rows = soup.find_all('tr')

    res = []
    links = []
    # This can be its own function
    for row in rows:
        cols = row.find_all('td', text=True)
        temp = []
        for el in cols:

            #need the strip to make them more orgainzed
            temp.append(el.text.strip())
            if el:
                link = el.find('a', href = True)
                if link:
                    links.append(link['href'])
                res.append(temp)

    return res, links

def loadFirstDoc(link, driver):
    # We go for the first link since that's the most updated one
    nUrl = "https://www.sec.gov"+ link

    driver.get(nUrl)

def loadXml(driver):
    # Find the button to click on after you in the Documents
    driver.find_element_by_xpath('//*[@id="formDiv"]/div/table/tbody/tr[5]/td[3]/a').click()

    # Gotta wait to get the current url, let the page load to xml first.
    time.sleep(5)

    xmlUrl = driver.current_url

    return xmlUrl

def readXml(xmlUrl):

    file = urlopen(xmlUrl)

    # Decode the data from bytes to string
    content = file.read().decode("utf-8")

    file.close()

    return content

def countNumOfComp(root):
    numOfComp = 0
    for child in root:
        numOfComp+=1

    return numOfComp

def getColNames(root):
    colNames = []
    for child in root[0]:
        colNames.append(child.tag.replace('{http://www.sec.gov/edgar/document/thirteenf/informationtable}', ''))
        for gChild in child:
            colNames.append(gChild.tag.replace('{http://www.sec.gov/edgar/document/thirteenf/informationtable}', ''))

    # Returns a list of column names
    return colNames
