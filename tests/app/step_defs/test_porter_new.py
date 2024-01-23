import os
from pytest_bdd import given, when, then, parsers, scenarios
import json
from tests.app.pages.login_page import LoginPage
from tests.app.pages.porternew_page import PorterPage
from tests import conftest
import pytest
from tests.testrail_util import *
import requests


scenarios('../features/trackerwave.feature')

# pytest --browser Chrome --env demo -k "tester" -v -s --html=report1.html

with open(os.path.realpath('') + os.sep + 'tests' + os.sep + 'testdata.json') as testdata:
    data = json.load(testdata)


@pytest.fixture
def testrail_util():
    return conftest.testrail_util

@given(parsers.parse("I launch Demo TrackerWave App"))
def enterprise_LoginPage(browser, db):
    LoginPage(browser).launch_url(db)

@when(parsers.parse("I enter a valid {EMAIL} and {PASSWORD}"))
def login_with_valid_credentials(browser, EMAIL, PASSWORD):
    LoginPage(browser).enter_valid_email_and_password(data[EMAIL], data[PASSWORD])

@then(parsers.parse("I should see the homepage"))
def verify_main_page(browser):
    PorterPage(browser).hamburger_click_if_no_request_page_appear()
    PorterPage(browser).verify_trackerwave_main_page()  

@given(parsers.parse("I am on the homepage"))
def verify_main_page(browser):
    PorterPage(browser).hamburger_click_if_no_request_page_appear()
    PorterPage(browser).verify_trackerwave_main_page()

@when(parsers.parse("I create a request using following details {Servicegroup} , {Servicename} , {From} , {Remarks}"))
def enter_required_options(browser, Servicegroup, Servicename, From):
    PorterPage(browser).click_button("create_request")
    PorterPage(browser).select_service_group(Servicegroup)
    PorterPage(browser).select_service_name(Servicename)
    PorterPage(browser).select_from(From)
    PorterPage(browser).enter_remarks(data['remark']+"_"+conftest.strExecutionID)
    PorterPage(browser).click_pickup_time()
    PorterPage(browser).click_button("send_request")

@then(parsers.parse("I should see the requestId and {remarks}"))
def verify_message(browser):
    PorterPage(browser).accept_confirmation_if_appear()
    PorterPage(browser).verify_success_message()
    PorterPage(browser).verify_request_id()
    PorterPage(browser).search_id(data['remark']+"_"+conftest.strExecutionID)
    PorterPage(browser).verify_remarks(data['remark']+"_"+conftest.strExecutionID)
    PorterPage(browser).get_request_id(data['remark']+"_"+conftest.strExecutionID)