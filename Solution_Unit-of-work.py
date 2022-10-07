# P1. Create functions, set constants, import required libraries and set up, initialise browser and MS WORD
from Classes.User import User
import RPA1
import RPA2
import CSV_Import
import logging
from datetime import date
from time import process_time
import csv
import timeit

process_start = process_time()

# Initialise constants / objects / logging etc
TODAY_NUMERIC = date.today().strftime("%d%m%Y") # For unique filenames
TODAY_STRING = date.today().strftime("%d %B %Y") # For saving in document

logging.basicConfig(filename=f"log_{TODAY_NUMERIC}.txt", filemode="w", level=logging.INFO, format='%(asctime)s | %(name)s | %(levelname)s | %(message)s') # Setup logging for process
logging.info("Process Started")

wordApp = RPA2.startMSWord(True) # Creates PyWin32 MS Word Object - True/False dictate whether Word is visible.
driver = RPA1.startSelenium("Chrome") # Creates Selenium Object - use "Edge" or "Chrome" to get relevant browser.

RPA1.loginToSite(driver) # Navigate and login to site

csvPath = "testresults.csv"

# P2. CSV IMPORT - import usernames from CSV file, create a new user instance for each and save to userManager, ready to be iterated through later
userManager = CSV_Import.importCSVtoUserManager()

# P3. LOOP THROUGH USERS
with open(csvPath, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=['Test_Timing'])
    writer.writeheader()

    for user in userManager.users():
        user_process_start = timeit.default_timer()
        logging.info(f"--- RUNNING RPA PROCESSES FOR {user.returnUserName()} ---")
        # RPA1. CUSTOMER DATA RETRIEVAL
        updatedUser = RPA1.getUserDetails(driver=driver, user=user)
        if isinstance(updatedUser, User):
            user.updateUser(updatedUser) # If return from RPA1 is a valid user object then update userManager with retrieved details
            # RPA2. MS Word Doc Creation - only required if user found
            RPA2.createMSWordDocument(wordApp=wordApp, user=user, todaystring=TODAY_STRING, todaynumeric=TODAY_NUMERIC)
        #user_process_end = process_time()
        user_process_end = timeit.default_timer()
        logging.info(f"--- Total time running for {user.returnUserName()}: {user_process_end-user_process_start} seconds ---")
        rowData={'Test_Timing': user_process_end - user_process_start}
        writer.writerow(rowData)

# P5.Housekeeping
RPA2.closeMSWord(wordApp)
RPA1.closeSelenium(driver)

process_end = process_time()

logging.info(f"Process terminated. Total time running: {process_end-process_start} seconds")
