# import pytest
# from selenium import webdriver
# from appium.options.common import AppiumOptions
# import random
# import string
# from tests.params import server_name


# @pytest.fixture(scope='session')
# def browser(request):
#     BROWSERS = ['Chrome', 'Firefox', 'Edge', 'Mobile', 'Mobile_browser']
#     browsers = request.config.getoption("--browser")
#     headless = request.config.getoption("--headless", False)
#     assert browsers in BROWSERS
#     if browsers == 'Chrome':
#         opts = webdriver.ChromeOptions()
#         opts.add_argument("start-maximized")
#         opts.add_argument("--disable-notifications")
#         if headless:
#             opts.add_argument('headless')
        
#         browser = webdriver.Chrome(options=opts)

#     elif browsers == 'Edge':
#         opts = webdriver.EdgeOptions()
#         browser = webdriver.Edge(options=opts)

#     elif browsers == 'Mobile':
#         desired_caps = {
#             "deviceName": "Nokia",
#             "platformName": "Android",
#             "platformVersion": "11",
#             "allowTestPackages": True,
#             "autoGrantPermissions": True,
#             "ignoreHiddenApiPolicyError": True,
#             "noReset": False,
#             "appPackage": "com.puratech.raysil",
#             "appActivity": "com.puratech.raysil.MainActivity"
#         }
#         url = 'http://localhost:4723/wd/hub'
#         browser = webdriver.Remote(
#             url, options=AppiumOptions().load_capabilities(desired_caps))

#     elif browsers == 'Mobile_browser':
#         desired_caps = {
#             "deviceName": "NOkia",
#             "platformName": "Android",
#             "platformVersion": "13",
#             "allowTestPackages": True,
#             "autoGrantPermissions": True,
#             "ignoreHiddenApiPolicyError": True,
#             "noReset": False,
#             "browserName": "Chrome",
#             "chromedriverExecutable":'C:\\Users\\AJITHB\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe'
#             }
#         url = 'http://localhost:4723/wd/hub'
#         browser = webdriver.Remote(
#             url, options=AppiumOptions().load_capabilities(desired_caps))
        
#     yield browser  # Return the WebDriver instance
#     browser.quit()

# @pytest.fixture(scope='session')
# def db(request):
#     return request.config.getoption("--env")

# def pytest_addoption(parser):
#     parser.addoption("--env", action="store", default="demo")
#     parser.addoption("--browser", action="store", default="Chrome")
#     parser.addoption("--headless", action="store_true", default=False)


# def server(db):
#     print(db)
#     return server_name.format(db)


# def getRandromStringInUpperCase():
#     global strExecutionID
#     strExecutionID = ''.join((random.choice(string.ascii_uppercase) for x in range(10)))
#     print("Execution ID1 >>>> ", strExecutionID)
#     return strExecutionID

# getRandromStringInUpperCase()




import pytest
from selenium import webdriver
from appium.options.common import AppiumOptions
import random
import re
import os
import json
import string
import traceback
from tests.params import server_name
from tests.testrail_util import TestRailUtil  # Import the TestRailUtil class



testdata_path = os.path.join(os.path.dirname(__file__), 'testdata.json')
with open(testdata_path, 'r') as file:
    testdata = json.load(file)

for key, value in testdata.items():
    os.environ[key] = value

def pytest_configure(config):
    config.addinivalue_line(
        "markers", "testrail(case_id): associate a TestRail case ID with a scenario"
    )

@pytest.hookimpl(tryfirst=True)
def pytest_bdd_before_scenario(request, feature, scenario):
    custom_option = request.config.getoption("--custom-option")
    print(f"\nBefore Scenario: {feature.name} - {scenario.name}")
    print(f"Custom Option Value: {custom_option}")
    scenario_tags = list(scenario.tags)
    print(f"Scenario Tags: {scenario_tags}")
    print(f"Is 'testrail' in scenario_tags? {'testrail' in scenario_tags}")
    for tag in scenario_tags:
            print("tag is")
            print(tag)
            if tag.startswith('testrail-C'):
                case_id = tag[10:]  # Extract the TestRail case ID from the tag
                print("mytestrun rest")
                print(f"TestRail Case ID: {case_id}")
                break

