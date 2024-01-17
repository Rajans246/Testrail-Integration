from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.conftest import *
from tests.conftest import server
from tests.params import ULTRA_WAIT, SHORT_WAIT, DEFAULT_WAIT, LONG_WAIT, SUPER_WAIT
from tests.capabilities.actions.web_actions import BasePage
from tests.locators import *
import allure


class LoginPage(BasePage):
    def __init__(self, browser):
        self.browser = browser
        self.ultra_wait = WebDriverWait(self.browser, ULTRA_WAIT)
        self.short_wait = WebDriverWait(self.browser, SHORT_WAIT)
        self.wait = WebDriverWait(self.browser, DEFAULT_WAIT)
        self.long_wait = WebDriverWait(self.browser, LONG_WAIT)
        self.super_wait = WebDriverWait(self.browser, SUPER_WAIT)

    def launch_url(self, db):  # Pass adminServer fixture as a default parameter
        url = server(db)  # Use admin_server fixture to generate URL
        print(url)
        self.browser.get(url)

    def verify_enterprise_loginPage(self):
        l = locators
        BasePage.wait_for_seconds(self, 5)
        BasePage.fluent_wait(self, l['btn_login'], 3)
        elment_to_verify = self.long_wait.until(
            EC.visibility_of_element_located(l['btn_login']))
        BasePage.verify_element(self, elment_to_verify)
        BasePage.screenshot_attachment(self, "LoginPage")
        BasePage.screenshot_attachment(self, "LoginPage")

    def verify_admin_main_page(self):
        l = locators
        BasePage.fluent_wait(self, l["txt_main_page_verify"], 3)
        BasePage.verify_elmnt(self, l['txt_main_page_verify'])
        BasePage.screenshot_attachment(self, "AdminMainPage")

    def enter_valid_email_and_password(self, strEmail, strPassword):
        l = locators
        elmnt_email = self.long_wait.until(
            EC.visibility_of_element_located(l['txt_username']))
        BasePage.enter_value(self, elmnt_email, strEmail)
        allure.attach(f"{strEmail}", name="Username",
                      attachment_type=allure.attachment_type.TEXT)
        elmnt_password = self.long_wait.until(
            EC.visibility_of_element_located(l['txt_password']))
        allure.attach(f"{strPassword}", name="password",
                      attachment_type=allure.attachment_type.TEXT)
        BasePage.enter_value(self, elmnt_password, strPassword)
        BasePage.fluent_wait(self, l["btn_login"], 3)
        BasePage.click(self, l["btn_login"])

    def refresh_page(self):
        self.browser.refresh()
