import pytest
from selenium import webdriver
from appium.options.common import AppiumOptions
import random
import os
import json
import string
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
    feature_file_name = request.config.invocation_params.args[2]
    request.config._pytestbdd_current_feature_name
    print(f"\nAfter Feature: {request.node.name} '@{feature_file_name}' marker and  {request.config._pytestbdd_current_feature_name}.feature")
    print("feature file executed successfully")
    TestRailUtil.add_test_result(testdata["str_testrunID"])

@pytest.fixture(scope='session', autouse=True)
def clear_results_file(request):
    result_data_path = os.path.join(os.path.dirname(__file__), 'result.json')
    if os.path.exists(result_data_path):
        os.remove(result_data_path) 
    yield

@pytest.hookimpl(tryfirst=True)
def pytest_bdd_before_scenario(request, feature, scenario):
    request.config._pytestbdd_current_case_id = None
    request.config._pytestbdd_current_feature_name=feature.name
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
                print

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
    print("your caseee id is")
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

def pytest_runtest_protocol(item, nextitem):
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


testrail_url = os.environ["TESTRAIL_URL"]
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
    TestRailUtil.create_testrail_instance(testrail_url, testrail_username, testrail_password)
    project_id = TestRailUtil.create_testrail_project(project_name)
    print("testsuite")
    print(type(project_id))
    print(project_id)   
    suite_id = TestRailUtil.create_testrail_suite_test(project_id, suite_name=suite_name)
    section_id = TestRailUtil.create_testrail_section(project_id, suite_id=suite_id, section_name=section_name)
    TestRailUtil.create_testrail_testcases(project_id,suite_id,section_id, test_case_title=test_case_title)
    print("created successfully")
    TestRailUtil.create_testrail_run(project_id=project_id, suite_id=suite_id, test_run_name=test_run_name)
    yield
    import pytest