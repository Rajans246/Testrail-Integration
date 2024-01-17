from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from tests.locators import *
from tests.conftest import *
from tests.params import ULTRA_WAIT, SHORT_WAIT, DEFAULT_WAIT, LONG_WAIT, SUPER_WAIT
from tests.capabilities.actions.web_actions import BasePage
import allure


class PorterPage(BasePage):
    def __init__(self, browser):
        self.browser = browser
        self.ultra_wait = WebDriverWait(self.browser, ULTRA_WAIT)
        self.short_wait = WebDriverWait(self.browser, SHORT_WAIT)
        self.wait = WebDriverWait(self.browser, DEFAULT_WAIT)
        self.long_wait = WebDriverWait(self.browser, LONG_WAIT)
        self.super_wait = WebDriverWait(self.browser, SUPER_WAIT)

    def verify_trackerwave_main_page(self):
        l = locators
        BasePage.fluent_wait(self, l['all_requests'], 3)
        BasePage.verify_elmnt(self, l['all_requests'])
        BasePage.screenshot_attachment(self, "Request_page")

    def click_create_request(self):
        l = locators
        BasePage.fluent_wait(self, l['create_request'], 3)
        BasePage.verify_elmnt(self, l['create_request'])
        BasePage.screenshot_attachment(self, "createRequest")
        BasePage.click(self, l["create_request"])

    def click_button(self, element):
        l = locators
        element = element.lower()
        print(element)
        BasePage.fluent_wait(self, l[element], 5)
        BasePage.verify_elmnt(self, l[element])
        BasePage.click(self, l[element])

    def select_dropdown_value(self, element):
        l = locators
        element = self.browser.find_element(
            By.XPATH, "//mat-option//span[contains(text(),'{0}')]".format(str(element)))
        print(element)
        BasePage.js_click(self, element)
        BasePage.wait_for_seconds(self, 5)

    def select_service_group(self, element):
        l = locators
        BasePage.fluent_wait(self, l['service_group'], 5)
        BasePage.verify_elmnt(self, l['service_group'])
        BasePage.click(self, l['service_group'])
        BasePage.wait_for_seconds(self, 1)
        BasePage.screenshot_attachment(self, "serviceGroup")
        PorterPage.select_dropdown_value(self, element)

    def select_service_name(self, element):
        l = locators
        BasePage.fluent_wait(self, l['service_name'], 5)
        BasePage.verify_elmnt(self, l['service_name'])
        BasePage.click(self, l['service_name'])
        BasePage.wait_for_seconds(self, 1)
        BasePage.screenshot_attachment(self, "serviceName")
        PorterPage.select_dropdown_value(self, element)

    def select_from(self, values):
        element = self.browser.find_element(
            By.XPATH, "//input[@formcontrolname='sourceId']")
        element.send_keys("room")
        BasePage.wait_for_seconds(self, 7)
        BasePage.screenshot_attachment(self, "entered room values")
        element1 = self.browser.find_element(
            By.XPATH, "//mat-option//span//div[contains(text(),'{0}')]".format(str(values)))
        BasePage.screenshot_attachment(self, "select room values")
        print("element1")
        print(element1)
        BasePage.js_click(self, element1)

    def enter_remarks(self, value):
        l = locators
        BasePage.scroll_into_view(self, l["remarks_input"])
        elmnt = self.long_wait.until(
            EC.visibility_of_element_located(l['remarks_input']))
        BasePage.enter_value(self, elmnt, value)

    def verify_remarks(self, value):
        ele = (By.XPATH, " //span[contains(text(),' {0}')]".format(str(value)))
        BasePage.fluent_wait(self, ele, 3)
        BasePage.verify_elmnt(self, ele)
        BasePage.screenshot_attachment(self, "verify_remarks")

    def click_send_request(self, value):
        l = locators
        BasePage.wait_for_seconds(self, 3)
        BasePage.click(self, l['send_request'])
        BasePage.wait_for_seconds(self, 1)

    def accept_confirmation_if_appear(self):
        l = locators
        # BasePage.wait_for_seconds(self,1)
        try:
            ele = self.ultra_wait.until(
                EC.visibility_of_element_located(l['waiting_confirmation']))
            # BasePage.focusFrame(self,l["waiting_confirmation"])
            yes_ele = self.ultra_wait.until(
                EC.visibility_of_element_located(l['yes']))
            elem = ele.is_displayed()
            if (elem == True):
                BasePage.js_click(self, yes_ele)

        except:
            pass

    def verify_success_message(self):
        l = locators
        BasePage.verify_elmnt(self, l['success_message'])
        BasePage.screenshot_attachment(self, "successMessage")

    def verify_request_id(self):
        l = locators
        BasePage.wait_for_seconds(self, 3)
        BasePage.verify_elmnt(self, l['request_id'])
        BasePage.screenshot_attachment(self, "requestId")

    def search_id(self, value):
        l = locators
        elmnt = self.long_wait.until(
            EC.visibility_of_element_located(l['search']))
        BasePage.wait_for_seconds(self, 3)
        BasePage.enter_value(self, elmnt, value)
        BasePage.wait_for_seconds(self, 3)

    def get_request_id(self, value):
        requetmail = (
            By.XPATH, "//span[contains(normalize-space(),'{0}')]//preceding::span[contains(normalize-space(),'RequestID')]/following::td[contains(@class,'RequestID')]/span".format(str(value)))
        BasePage.fluent_wait(self, requetmail, 3)
        requestemailrefresh = self.long_wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//span[contains(normalize-space(),'{0}')]//preceding::span[contains(normalize-space(),'RequestID')]/following::td[contains(@class,'RequestID')]/span".format(str(value)))))
        # print(requestemailrefresh)
        requestemailtxt = requestemailrefresh.text
        allure.attach(f"{requestemailtxt}", name="Request ID Values",
                      attachment_type=allure.attachment_type.TEXT)
        print("Request Id : " + requestemailtxt + " Remark --> "+value)

    def click_pickup_time(self):
        l = locators
        BasePage.scroll_into_view(self, l["pickup_time"])
        elmnt1 = self.long_wait.until(
            EC.visibility_of_element_located(l['pickup_time']))
        BasePage.click(self, l['pickup_time'])
        element = self.browser.find_element(
            By.XPATH, "//input[@formcontrolname='startTime']")
        Action = ActionChains(self.browser)
        Action.move_to_element(elmnt1).click().send_keys(
            Keys.ARROW_RIGHT).perform()
        Action.move_to_element(elmnt1).click().send_keys(
            Keys.ARROW_RIGHT).perform()
        Action.move_to_element(elmnt1).click().send_keys(
            Keys.ARROW_RIGHT).perform()
        Action.move_to_element(elmnt1).click(
        ).send_keys(Keys.ARROW_UP).perform()
        # BasePage.wait_for_seconds(self, 3)

    def hamburger_click_if_no_request_page_appear(self):
        l = locators
        print("before click the hamburger")
        try:
            ele = self.wait.until(EC.visibility_of_element_located(
                l['all_requests'])).is_displayed()
            print("ele is displayed")
            print(ele)
        except:
            BasePage.click(self, l['hamburger'])
            BasePage.click(self, l['workflows'])
