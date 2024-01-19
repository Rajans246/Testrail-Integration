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
from tests.testrail_util import TestRailUtil  # Itestdata_pathmport the TestRailUtil class



testdata_path = os.path.join(os.path.dirname(__file__), 'testdata.json')
with open(testdata_path, 'r') as file:
    testdata = json.load(file)

for key, value in testdata.items():
    os.environ[key] = value

def pytest_configure(config):
    config.addinivalue_line(
        "markers", "testrail(case_id): associate a TestRail case ID with a scenario"
    )

@pytest.fixture(scope="session", autouse=True)
def after_feature(request):
    yield
    # Perform actions or cleanup after the execution of the entire feature file
    print(f"\nAfter Feature: {request.node.name}")
    print("feature file executed successfully")


@pytest.fixture()
def clear_results_file_at_session_start():
    results_file_path = os.path.join(os.path.dirname(__file__), 'result.json')
    # Open the file in write mode to clear its content
    with open(results_file_path, 'w') as json_file:
        json_file.write('{}') 


@pytest.hookimpl(tryfirst=True)
def pytest_bdd_before_scenario(request, feature, scenario):
    request.config._pytestbdd_current_case_id = None
    global current_case_id 
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
                current_case_id = tag[10:]  # Extract the TestRail case ID from the tag
                print("mytestrun rest")
                print(f"TestRail Case ID: {current_case_id}")
                
                print("request.config._pytestbdd_current_case_id")
                print(request.config._pytestbdd_current_case_id)
                request.config._pytestbdd_current_case_id = current_case_id
                print(request.config._pytestbdd_current_case_id)
                # TestRailUtil.save_test_case_id(current_case_id)
                print
            #     break
        #     if 'testrail-C' in scenario.tags:
        # # Extract case ID from the testrail tag
        #       case_id = scenario.tags['testrail-C']
        # # Set the current_case_id in the request.config
            #   print(case_id)

@pytest.hookimpl(tryfirst=True)
def pytest_bdd_after_step(request, feature, scenario, step, step_func, step_func_args):
    current_case_id = getattr(request.config, '_pytestbdd_current_case_id', None)
    try:
        result_data_path = os.path.join(os.path.dirname(__file__), 'result.json')
        with open(result_data_path, "r") as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        data = {}

    data.setdefault("results", [])
    status_id = 1 if not step.failed else 5  # Assuming '1' is the status_id for passed

    # current_case_id = request.config._pytestbdd_current_case_id
    print("your caseee id isss")
    print(current_case_id)

    if current_case_id:
        for result in data["results"]:
            if result["case_id"] == current_case_id:
                result["status_id"] = status_id
                break
        else:
            data["results"].append({"case_id": current_case_id, "status_id": status_id})

    with open(result_data_path, "w") as json_file:
        json.dump(data, json_file)
    # global current_case_id
    # try:
    #     result_data = os.path.join(os.path.dirname(__file__), 'result.json')
    #     with open(result_data, "r") as json_file:
    #         data = json.load(json_file)
    # except FileNotFoundError:
    #     # If result.json doesn't exist, initialize with an empty list
    #     data = {}

    # data.setdefault("results", [])
    # exception = None
    # # try:
    # #     result = yield
    # # except Exception as e:
    # #     exception = e
    # if step.failed or exception:
    #     status_id = 5 
    #     print(f"Failed After Step: {feature.name} - {scenario.name} - {step.keyword} {step.name} {status_id} FAILED")
    # else:
    #     status_id = 1  # Assuming '1' is the status_id for passed
    #     print(f"Passed After Step: {feature.name} - {scenario.name} - {step.keyword} {step.name} {status_id} PASSED")
    # if current_case_id:
    #         # Update the status_id for the corresponding case_id
    #         for result in data["results"]:
    #             if result["case_id"] == current_case_id:
    #                 result["status_id"] = status_id  # Assuming '5' is the status_id for failed
    #                 break
    #         else:
    #             # If case_id not found, add a new result entry
    #             data["results"].append({"case_id": current_case_id, "status_id": status_id})

    # # if step.exception:
    # # if step.Exception:
    #     # print(f"Step failed due to exception: {Exception}")
    #     # print(f"After Step: {feature.name} - {scenario.name} - {step.keyword} {step.name}  FAILED")
    #     # print("Custom Option Value:", request.config.getoption('--custom-option'))
    #     # print()
    # # else:
    # #     print(f"After Step: {feature.name} - {scenario.name} - {step.keyword} {step.name} PASSED")
    # #     if current_case_id:
    # #         # Update the status_id for the corresponding case_id
    # #         for result in data["results"]:
    # #             if result["case_id"] == current_case_id:
    # #                 result["status_id"] = 1  # Assuming '1' is the status_id for passed
    # #                 break
    # #         else:
    # #             # If case_id not found, add a new result entry
    # #             data["results"].append({"case_id": current_case_id, "status_id": 1})
    
    # with open("result.json", "w") as json_file:
    #     json.dump(data, json_file)
    
    # current_case_id = None 
        # print("Custom Option Value:", request.config.getoption('--custom-option'))
        # print("PASSED")
@pytest.hookimpl
def pytest_bdd_step_error(request, feature, scenario, step, step_func, step_func_args, exception):
    current_case_id = request.config._pytestbdd_current_case_id
    if current_case_id:
        try:
            testdata_path = os.path.join(os.path.dirname(__file__), 'result.json')
            with open(testdata_path, "r") as json_file:
                data = json.load(json_file)
        except FileNotFoundError:
            data = {}
        data.setdefault("results", [])

        for result in data["results"]:
            if result["case_id"] == current_case_id:
                result["status_id"] = 5  # Assuming '5' is the status_id for failed
                break
        else:
            data["results"].append({"case_id": current_case_id, "status_id": 5})

        with open(testdata_path, "w") as json_file:
            json.dump(data, json_file)
    # global current_case_id
    # print(f"Step: {step.keyword} {step.name} encountered an error.")
    # # print(f"Arguments passed to step function: {step_func_args}")
    # # print(f"Failed After Step: {feature.name} - {scenario.name} - {step.keyword} {step.name} FAILED")
    # print("your current case id is")
    # print(current_case_id)
    # print(f"Exception: {exception}")
    # # data = {}
    # if current_case_id:
    #     try:
    #         testdata_path = os.path.join(os.path.dirname(__file__), 'testdata.json')
    #         with open(testdata_path, "r") as json_file:
    #             data = json.load(json_file)
    #         print("your data")
    #         print(data)
    #     except FileNotFoundError:
    #         # If result.json doesn't exist, initialize with an empty dictionary
    #         data = {}
    #     data.setdefault("results", [])
    #     for result in data["results"]:
    #         print("entered in to the resultssss")
    #         if result["case_id"] == current_case_id:
    #             result["status_id"] = 5  # Assuming '5' is the status_id for failed
    #             break
    #     else:
    #         # If case_id not found, add a new result entry with status_id = 5
    #         data["results"].append({"case_id": current_case_id, "status_id": 5})
    #         print("newlyentered")

    # with open("result.json", "w") as json_file:
    #         json.dump(data, json_file)

    # print(f"After Step Failed: {feature.name} - {scenario.name} - {step.keyword} {step.name} FAILED")

    # current_case_id = None

# def pytest_bdd_apply_tag(tag, function):
#     if tag.startswith('testrail-C'):
#         # Extract case ID from the tag
#         case_id = tag.split('-C')[1]
#         # Set the current_case_id in the request.config
#         request.config._pytestbdd_current_case_id = case_id
#     return True

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