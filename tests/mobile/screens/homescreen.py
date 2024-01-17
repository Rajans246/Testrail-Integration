from tests.mobile_locators import mlocators 
from tests.capabilities.actions.mobile_actions import BaseScreen

class HomeScreen(BaseScreen):
    def __init__(self, browser):
        self.browser = browser

    def verify_homescreen_element(self):
        l = mlocators
        BaseScreen.verify_element(self,l['search_product'])
        BaseScreen.take_screenshot(self, "search_product")

    def tap_select_application_dropdown(self):
        l = mlocators
        BaseScreen.tap(self, l['application_dropdown'])
        BaseScreen.tap(self, l['home_textiles_radio_btn'])

    def tap_select_range_dropdown(self):
        l = mlocators
        BaseScreen.tap(self, l['range_dropdown'])
        BaseScreen.tap(self, l['home_furnishing_radio_btn'])

    def click_submit(self):
        l = mlocators
        BaseScreen.tap(self, l['submit_btn'])

    def verify_details_tab(self):
        l = mlocators
        BaseScreen.tap(self, l['view_more_btn'])
        BaseScreen.verify_element(self,l['details_tab'])
        BaseScreen.take_screenshot(self, "details_tab")

    def select_home_screen(self):
        l = mlocators
        BaseScreen.tap(self, l['home_tile_btn'])