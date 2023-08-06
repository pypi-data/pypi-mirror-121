from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


import logging
logger = logging.getLogger('selenium.webdriver.remote.remote_connection')
logger.setLevel(logging.WARNING)  # or any variant from ERROR, CRITICAL or NOTSET


# import pyautogui, pyperclip
import time, os
from python_helper import Constant as c
from python_helper import log


###- https://www.selenium.dev/selenium/docs/api/py/webdriver_support/selenium.webdriver.support.expected_conditions.html
###- https://sites.google.com/a/chromium.org/chromedriver/downloads
class SeleniumHelper:

    TAG_BODY = 'body'
    TAG_SELECT = 'select'
    TAG_OPTION = 'option'
    TAG_HEADER = 'header'
    TAG_BUTTON = 'button'
    TAG_IMPUT = 'input'
    TAG_TABLE = 'table'
    TAG_FORM = 'form'
    TAG_PRE = 'pre'
    TAG_BR = 'br'

    ATTRIBUTE_HREF = 'href'

    def __init__(self, globals, waittingTime=2, headless=True):
        self.globals = globals
        # self.pyautogui = pyautogui
        # self.pyautogui.FAILSAFE = True
        # self.pyperclip = pyperclip
        self.time = time
        self.waittingTime = waittingTime
        self.fractionOfWaittingTime = waittingTime / 7.0
        self.driverPath = f'{self.globals.apiPath}api{self.globals.OS_SEPARATOR}resource{self.globals.OS_SEPARATOR}dependency{self.globals.OS_SEPARATOR}chromedriver.exe'
        self.aKey = 'a'
        self.closeBraceKey = '}'

    def newDriver(self):
        try :
            self.closeDriver()
        except Exception as exception :
            log.log(self.newDriver, f'Failed to close driver', exception=exception)
        try :
            try :
                chromeOptions = webdriver.ChromeOptions()
                chromeOptions.add_argument('--ignore-certificate-errors')
                chromeOptions.add_argument("user-agent=whatever you want")
                chromeOptions.add_argument('--disable-blink-features=AutomationControlled')
                chromeOptions.add_experimental_option("excludeSwitches", ["enable-automation"])
                chromeOptions.add_experimental_option('useAutomationExtension', False)
                chromeOptions.add_argument('--disable-extensions')
                chromeOptions.add_argument('--disable-gpu')
                chromeOptions.add_argument('--disable-dev-shm-usage')
                chromeOptions.add_argument('--no-sandbox')
                if headless:
                    chromeOptions.add_argument("headless")
                chromeOptions.add_argument('--incognito')
                chromeOptions.add_argument('--log-level 3')
                chromeOptions.add_argument('--disable-logging')
                chromeOptions.add_experimental_option("excludeSwitches", ["enable-logging"])
                chromeOptions.add_experimental_option('detach', True)
                self.driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chromeOptions) ### webdriver.Chrome(executable_path=self.driverPath)
            except Exception as exception :
                log.failure(self.newDriver, f'Failed to load web driver from default library. Going for a second attempt by another library', exception=exception)
                self.driver = webdriver.Chrome(executable_path=self.driverPath)
            self.wait()
            return self.driver.find_element_by_tag_name(self.TAG_BODY)
        except Exception as exception :
            log.error(self.newDriver, f'Failed to creat a new driver', exception)

    def reset(self):
        try :
            self.driver.switch_to.default_content();
            self.wait(fraction=True)
        except Exception as exception :
            log.error(self.reset, f'Failed to reset driver', exception)

    def closeDriver(self):
        try :
            self.driver.close()
        except Exception as exception :
            log.failure(self.closeDriver,f'Failed to close driver', exception)

    def wait(self,fraction=False,processingTime=None):
        if fraction :
            self.time.sleep(self.fractionOfWaittingTime)
        elif processingTime :
            self.time.sleep(processingTime)
        else :
            self.time.sleep(self.waittingTime)

    # def copyPasteAutoguiAfterElementClicked(self,text):
    #     try :
    #         self.pyperclip.copy(text)
    #         self.pyautogui.hotkey("ctrl", "v")
    #         self.wait()
    #     except Exception as exception :
    #         log.error(self.copyPasteAutoguiAfterElementClicked,f'Failed to copy paste text (by pyautogui)', exception)

    def paste(self,text,elementRequest):
        try :
            os.system("echo %s| clip" % text.strip())
            elementRequest.send_keys(Keys.CONTROL, 'v')
            self.wait()
        except Exception as exception :
            log.error(self.paste,f'Failed to paste text to the element', exception)

    def getDriver(self,elementRequest):
        try :
            self.wait(fraction=True)
            if elementRequest :
                return elementRequest
            else :
                return self.driver
        except Exception as exception :
            log.error(self.getDriver,f'Failed to get driver', exception)

    def moveToElement(self, element):
        ActionChains(self.driver).move_to_element(element).perform()
        self.wait(fraction=True)

    def accessUrl(self,url,waittingTime=0,acceptAlert=False,ignoreAlert=False):
        try :
            self.driver.get(url)
            self.wait(processingTime = waittingTime if waittingTime > 0 else None)
            self.handleAlertBox(waittingTime=waittingTime,acceptAlert=acceptAlert,ignoreAlert=ignoreAlert)
            self.driver.find_element_by_tag_name(self.TAG_BODY)
            return self.driver
        except Exception as exception :
            log.error(self.accessUrl,f'Failed to access url', exception)

    def refreshPage(self):
        try :
            self.driver.refresh()
            self.wait()
        except Exception as exception :
            print(f'{self.globals.ERROR}Failed to refresh page', exception)

    # def ctrlF5(self) :
    #     self.pyautogui.hotkey("ctrl", "F5")
    #     self.wait()

    def handleAlertBox(self,waittingTime=0,acceptAlert=False,ignoreAlert=False):
        resolved = False
        self.wait(processingTime = waittingTime)
        try :
            if ignoreAlert :
                self.driver.switch_to.alert.ignore()
                resolved = True
            elif acceptAlert :
                self.driver.switch_to.alert.accept()
                resolved = True
            return resolved
        except Exception as exception :
            log.error(self.handleAlertBox,f'No alertFound', exception)
            return resolved

    def findButton(self,elementRequest):
        try :
            driver = self.getDriver(elementRequest)
            element = driver.find_element_by_tag_name(self.TAG_BUTTON)
            return element
        except Exception as exception :
            log.error(self.findButton,f'Failed to find button', exception)

    def accessButton(self,elementRequest):
        try :
            driver = self.getDriver(elementRequest)
            element = driver.find_element_by_tag_name(self.TAG_BUTTON)
            self.moveToElement(element)
            element = element.click()
            self.wait(fraction=True)
            return element
        except Exception as exception :
            log.error(self.accessButton,f'Failed to access button', exception)

    def findById(self,id,elementRequest):
        try :
            driver = self.getDriver(elementRequest)
            element = driver.find_element_by_id(id)
            return element
        except Exception as exception :
            log.error(self.findById,f'Failed to find by id', exception)

    def findByClass(self,cssClass,elementRequest):
        try :
            driver = self.getDriver(elementRequest)
            element = driver.find_element_by_class_name(cssClass)
            return element
        except Exception as exception :
            log.error(self.findByClass,f'Failed to find by class', exception)

    def accessClass(self,cssClass,elementRequest):
        try :
            driver = self.getDriver(elementRequest)
            element = driver.find_element_by_class_name(cssClass)
            self.moveToElement(element)
            element = element.click()
            self.wait(fraction=True)
            return element
        except Exception as exception :
            log.error(self.accessClass,f'Failed to access class', exception)

    def accessTag(self,tagName,elementRequest):
        try :
            driver = self.getDriver(elementRequest)
            element = driver.find_element_by_tag_name(tagName)
            self.moveToElement(element)
            element = element.click()
            self.wait(fraction=True)
            return element
        except Exception as exception :
            log.error(self.accessTag,f'Failed to access tag', exception)

    def getTextByClass(self,cssClass,elementRequest):
        try :
            driver = self.getDriver(elementRequest)
            element = driver.find_element_by_class_name(cssClass)
            return element.text
        except Exception as exception :
            log.error(self.getTextByClass,f'Failed to get text by class', exception)

    def getTextBySelector(self,selector,elementRequest):
        try :
            driver = self.getDriver(elementRequest)
            element = driver.find_element_by_xpath(selector)
            return element.text
        except Exception as exception :
            log.error(self.getTextBySelector,f'Failed to get text by selector', exception)

    def findButtonByClass(self,cssClass,elementRequest):
        try :
            driver = self.getDriver(elementRequest)
            element = driver.find_element_by_css_selector(f'{self.TAG_BUTTON}.{cssClass}')
            return element
        except Exception as exception :
            log.error(self.findButtonByClass,f'Failed to find button by class', exception)

    def accessButtonByClass(self,cssClass,elementRequest):
        try :
            driver = self.getDriver(elementRequest)
            element = driver.find_element_by_css_selector(f'{self.TAG_BUTTON}.{cssClass}')
            self.moveToElement(element)
            element = element.click()
            self.wait(fraction=True)
            return element
        except Exception as exception :
            log.error(self.accessButtonByClass,f'Failed to access button by class', exception)

    def accesHiperLink(self,hiperLink,elementRequest):
        try :
            driver = self.getDriver(elementRequest)
            element = driver.find_element_by_link_text(hiperLink)
            ###- element = driver.find_element_by_partial_link_text(hiperLink)
            element = element.click()
            self.wait(fraction=True)
            return element
        except Exception as exception :
            log.error(self.accesHiperLink,f'Failed to access hyperlink', exception)

    def accessId(self,id,elementRequest):
        try :
            driver = self.getDriver(elementRequest)
            element = driver.find_element_by_id(id)
            self.moveToElement(element)
            element = element.click()
            self.wait(fraction=True)
            return element
        except Exception as exception :
            log.error(self.accessId,f'Failed to access id', exception)

    def selectAllByClass(self,cssClass,elementRequest):
        try :
            driver = self.getDriver(elementRequest)
            element = driver.find_element_by_class_name(cssClass)
            element.send_keys(Keys.CONTROL, self.aKey)
            self.wait(fraction=True)
            return element
        except Exception as exception :
            log.error(self.selectAllByClass,f'Failed to select all by class', exception)

    def typeIn(self,text,elementRequest):
        try :
            driver = self.getDriver(elementRequest)
            driver.send_keys(Keys.CONTROL, self.aKey)
            driver.send_keys(text)
            self.wait(fraction=True)
            return driver
        except Exception as exception :
            log.error(self.typeIn,f'Failed to type in', exception)

    def typeInAndHitEnter(self,text,elementRequest):
        try :
            driver = self.getDriver(elementRequest)
            driver.send_keys(Keys.CONTROL, self.aKey)
            driver.send_keys(text)
            driver.send_keys(Keys.RETURN)
            self.wait(fraction=True)
            return driver
        except Exception as exception :
            log.error(self.typeInAndHitEnter,f'Failed to type in', exception)

    def hitEnter(self,elementRequest):
        try :
            driver = self.getDriver(elementRequest)
            driver.send_keys(Keys.RETURN)
            return driver
        except Exception as exception :
            log.error(self.hitEnter,f'Failed to hit enter', exception)

    def typeInSwagger(self,text,elementRequest):
        try :
            filteredText = text.strip()
            driver = self.getDriver(elementRequest)
            driver.send_keys(Keys.CONTROL, self.aKey)
            driver.send_keys(Keys.BACKSPACE)
            driver.send_keys(Keys.ARROW_LEFT)
            driver.send_keys(filteredText[0])
            driver.send_keys(Keys.ARROW_LEFT)
            driver.send_keys(Keys.BACKSPACE)
            driver.send_keys(Keys.ARROW_RIGHT)
            driver.send_keys(text.strip()[1:])
            driver.send_keys(Keys.DELETE)
            self.wait(fraction=True)
            return driver
        except Exception as exception :
            log.error(self.typeInSwagger,f'Failed to type in swagger', exception)

    def findByTag(self,tagName,elementRequest):
        try :
            driver = self.getDriver(elementRequest)
            return driver.find_element_by_tag_name(tagName)
        except Exception as exception :
            log.error(self.findByTag,f'Failed to find by tag', exception)

    def findBySelector(self, selector, movingTo=False, muteLogs=False):
        try :
            element = self.driver.find_element_by_xpath(selector)
            self.wait(fraction=True)
            if movingTo:
                self.moveToElement(element)
            return element
        except Exception as exception :
            if not muteLogs:
                log.error(self.findBySelector,f'Failed to find by selector {selector}', exception)

    def accessSelector(self, selector, movingTo=False, muteLogs=False):
        try :
            element = self.findBySelector(selector, movingTo=movingTo)
            self.clickElement(element, muteLogs=muteLogs)
            return element
        except Exception as exception :
            if not muteLogs:
                log.error(self.accessSelector,f'Failed to access selector {selector}', exception)

    def findAllByClass(self,className,elementRequest):
        try :
            driver = self.getDriver(elementRequest)
            return driver.find_elements_by_class_name(className)
        except Exception as exception :
            log.error(self.findAllByClass,f'Failed to find all by class', exception)

    def findAllByTag(self,tagName,elementRequest):
        try :
            driver = self.getDriver(elementRequest)
            return driver.find_elements_by_tag_name(tagName)
        except Exception as exception :
            log.error(self.findAllByTag,f'Failed to find all by tag', exception)

    def findAllBySelector(self,selector,elementRequest):
        try :
            driver = self.getDriver(elementRequest)
            return driver.find_elements_by_xpath(selector)
        except Exception as exception :
            log.error(self.findAllBySelector,f'Failed to find all by class', exception)

    def clickElement(self, elementRequest, muteLogs=False):
        try :
            elementRequest.click()
        except Exception as exception :
            if not muteLogs:
                log.error(self.clickElement,f'Failed to click element {str(elementRequest)}', exception)

    # def calculateAndClick(self,position,fatherSize):
    #     try :
    #         windowX = self.driver.execute_script("return window.screenX")
    #         windowY = self.driver.execute_script("return window.screenY")
    #         windowOuterWidth = self.driver.execute_script("return window.outerWidth")
    #         windowOuterHeight = self.driver.execute_script("return window.outerHeight")
    #         windowInnerWidth = self.driver.execute_script("return window.innerWidth")
    #         windowInnerHeight = self.driver.execute_script("return window.innerHeight")
    #         windowScrollX = self.driver.execute_script("return window.scrollX")
    #         windowScrollY = self.driver.execute_script("return window.scrollY")
    #         bottonWidth = (windowOuterWidth - windowInnerWidth) / 2
    #         position[0] += int(windowX + (windowInnerWidth - fatherSize[0]) / 2 - bottonWidth)
    #         position[1] += int(windowY + (windowOuterHeight - windowInnerHeight - bottonWidth) + (windowInnerHeight - fatherSize[1]) / 2 + 1.5 * bottonWidth)
    #         self.pyautogui.moveTo(position[0],position[1])
    #         self.pyautogui.click()
    #         return position
    #     except Exception as exception :
    #         log.error(self.calculateAndClick,f'Failed to return {element}', exception)
