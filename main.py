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
    driver = functions.loadCompRes(cik)

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
    functions.loadFirstDoc(links[0], driver)

    #This time out is a MUST, else xmlUrl would load the previous page url
    time.sleep(5)

    # Since the page is at the xml page now, we get the current url.
    xmlUrl = functions.loadXml(driver)

    print(xmlUrl)

    # We read the content on the xml page given the url
    content = functions.readXml(xmlUrl)

    # Creat ElementTree
    root = ET.fromstring(content)

    time.sleep(5)

    numOfComp = functions.countNumOfComp(root)

    colNames = functions.getColNames(root)

    time.sleep(5)

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