@pytest.hookimpl(tryfirst=True)
def pytest_bdd_after_step(request, feature, scenario, step, step_func, step_func_args):
    if step.failed:
        print(f"After Step: {feature.name} - {scenario.name} - {step.keyword} {step.name}  FAILED")
    # if step.failed:
    # if step.Exception:
    #     print(f"Step failed due to exception: {Exception}")
    #     print(f"After Step: {feature.name} - {scenario.name} - {step.keyword} {step.name}  FAILED")
    #     # print("Custom Option Value:", request.config.getoption('--custom-option'))
        # print()
    else:
        print(f"After Step: {feature.name} - {scenario.name} - {step.keyword} {step.name}  PASSED")
        # print("Custom Option Value:", request.config.getoption('--custom-option'))
        # print("PASSED")
@pytest.hookimpl
def pytest_bdd_step_error(request, feature, scenario, step, step_func, step_func_args, exception):
    print(f"Step: {step.keyword} {step.name} encountered an error.")
    print(f"Arguments passed to step function: {step_func_args}")
    print(f"Exception: {exception}")

# @pytest.hookimpl(tryfirst=True)
# def pytest_bdd_after_scenario(request, feature, scenario):
#     custom_option = request.config.getoption("--custom-option")
#     print(f"\nAfter Scenario: {feature.name} - {scenario.name}")
#     print(f"Custom Option Value: {custom_option}")
#     for step in scenario.steps:
#         if hasattr(step, 'exception') and step.exception:
#             print(f"Step '{step.name}' failed")
#         else:
#             print(f"Step '{step.name}' passed")


@pytest.fixture(scope='session')
def browser(request):
    BROWSERS = ['Chrome', 'Firefox', 'Edge', 'Mobile', 'Mobile_browser']
    browsers = request.config.getoption("--browser")
    headless = request.config.getoption("--headless", False)
    assert browsers in BROWSERS
    if browsers == 'Chrome':
        opts = webdriver.ChromeOptions()
        opts.add_argument("start-maximized")
        opts.add_argument("--disable-notifications")
        if headless:
            opts.add_argument('headless')

        browser = webdriver.Chrome(options=opts)

    elif browsers == 'Edge':
        opts = webdriver.EdgeOptions()
        browser = webdriver.Edge(options=opts)

    elif browsers == 'Mobile':
        desired_caps = {
            "deviceName": "Nokia",
            "platformName": "Android",
            "platformVersion": "11",
            "allowTestPackages": True,
            "autoGrantPermissions": True,
            "ignoreHiddenApiPolicyError": True,
            "noReset": False,
            "appPackage": "com.puratech.raysil",
            "appActivity": "com.puratech.raysil.MainActivity"
        }
        url = 'http://localhost:4723/wd/hub'
        browser = webdriver.Remote(
            url, options=AppiumOptions().load_capabilities(desired_caps))

    elif browsers == 'Mobile_browser':
        desired_caps = {
            "deviceName": "NOkia",
            "platformName": "Android",
            "platformVersion": "13",
            "allowTestPackages": True,
            "autoGrantPermissions": True,
            "ignoreHiddenApiPolicyError": True,
            "noReset": False,
            "browserName": "Chrome",
            "chromedriverExecutable": 'C:\\Users\\AJITHB\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe'
        }
        url = 'http://localhost:4723/wd/hub'
        browser = webdriver.Remote(
            url, options=AppiumOptions().load_capabilities(desired_caps))

    yield browser  # Return the WebDriver instance
    browser.quit()

@pytest.fixture(scope='session')
def db(request):
    return request.config.getoption("--env")

def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="demo")
    parser.addoption("--browser", action="store", default="Chrome")
    parser.addoption("--headless", action="store_true", default=False)
    parser.addoption("--custom-option", action="store", default=None, help="Custom option description")

def server(db):
    print(db)
    return server_name.format(db)

def getRandromStringInUpperCase():
    global strExecutionID
    strExecutionID = ''.join((random.choice(string.ascii_uppercase) for x in range(10)))
    print("Execution ID1 >>>> ", strExecutionID)
    return strExecutionID

