'''Page where all the common methods required for different pages are
situated
'''
import json
import os
import time
import allure
from allure_commons.types import AttachmentType
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.color import Color
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests import conftest
from tests.params import ULTRA_WAIT, SHORT_WAIT, DEFAULT_WAIT, LONG_WAIT, SUPER_WAIT
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
from time import sleep

locators = {
    'captcha_iframe': (By.XPATH, "//iframe[@title='reCAPTCHA']")
}


class BasePage:

    def __init__(self, browser):
        self.browser = browser
        self.ultra_wait = WebDriverWait(self.browser, ULTRA_WAIT)
        self.short_wait = WebDriverWait(self.browser, SHORT_WAIT)
        self.wait = WebDriverWait(self.browser, DEFAULT_WAIT)
        self.long_wait = WebDriverWait(self.browser, LONG_WAIT)
        self.super_wait = WebDriverWait(self.browser, SUPER_WAIT)

    def get_current_url(self):
        return self.browser.current_url

    def focus_frame_click(self, iframe, ele):
        sleep(2)
        self.scroll_to_view(iframe)
        sleep(2)
        self.long_wait.until(EC.frame_to_be_available_and_switch_to_it(iframe))
        self.long_wait.until(EC.element_to_be_clickable(ele)).click()
        sleep(2)

    def scroll_to_view(self, ele):
        l = locators
        self.browser.execute_script("arguments[0].scroll_into_view();",
                                    self.short_wait.until(EC.visibility_of_element_located(ele)))

    def verify_element(self, ele):
        try:
            isVerify = ele.is_displayed()
        except NoSuchElementException:
            isVerify = False
        return isVerify

    def verify_elmnt(self, ele):
        sleep(2)
        elmnt = self.long_wait.until(EC.presence_of_element_located(ele))
        try:
            isVerify = elmnt.is_displayed()
        except NoSuchElementException:
            isVerify = False
        return isVerify

    def not_verify_element(self, ele):
        beResult = True
        try:
            if (ele.is_displayed()):
                beResult = False
        except NoSuchElementException:
            beResult = False
        return beResult

    def js_click(self, ele):
        self.browser.execute_script("arguments[0].click();", ele)

    def click(self, ele):
        sleep(2)
        self.long_wait.until(EC.element_to_be_clickable(ele)).click()

    def enter_value(self, ele, val):
        sleep(2)
        self.long_wait.until(EC.visibility_of(ele)).click()
        sleep(1)
        self.long_wait.until(EC.visibility_of(ele)).clear()
        self.long_wait.until(EC.visibility_of(ele)).send_keys(val)

    def enter_value_without_click(self, ele, val):
        sleep(1)
        self.long_wait.until(EC.visibility_of(ele)).clear()
        self.long_wait.until(EC.visibility_of(ele)).send_keys(val)

    def clear_text_box(self, ele):
        sleep(2)
        self.long_wait.until(EC.visibility_of(ele)).clear()

    def select_by_visible_text(self, ele, val):
        select = Select(self.long_wait.until(EC.visibility_of(ele)))
        # select by visible text
        select.select_by_visible_text(val)

    def focus_and_return_back_to_parent_window(self, x):
        handles = self.browser.window_handles
        size = len(handles)
        parent_handle = self.browser.current_window_handle
        for x in range(size):
            if handles[x] != parent_handle:
                self.browser.switch_to.window(handles[x])
                print(self.browser.title)
                # if elmnt.is_displayed():
                #     return True
                self.browser.close()
                break
        self.browser.switch_to.window(parent_handle)

    def focus_window(self, x):
        handles = self.browser.window_handles
        size = len(handles)
        parent_handle = self.browser.current_window_handle
        for x in range(size):
            if handles[x] != parent_handle:
                self.browser.switch_to.window(handles[x])
                print(self.browser.title)

    def focus_frame(self, ele):
        eli = self.long_wait.until(EC.visibility_of_element_located(ele))
        self.browser.switch_to.frame(eli)

    def mouse_over(self, ele):
        Action = ActionChains(self.browser)
        elmnt = self.long_wait.until(EC.visibility_of_element_located(ele))
        Action.move_to_element(elmnt)
        Action.perform()

    def mouse_click(self, ele):
        Action = ActionChains(self.browser)
        elmnt = self.long_wait.until(EC.visibility_of_element_located(ele))
        Action.click(elmnt)
        Action.perform()

    def scroll_down(self, ele):
        Action = ActionChains(self.browser)
        Action.move_to_element(ele)
        Action.perform()

    def scroll(self, ele):
        self.browser.execute_script(
            'arguments[0].scroll_into_view(true);', ele)

    def scroll_to_top_of_the_page(self, ele):
        self.long_wait.until(EC.element_to_be_clickable(
            ele)).send_keys(Keys.CONTROL + Keys.HOME)

    def js_scroll_up(self):
        self.browser.execute_script("window.scrollTo(0,0);")

    def js_scroll_down(self):
        self.browser.execute_script("window.scrollTo(0,500);")

    def scroll_into_view(self, ele):
        elmnt = self.long_wait.until(EC.visibility_of_element_located(ele))
        self.browser.execute_script(
            'arguments[0].scrollIntoView(true);', elmnt)

    def screenshot_attachment(self, Screenshot):
        allure.attach(self.browser.get_screenshot_as_png(),
                      name=Screenshot, attachment_type=AttachmentType.PNG)

    def wait_for_element_disappear(self, elmnt):
        isElementDisappear = False
        try:
            self.long_wait.until(EC.invisibility_of_element_located(elmnt))
            isElementDisappear = True

        except NoSuchElementException:
            print("Error Occurred")
        return isElementDisappear

    def fluent_wait(self, ele, secs):
        WebDriverWait(self.browser, 60, poll_frequency=secs).until(EC.visibility_of_element_located(ele),
                                                                   'Error')

    def refresh_and_wait(self, ele):
        try:
            self.browser.implicitly_wait(2)
            print("before Fluent wait in try")
            WebDriverWait(self.browser, 600, poll_frequency=120).until(EC.invisibility_of_element_located(ele),
                                                                       'Error')
            print("after Fluent wait in try")
            self.browser.refresh()
            print("after refresh in try")

            if (ele.is_displayed()):
                print("before Fluent wait in if")
                WebDriverWait(self.browser, 120, poll_frequency=60).until(EC.invisibility_of_element_located(ele),
                                                                          'Error')
                print("after Fluent wait in if")
                self.browser.refresh()
                print("after refresh in if")
            else:
                print("inside else")
                return ele
        except:
            print("Video has not been transcoded")

    def new_wind(self):

        self.browser.execute_script('''window.open("", "_blank");''')
        print('new window opened')

    def verify_color(self, ele, hexvalue, val):
        try:
            expected = hexvalue
            elmnt = self.long_wait.until(EC.visibility_of_element_located(ele))
            txtcolor = elmnt.value_of_css_property(val)
            hexcolor = Color.from_string(txtcolor).hex
            actual = hexcolor
            if (actual == expected):
                return True
        except Exception as e:
            print(e)
        return False

    def focus_next_window(self, x):
        handles = self.browser.window_handles
        size = len(handles)
        parent_handle = self.browser.current_window_handle
        for x in range(size):
            if handles[x] != parent_handle:
                self.browser.switch_to.window(handles[x])
                print(self.browser.title)
                # if elmnt.is_displayed():
                #     return True
                break
        self.browser.switch_to.window(parent_handle)

    def close_window(self, x):
        handles = self.browser.window_handles
        size = len(handles)
        parent_handle = self.browser.current_window_handle
        for x in range(size):
            if handles[x] != parent_handle:
                self.browser.switch_to.window(handles[x])
                print(self.browser.title)
                self.browser.close()

    def scroll_left(self, ele):
        Action = ActionChains(self.browser)
        elmnt = self.long_wait.until(EC.visibility_of_element_located(ele))
        Action.move_to_element_with_offset(elmnt, 100, 100)
        Action.perform()
        print("Mousedrag Successful")

    def fluent_wait_new(self, ele, secs):
        WebDriverWait(self.browser, 60, poll_frequency=secs).until(
            EC.visibility_of_element_located(ele), 'Error')

    def verify_color_code(self, ele, hexvalue, val):
        try:
            expected = hexvalue
            txtcolor = ele.value_of_css_property(val)
            hexcolor = Color.from_string(txtcolor).hex
            actual = hexcolor
            if (actual == expected):
                return True

        except Exception as e:
            print(e)

        return False

    def refresh_page(self):
        self.browser.refresh()

    def wait_for_seconds(self, secs):
        time.sleep(secs)
