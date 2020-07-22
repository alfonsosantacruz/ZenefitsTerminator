import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementNotVisibleException, StaleElementReferenceException
import platform
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import os.path as osp

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from terminator import Terminator
from gsheets import get_gsheet

def main(sheet, nav):
    # Gets the hires from the Google Sheet
    hires = sheet.get_all_values()
    
    nav.enter_login("https://secure.zenefits.com/accounts/login/", 
                    "id_username", 
                    "password", 
                    "********************", 
                    "********************",
                    "loginButton")
    
    for i, hire in enumerate(hires[1:]): # Takes the first element out to avoid the columns header
        if hire[3] != "" and hire[7] == "":
            hire_name = hire[2]
            hire_email = hire[5]
            employee_id = hire[4]
            end_date = hire[3]
            nav.search_and_terminate_hire("https://secure.zenefits.com/dashboard/#/offboarding/terminate/{}/intro".format(employee_id), 
                                          hire_name, 
                                          hire_email, 
                                          end_date)

            sheet.update_cell(i + 2, 8, "Terminated")

if __name_== "__main__":
    nav = Terminator()
    sheet = get_gsheet('**************************') # Google Sheet name goes as function argument
    main(sheet, nav)
