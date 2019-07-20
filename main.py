# Requirments
# Python3
# chromedriver downloaded from selenium website
# chromedriver must be in the same folder as the script
# pip install

import time
import xml.etree.ElementTree as ET
import functions
import sys
import os

if __name__ == '__main__':

    # Going try to install the modules for the user
    try:
        functions.install('selenium')
        functions.install('BeautifulSoup4')
        functions.install('urllib3')
    except:
        print("Oops, sorry you might have to pip install manually")

    print('\n')


    while 1:
        print("Enter exit to leave...\n")

        cik = input("Please Enter the CIK #: ")

        if cik.lower() == 'exit':
            sys.exit()

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

        # Clear the input buffer, so if the previous try is invalid, it doesn't carry over.
        os.system('clear')

    # This will be able to look at previous documents
    while 1:
        ith = input("Please enter the i-th most recent document you want to review, i: ")

        if ith.lower() == 'exit':
            sys.exit()

        try:
            int(ith)
            err = False
        except:
            print("Invalid input.")
            err = True
        if err == False and int(ith) > 0:
            break

        # Clear the input buffer, so if the previous try is invalid, it doesn't carry over.
        os.system('clear')
        
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
    try:
        xmlUrl = functions.loadXml(driver)
    except:
        print("Company document doesn't not contain a information table.")
        sys.exit()

    # We read the content on the xml page given the url
    content = functions.readXml(xmlUrl)

    # Creat ElementTree
    root = ET.fromstring(content)

    time.sleep(5)

    idx = [i for i in range(2,len(res), 3)]


    #idx = [i+3 for i in range(2, len(res))]
    print(idx)

    # I need to write a function that creats file name.
    fileName = compName + '--' + filing + '--' + res[idx[int(ith)-1]] + '.txt'
    fNameLs = [compName, filing, res[idx[int(ith)-1]]]

    # Write the tsv file.
    functions.writeTsv(fileName, fNameLs, root)

    # Closer the webpage when finished.
    driver.quit()
