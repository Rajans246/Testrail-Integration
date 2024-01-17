from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure

class BaseScreen:
    def __init__(self, browser):
        self.browser = browser

    def verify_element(self, ele):
        element = WebDriverWait(self.browser, 30).until(EC.presence_of_element_located(ele))
        assert element

    def take_screenshot(self, Screenshot):
        allure.attach(self.browser.get_screenshot_as_png(), name=Screenshot, attachment_type=allure.attachment_type.PNG)

    def tap(self, ele):
        element = WebDriverWait(self.browser, 30).until(EC.presence_of_element_located(ele))
        element.click()