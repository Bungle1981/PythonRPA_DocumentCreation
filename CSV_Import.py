import csv
from Classes.User import User
from Classes.UserManager import UserManager
import logging

log = logging.getLogger(__name__)

def importCSVtoUserManager():
    log.info("CSV FILE: Importing.")
    tempUserManager = UserManager()
    try:
        with open("usersShortList.csv", mode="r") as datafile:
            data = csv.reader(datafile)
            for row in data:
                if row[1] != "user_name": # Ignore header if necessary
                    newUser = User(username=row[1])
                    tempUserManager.addUser(newUser)
            log.info("CSV FILE: Successfully imported.")
    except:
        log.critical("CSV FILE: Problem importing.")
    finally:
        return tempUserManager