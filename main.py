# Requirments
# Python3
# chromedriver downloaded from selenium website
# chromedriver must be in the same folder as the script
# pip install

import time
import xml.etree.ElementTree as ET
import functions

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
    driver, compName, filing = functions.load13FRes(cik)

    # Wait for the page to load
    time.sleep(5)

    # Get the URL of the current page
    url = driver.current_url

    # Get the page source AKA html format
    data = driver.page_source

    # The rock is coooooooooooking
    res, links = functions.cookTheSoup(data)



    # We go for the first link since that's the most updated one
    functions.loadFirstDoc(links[0], driver)

    #This time out is a MUST, else xmlUrl would load the previous page url
    time.sleep(5)

    # Since the page is at the xml page now, we get the current url.
    xmlUrl = functions.loadXml(driver)

    # We read the content on the xml page given the url
    content = functions.readXml(xmlUrl)

    # Creat ElementTree
    root = ET.fromstring(content)

    time.sleep(5)

    # I need to write a function that creats file name.
    fileName = compName + '--' + filing + '--' + res[2] + '.txt'
    fNameLs = [compName, filing, res[2]]

    # Write the tsv file.
    functions.writeTsv(fileName, fNameLs, root)

    # Closer the webpage when finished.
    driver.quit()
