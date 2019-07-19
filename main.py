# Requirments
# Python3
# chromedriver downloaded from selenium website
# chromedriver must be in the same folder as the script
# pip install

from selenium import webdriver
import os
from bs4 import BeautifulSoup
import time
from urllib.request import urlopen
import requests
import xml.etree.ElementTree as ET
import csv
import functions
#from xlsxwriter.workbook import Workbook

if __name__ == '__main__':
    while 1:
        cik = input("Please Enter the CIK #: ")

        # Prevents invalid input
        try:
            # If input isn't a combination of numbers
            int(cik)
            err = False
        except:
            print("Your CIK # is invalid")
            err = True

        # If length of cik is invalid or input isn't numbers, make sure no extra space.
        if len(cik) != 10 or err is True:
            print("CIK # should contain 10 digits \n")
        else:
            break

    # Callig loadPage with Selenium from functions.py
    driver = functions.loadPage(cik)

    # Wait for the page to load
    time.sleep(5)

    # Get the URL of the current page
    url = driver.current_url

    # Get the page source AKA html format
    data = driver.page_source

    # The rock is coooooooooooking
    res, links = functions.cookTheSoup(data)

    #To only go for the most recent, we can just focus on res[1] and links[0]
    #for some reason res[0] is this filter result text that i can't get rid of



    # We go for the first link since that's the most updated one
    nUrl = "https://www.sec.gov"+ links[0]


    driver.get(nUrl)

    time.sleep(5)

    driver.find_element_by_xpath('//*[@id="formDiv"]/div/table/tbody/tr[5]/td[3]/a').click()

    #This time out is a MUST, else xmlUrl would load the previous page url
    time.sleep(5)

    #half way through doing this, I realized It prob would have been better to use request,
    #since in this case it's not necessary show the simluation, but just getting the data.
    # Since I'm too deep in, I would probably use Requests if I go back in time,
    # just because it keeps opening webpage, and this case would probably be more clean.

    xmlUrl = driver.current_url

    # Seems like my xmlUrl has issues that are causing the tree to not work

    #content = requests.get('https://www.sec.gov/Archives/edgar/data/1166559/000110465919029714/primary_doc.xml')
    #ontent = requests.get(xmlUrl)

    file = urlopen(xmlUrl)

    content = file.read().decode("utf-8")
    file.close()



    root = ET.fromstring(content) # If you use requests you do content.text

    time.sleep(5)

    print(root)

    numOfComp = 0
    for child in root:
        numOfComp+=1

    print(numOfComp)

    colNames = []
    for child in root[0]:
        colNames.append(child.tag.replace('{http://www.sec.gov/edgar/document/thirteenf/informationtable}', ''))
        for gChild in child:
            colNames.append(gChild.tag.replace('{http://www.sec.gov/edgar/document/thirteenf/informationtable}', ''))

    print(colNames)


    print('\n')

    #print(content)


    time.sleep(5)

    print('\n')
    #for child in root:
    #    print(child.tag, child.attrib)

    # Give the file a name and write to it.
    fileName = 'test.txt'
    outputF = open(fileName,'w')

    # # Make it an .tsv file
    tsvWriter = csv.writer(outputF, delimiter='\t')
    tsvWriter.writerow(colNames)

    # In text file
    for i in range(numOfComp):
        text = []
        for child in root[i]:
            # To change newline into ''
            d1 = child.text.strip()
            # Not include ''
            if d1 is not '':
                text.append(d1)
            for gChild in child:
                d2 = gChild.text.strip()
                if d2 is not '':
                    text.append(d2)

        tsvWriter.writerow(text)

    # # import into excelsheet, becuase tsv file format looks kinda bad, and I tried fixing it.
    # tsvFile = fileName
    # xslFile = 'test.xlsx'

    # # Create xlsx workbook
    # workbook = Workbook(xslFile)
    # worksheet = workbook.add_worksheet()
    #
    # tsvRead = csv.reader(open(tsvFile, 'rt'), delimiter = '\t')
    #
    # for f in colNames:
    #     for i in range(numOfComp):
    #         worksheet.write_column(i, f, tsvRead)



    driver.quit()
