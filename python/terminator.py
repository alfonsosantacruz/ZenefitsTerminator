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


class Terminator:
    def __init__(self, no_gui=False):
        executable = ''

        if platform.system() == 'Windows':
            print('Detected OS : Windows')
            executable = '../chromedriver/chromedriver_win.exe'
        elif platform.system() == 'Linux':
            print('Detected OS : Linux')
            executable = '../chromedriver/chromedriver_linux'
        elif platform.system() == 'Darwin':
            print('Detected OS : Mac')
            executable = '../chromedriver/chromedriver_mac'
        else:
            raise OSError('Unknown OS Type')

        if not osp.exists(executable):
            raise FileNotFoundError('Chromedriver file should be placed at {}'.format(executable))

        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

        if no_gui:
            chrome_options.add_argument('--headless')
        self.browser = webdriver.Chrome(executable, chrome_options=chrome_options)

        browser_version = 'Failed to detect version'
        chromedriver_version = 'Failed to detect version'
        different_version = False

        if 'browserVersion' in self.browser.capabilities:
            browser_version = str(self.browser.capabilities['browserVersion'])

        if 'chrome' in self.browser.capabilities:
            if 'chromedriverVersion' in self.browser.capabilities['chrome']:
                chromedriver_version = str(self.browser.capabilities['chrome']['chromedriverVersion']).split(' ')[0]

        if browser_version.split('.')[0] != chromedriver_version.split('.')[0]:
            different_version = True

        print('_________________________________')
        print('Current web-browser version:\t{}'.format(browser_version))
        print('Current chrome-driver version:\t{}'.format(chromedriver_version))
        if different_version:
            print('warning: Different Version')
            print('Download correct version at "http://chromedriver.chromium.org/downloads" and place in "./chromedriver"')
        print('_________________________________')
        
    def enter_login(self, url, username_item_id, password_item_name, username, password, login_button_id):
        self.browser.get(url)
        
        print("Starting access to Zenefits")
        
        # time.sleep(30)
        
        self.browser.find_element_by_id(username_item_id).send_keys(username)
        
        self.browser.find_element_by_name(password_item_name).send_keys(password)
        
        self.browser.find_element_by_id(login_button_id).click()
        
        print("Access to Zenefits Confirmed")
        
        time.sleep(30) # One minute for the human user to input the access code
        
    def wait_and_click(self, xpath):
        #  Sometimes click fails unreasonably. So tries to click at all cost.
        try:
            w = WebDriverWait(self.browser, 10)
            elem = w.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            elem.click()
        except Exception as e:
            print('Click time out - {}'.format(xpath))
            time.sleep(2)
            return self.wait_and_click(xpath)

        return elem
        
    def search_and_terminate_hire(self, url, name, email, end_date):
        
        print("")
        print("Started termination for ", name, email)
        print("")
        
        self.browser.get(url)
            
        # Next button to start termination process
        self.wait_and_click("//button[@class='btn--primary js-glue-termination-confirm-button ember-view z-laddaButton btn btn--primary']")
        # self.browser.find_element_by_xpath().click()
        
        time.sleep(3)
        
        # Basic info about employee termination
        # print(self.browser.find_elements_by_xpath("//div[@class='grid-block shrink z-radioButtonOptionWrapper ']"))
        self.browser.find_elements_by_xpath("//div[@class='grid-block shrink z-radioButtonOptionWrapper ']")[2].click()
        
        #self.browser.find_element_by_class_name("z-textField-textarea js-z-textField-textarea ember-view ember-text-area").send_keys("Switching all users to a new platform")
        
        self.browser.find_element_by_xpath("//input[@class='z-textField-input js-z-textField-input js-glue-z-textField-input ember-view ember-text-field']").send_keys(end_date)
        
        self.browser.find_element_by_xpath("//button[@class='btn--primary u-bumperLeft js-glue-termination-confirm-button ember-view z-laddaButton btn btn--primary']").click()
        
        time.sleep(2)
        
        # Clicks Next button after asking for COBRA
        self.browser.find_element_by_xpath("//button[@class='btn--primary u-bumperLeft js-glue-termination-confirm-button ember-view z-laddaButton btn btn--primary']").click()
    
        time.sleep(2)
        
        # Clicks checkmark for the employee to be terminated from Payroll as well
        self.browser.find_element_by_xpath("//div[@class='ember-view js-glue-radio-block-wrapper radio-block-wrapper grid-block u-justifyCenter is-yes']").click()
        
        time.sleep(2)
        
        # Selects the next options for terminating from Payroll
        self.browser.find_element_by_xpath("//div[@class='ember-view js-glue-radio-block-wrapper radio-block-wrapper grid-block u-justifyCenter is-yes']").click()
        self.browser.find_element_by_xpath("//div[@class='ember-view js-glue-radio-block-wrapper radio-block-wrapper grid-block u-justifyCenter is-yes']").click()
        
        # Select(self.browser.find_element_by_xpath("//select[@class='selectField-native ember-view ember-select']")).select_by_visible_text("Mutual Agreement")
        
        self.browser.find_element_by_xpath("//button[@class='btn--primary u-bumperLeft js-glue-termination-confirm-button ember-view z-laddaButton btn btn--primary']").click()
        
        time.sleep(2)
        
        # Confirms email
        self.browser.find_element_by_xpath("//input[@class='z-textField-input js-z-textField-input ember-view ember-text-field']").clear()
        self.browser.find_element_by_xpath("//input[@class='z-textField-input js-z-textField-input ember-view ember-text-field']").send_keys(email)

        self.browser.find_element_by_xpath("//button[@class='btn--primary u-bumperLeft js-glue-termination-confirm-button ember-view z-laddaButton btn btn--primary']").click()
        
        time.sleep(2)
        
        # Confirms termination
        # Obtains name from placeholder and modifies it to satisfy the conditions of the input
        name = self.browser.find_element_by_xpath("//input[@class='z-textField-input js-z-textField-input ember-view ember-text-field']").get_attribute("placeholder")
        name = name[7:-1].upper()
        self.browser.find_element_by_xpath("//input[@class='z-textField-input js-z-textField-input ember-view ember-text-field']").send_keys(name)
        
        self.browser.find_element_by_xpath("//button[@class='btn--primary u-bumperLeft js-glue-termination-confirm-button ember-view z-laddaButton btn btn--primary']").click()
        
        print("")
        print('Termination Confirmed for ', name, email)
        print("")
        
        self.wait_and_click("//button[@class='btn--primary js-glue-termination-confirm-button ember-view z-laddaButton btn btn--primary']")
            
        # time.sleep(10)
        
        # self.browser.find_element_by_xpath("//button[@class='btn--primary js-glue-termination-confirm-button ember-view z-laddaButton btn btn--primary']").click()
        
        print('Termination DONE for ', name, email)
        print("")
        print("-----------------------------------------------------------------------------")
        
        time.sleep(5)
        
