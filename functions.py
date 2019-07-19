from selenium import webdriver
import os

def loadPage(cik):
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
