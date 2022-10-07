# RPA2: Code required for Selenium Data Retrieval
import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from Classes.User import User
import logging

MAIN_WEBSITE_URL = os.environ["mainWebsiteURL"]
ADMIN_PAGE_URL = os.environ["websiteAdminURL"]
USERNAME = os.environ["username"]
PASSWORD = os.environ['sitePassword']
log = logging.getLogger(__name__)

def startSelenium(browser):
    log.info("SELENIUM: Creating instance")
    try:
        s = Service("C:\Program Files\ChromeDriver\chromedriver.exe")
        n = Service("C:\Program Files\ChromeDriver\msedgedriver.exe")
        if browser == "Chrome":
            driver = webdriver.Chrome(service=s) #For Chrome
        elif browser == "Edge":
            driver = webdriver.Edge(service=n)  # For Edge
        log.info("SELENIUM: Successfully created instance.")
    except:
        log.critical("SELENIUM: Problem encountered creating instance")
        return
    else:
        return driver

def loginToSite(driver):
    # Code to login to site.
    try:
        driver.get(MAIN_WEBSITE_URL)
        driver.find_element(By.XPATH, "/html/body/div/div[2]/div/form/div/div[1]/div[2]/input").send_keys(USERNAME)
        driver.find_element(By.XPATH, "/html/body/div/div[2]/div/form/div/div[2]/div[2]/input").send_keys(PASSWORD)
        driver.find_element(By.XPATH, "/html/body/div/div[2]/div/form/div/div[3]/button").click()
        driver.get(ADMIN_PAGE_URL)
        driver.find_element(By.XPATH, "/html/body/div/div[2]/div[2]/div[2]/div[1]/p[2]/a").click()  # Go to user search page
        log.info("SELENIUM: Successfully logged into target site")
    except:
        log.error("SELENIUM: Unable to log into target site")

def getUserDetails(driver, user):
    userName = user.returnUserName()
    log.info("SELENIUM: Searching for user.")
    driver.find_element(By.XPATH, "/html/body/div/div[2]/div[2]/div[2]/form/div/div[2]/div[1]/input").send_keys(userName)  # Enter username
    driver.find_element(By.XPATH, "/html/body/div/div[2]/div[2]/div[2]/form/div/div[2]/button").click()  # Click search

    # Handle user not found
    resultTable = driver.find_element(By.CLASS_NAME, "user-table").find_element(By.CSS_SELECTOR, "tbody")
    for row in resultTable.find_elements(By.CSS_SELECTOR, "tr"):
        if row.find_elements(By.CSS_SELECTOR, "td")[0].text == "No Search Results Found.":
            # If no user found return a null value
            log.error("SELENIUM: User not found.")
            driver.get(ADMIN_PAGE_URL)
            driver.find_element(By.XPATH,"/html/body/div/div[2]/div[2]/div[2]/div[1]/p[2]/a").click()  # Go to user search page
            return ""
        else:
            # User found - go to their profile
            row.find_elements(By.CSS_SELECTOR, "td")[9].find_element(By.CSS_SELECTOR,"a").click()  # Click to go to user profile
            break
    firstName = driver.find_element(By.XPATH, "//*[@id='editUserForm']/div[3]/div[2]/input").get_attribute('value')
    lastName = driver.find_element(By.XPATH, "/html/body/div/div[2]/div[2]/div[2]/form/div[4]/div[2]/input").get_attribute('value')
    address1 = driver.find_element(By.XPATH, "/html/body/div/div[2]/div[2]/div[2]/form/div[7]/div[2]/input").get_attribute('value')
    address2 = driver.find_element(By.XPATH, "/html/body/div/div[2]/div[2]/div[2]/form/div[8]/div[2]/input").get_attribute('value')
    town = driver.find_element(By.XPATH, "/html/body/div/div[2]/div[2]/div[2]/form/div[9]/div[2]/input").get_attribute('value')
    county = driver.find_element(By.XPATH, "/html/body/div/div[2]/div[2]/div[2]/form/div[11]/div[2]/input").get_attribute('value')
    postcode = driver.find_element(By.XPATH, "/html/body/div/div[2]/div[2]/div[2]/form/div[12]/div[2]/input").get_attribute('value')
    updatedUser = User(username=userName, firstName=firstName, lastName=lastName, address1=address1, address2=address2, town=town, county=county, postcode=postcode)
    driver.get(ADMIN_PAGE_URL) #Return to admin page, ready for next process.
    driver.find_element(By.XPATH, "/html/body/div/div[2]/div[2]/div[2]/div[1]/p[2]/a").click()  # Go to user search page
    log.info("SELENIUM: User details found.")
    return updatedUser


def closeSelenium(driver):
    driver.find_element(By.XPATH, "/html/body/div/div[2]/div[1]/div[2]/a").click() #Logout of site
    driver.quit() #Use quit instead of close otherwise the drive remains open and may impact efficiency?
    log.info("SELENIUM: Closing instance")