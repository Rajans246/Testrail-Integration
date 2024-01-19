import os
from pytest_bdd import given, when, then, parsers, scenarios
import json
from tests.app.pages.login_page import LoginPage
from tests.app.pages.porternew_page import PorterPage
from tests import conftest
# from tests import conftest
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

@pytest.fixture
def scenario_id(request):
    # Extract scenario name from the request object and fetch the TestRail case ID dynamically
    marker = request.node.get_closest_marker('scenario')
    if marker:
        scenario_name = marker.args[0]
        # Implement logic to fetch the TestRail case ID based on the scenario name
        # For simplicity, I'm assuming you have a function get_case_id_from_scenario_name
        return TestRailUtil.get_case_id_from_scenario_name(scenario_name)
    else:
        # Handle the case where 'scenario' marker is not found
        return None


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
    # test_run_id = TestRailUtil.run['id']
    # test_case_id = TestRailUtil.testCase['id']
    # TestRailUtil.add_test_result(data["str_testrunID"], data["str_testcaseID"])
    

@given(parsers.parse("I am on the homepage"))
def verify_main_page(browser):
    PorterPage(browser).hamburger_click_if_no_request_page_appear()
    PorterPage(browser).verify_trackerwave_main_page()

@when(parsers.parse("I create a request using following details {Servicegroup} , {Servicename} , {From} , {Remarks}"))
def enter_required_options(browser, Servicegroup, Servicename, From, Remarks):
    PorterPage(browser).click_button("create_request")
    PorterPage(browser).select_service_group(Servicegroup)
    PorterPage(browser).select_service_name(Servicename)
    PorterPage(browser).select_from(From)
    PorterPage(browser).enter_remarks(data['remark']+"_"+conftest.strExecutionID)
    PorterPage(browser).click_pickup_time()
    PorterPage(browser).click_button("send_request")

@then(parsers.parse("I should see the requestId and {remarks}"))
def verify_message(browser, remarks,request):
    # test_run_id = TestRailUtil.run['id']
    # test_case_id = TestRailUtil.testCase['id']
    PorterPage(browser).accept_confirmation_if_appear()
    PorterPage(browser).verify_success_message()
    PorterPage(browser).verify_request_id()
    PorterPage(browser).search_id(data['remark']+"_"+conftest.strExecutionID)
    PorterPage(browser).verify_remarks(data['remark']+"_"+conftest.strExecutionID)
    PorterPage(browser).get_request_id(data['remark']+"_"+conftest.strExecutionID)
    # TestRailUtil.update_test_result(scenario_id(request), status_id=1)
    # scenario_tags = request.node.get_closest_marker('scenario').args[0]

    # # Now you can use scenario_tags to get the specific tag information, e.g., @testrail-C1
    # for tag in scenario_tags:
    #     if 'testrail' in tag:
    #         case_id = tag.split('-')[-1]
    #         # Now you can use the case_id as needed
    #         TestRailUtil.update_test_result(case_id, status_id=1)
    
    # TestRailUtil.update_test_result(1, status_id=5)
    # marker = request.node.get_closest_marker('scenario')
 
    # if marker:
    #     scenario_tags = marker.args[0]
    #     # Now you can use scenario_tags to get the specific tag information, e.g., @testrail-C1
    #     for tag in scenario_tags:
    #         if 'testrail' in tag:
    #             case_id = tag.split('-')[-1]
    #             # Now you can use the case_id as needed
    #             caseid = 1
    #             TestRailUtil.update_test_result(caseid, status_id=1)  # Assuming status_id=1 for a passed test
    # else:
    #     # Handle the case where 'scenario' marker is not found
    #     pass


    
    # Simulate a PASS or FAIL status based on your test logic
    
    # scenario_status = "FAILED"

    # Add the test result to TestRail
    # TestRailUtil.add_test_result(test_run_id, test_case_id)