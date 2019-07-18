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


if __name__ == '__main__':
    while 1:
        cik = input("Please Enter the CIK #: ")

        # Prevents invalid input
        try:
            int(cik)
            err = False
        except:
            print("Your CIK # is invalid")
            err = True

        if len(cik) != 10 or err is True:
            print("CIK # should contain 10 digits \n")
        else:
            break

    # finds the path of the current directory
    path = os.getcwd() + "/chromedriver"
    driver = webdriver.Chrome(executable_path = path)

    # Go to the EDGAR page
    driver.get("https://www.sec.gov/edgar/searchedgar/companysearch.html")

    # Put the CIK # in
    test = driver.find_element_by_id('cik').send_keys(cik)

    # Click on the search button
    driver.find_element_by_id('cik_find').click()

    driver.maximize_window()

    # find filter input to 13F format only
    driver.find_element_by_xpath('//*[@id="type"]').send_keys('13F')

    # Click search
    driver.find_element_by_xpath('//*[@id="contentDiv"]/div[2]/form/table/tbody/tr/td[6]/input[1]').click()


    time.sleep(5)

    # table_id = driver.find_element_by_id('seriesDiv')
    #
    # rows = table_id.find_elements_by_tag_name('tr')
    #
    # res = []
    # for row in rows:
    #     cells = row.find_elements_by_tag_name('td')
    #     for cell in cells:
    #        res.append(cell.text.strip())
    #
    # print(res)

    # For some reason I must maxmize the window or soup won't be able to read data
    driver.maximize_window()

    # Get the URL of the current page
    url = driver.current_url

    # Wait so the driver can locate the element
    driver.implicitly_wait(10)

    data = driver.page_source#.encode('utf-8').strip()


    soup = BeautifulSoup(data, features='xml')


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
                #print('--------------THIS IS EL:', el.text)
                if link:

                    #print('========THIS IS LINK:', link)
                    links.append(link['href'])
                res.append(temp)

        #cols = [ele.text.strip() for ele in cols]
        #res.append([ele for ele in cols if ele])
    #print(links)


    #To only go for the most recent, we can just focus on res[1] and links[0]
    #for some reason res[0] is this filter result text that i can't get rid of




    # Not sure will I be able to click on buttons instead

    nUrl = "https://www.sec.gov"+ links[0]


    # Need to wait for the driver is ready, else it will just close

    driver.get(nUrl)

    time.sleep(5)

    driver.find_element_by_xpath('//*[@id="formDiv"]/div/table/tbody/tr[3]/td[3]/a').click()



    #half way through doing this, I realized It prob would have been better to use request,
    #since in this case it's not necessary show the simluation, but just getting the data.
    # Since I'm too deep in, I would probably use Requests if I go back in time,
    # just because it keeps opening webpage, and this case would probably be more clean.

    xmlUrl = driver.current_url

    print(xmlUrl)
    file = urlopen(xmlUrl)

    content = file.read().decode("utf-8")
    file.close()

    print(content)

    root = ET.fromstring(content)

    time.sleep(5)


    print('\n')



    #print(root.tag)


    time.sleep(5)

    print('\n')
    #for child in root:
    #    print(child.tag, child.attrib)

    # Give the file a name and write to it.
    # fileName = 'test.txt'
    # outputF = open(fileName,'w')
    #
    # # Make it an .tsv file
    # writer = csv.writer(outputF, delimter='\t')

    #print(writer)

    driver.quit()
