# RPA2: Code required for MS Word Document Creation Processes
import win32com.client as win32
import logging

log = logging.getLogger(__name__)
TEMPLATE_FILEPATH = "D:\Education\Computer Science (Uni of Staffordshire)\Dissertation\Letter Template\Letter Template.dotx"
OUTPUT_FILEPATH = "D:\Education\Computer Science (Uni of Staffordshire)\Dissertation\Letter Output"

def startMSWord(visible):
    wordApp = None
    log.info("MS WORD: Creating instance")
    try:
        # wordApp = win32.gencache.EnsureDispatch('Word.Application')  # Creates a new MS Word application
        wordApp = win32.Dispatch('Word.Application')  # Creates a new MS Word application
        wordApp.Visible = visible
        log.info("MS WORD: Successfully created instance.")
    except:
        log.critical("MS WORD: Problem encountered creating MS Word")
        return
    else:
        return wordApp

def createMSWordDocument(wordApp, user, todaynumeric, todaystring):
    username = user.returnUserName()
    firstname = user.returnFirstName()
    lastname = user.returnLastName()
    address = user.returnAddressBlock()
    savepath = f"{OUTPUT_FILEPATH}\{username}_{todaynumeric}.doc"
    log.info("MS WORD: Creating document.")
    try:
        doc = wordApp.Documents.Open(TEMPLATE_FILEPATH) # Open the template file
    except:
        log.error("MS WORD: Problem opening template.")
    else:
        # Insert data into bookmarked locations
        try:
            doc.Bookmarks("FirstName").Range.Text = firstname
            doc.Bookmarks("FirstName_2").Range.Text = firstname
            doc.Bookmarks("LastName").Range.Text = lastname
            doc.Bookmarks("AddressBlock").Range.Text = address
            doc.Bookmarks("TodaysDate").Range.Text = todaystring
        except:
            log.error("MS WORD: Problem with document bookmarks.")
        try:
            doc.SaveAs(savepath)
        except:
            log.error(f"MS WORD: Problem saving document - {savepath}.")
        else:
            doc.Close() # Close file ready for next one
            log.info(f"MS WORD: Document created - {savepath}.")



def closeMSWord(wordApp):
    # Close PyWin32 MS Word Object
    wordApp.Quit()
    log.info("MS WORD: Closing instance.")