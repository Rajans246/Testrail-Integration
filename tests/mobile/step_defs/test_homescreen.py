from pytest_bdd import given, when, then, parsers, scenarios
from tests.mobile.screens.homescreen import HomeScreen


scenarios('../features/homescreen.feature')

@given(parsers.parse("I am on Raysil application Home screen"))
def verify_homescreen(browser):
        HomeScreen(browser).verify_homescreen_element()

@given(parsers.parse("I select Application and Range"))
def select_application_and_range(browser):
        HomeScreen(browser).tap_select_application_dropdown()
        HomeScreen(browser).tap_select_range_dropdown()

@when(parsers.parse("I tap on Submit button"))
def select_product(browser):
        HomeScreen(browser).click_submit()

@then(parsers.parse("I should see Details screen for Range"))
def select_product(browser):
        HomeScreen(browser).verify_details_tab()

@then(parsers.parse("I tap Home Footer Icon"))
def select_product(browser):
        HomeScreen(browser).select_home_screen()
        HomeScreen(browser).verify_homescreen_element()