getRandromStringInUpperCase()

# TestRail Integration
testrail_util = TestRailUtil()

# def pytest_runtest_protocol(item, nextitem):
#     # Check if the test has the tester marker
#     # if item.has_marker("tester"):
#     if item.get_closest_marker("tester"):
#         # Get the TestRail ID from the marker (e.g., tc-01)
#         testrail_id = item.get_closest_marker("tester").args[0]

#         # Get the scenario steps
#         scenario_steps = [f"    {line.strip()}" for line in item.parent.location[0].split('\n')]

#         # Add the scenario steps as a comment
#         comment = f"\n  Given {scenario_steps[1]}\n  When {scenario_steps[2]}\n  Then {scenario_steps[3]}"

#         # Add the comment to TestRail
#         testrail_util.add_comment(testrail_id, comment)
def pytest_runtest_protocol(item, nextitem):
    # Check if the test has the tester marker
    marker = item.get_closest_marker("tester")
    if marker and marker.args:
        # Get the TestRail ID from the marker (e.g., tc-01)
        testrail_id = marker.args[0]

        # Get the scenario steps
        scenario_steps = [f"    {line.strip()}" for line in item.parent.location[0].split('\n')]

        # Add the scenario steps as a comment
        comment = f"\n  Given {scenario_steps[1]}\n  When {scenario_steps[2]}\n  Then {scenario_steps[3]}"

        # Add the comment to TestRail
        testrail_util.add_comment(testrail_id, comment)



# testrail_url = "https://codtestpy.testrail.io/"
testrail_url = os.environ["TESTRAIL_URL"]
# testrail_username = "natarajan.senthil@codoid.com"
# testrail_password = "Test@123"

# # Set your project, suite, section, and test run details
# project_name = "pytest13jan"
# suite_name = "Demo"
# section_name = "Testing"
# test_run_name = "TestRun007"

# # Set your test case details
# test_case_title = "User creates a porter request"
# str_testcaseID = "C1"
# scenario_status = "PASSED"  # or "FAILED"
# project_id = 55
# section_id = section_id
testrail_username = os.environ["TESTRAIL_USER"]
testrail_password = os.environ["TESTRAIL_PASSWORD"]

# Set your project, suite, section, and test run details
project_name = os.environ["project_name"]
suite_name = os.environ["suite_name"]
section_name = os.environ["section_name"]
test_run_name = os.environ["test_run_name"]

# Set your test case details
test_case_title = os.environ["test_case_title"]
str_testcaseID = os.environ["str_testcaseID"]
scenario_status = os.environ["scenario_status"]
project_id = int(os.environ["project_id"])
section_id = int(os.environ["section_id"])


@pytest.fixture(scope="session", autouse=True)
def setup_testrail():
    # Create TestRail instance
    TestRailUtil.create_testrail_instance(testrail_url, testrail_username, testrail_password)

    # Create TestRail project
    project_id = TestRailUtil.create_testrail_project(project_name)

    # Create TestRail suite
    print("testsuite")
    print(type(project_id))
    print(project_id)
    
    suite_id = TestRailUtil.create_testrail_suite_test(project_id, suite_name=suite_name)

    # Create TestRail section
    section_id = TestRailUtil.create_testrail_section(project_id, suite_id=suite_id, section_name=section_name)

    # Create TestRail test cases
    print("create_testrail_testcase")
    print(test_case_title)
    print("section_iddd")
    print(section_id)
    TestRailUtil.create_testrail_testcases(project_id,suite_id,section_id, test_case_title=test_case_title)
    print("created successfully")
    # Create TestRail run
    TestRailUtil.create_testrail_run(project_id=project_id, suite_id=suite_id, test_run_name=test_run_name)

    yield


    import pytest

# @pytest.hookimpl(tryfirst=True)
# def pytest_bdd_before_scenario(request, feature, scenario):
#     custom_option = request.config.getoption("--custom-option")
#     print(f"\nBefore Scenario: {feature.name} - {scenario.name}")
#     print(f"Custom Option Value: {custom_option}")

# # Add more hooks as needed...

# def pytest_addoption(parser):
#     parser.addoption("--custom-option", action="store", default=None, help="Custom option description")