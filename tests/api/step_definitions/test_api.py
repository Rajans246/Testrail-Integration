import allure
import requests
import json
from pytest_bdd import given, when, then, parsers, scenarios
import json
import pytest
import os
from datetime import datetime ,timedelta


@pytest.fixture
def context():
    return {}

scenarios('../features/Request.feature')

BASE_URL = "https://demoapi.trackerwave.com"



@given('I construct the payload to create a new porter request')
def load_payload(context):
    print(">>>>>>>>>>>>>>>>>>>>Given>>>>>>>>>>>>>>>>>>>")
    global json_finally
    project_directory=os.getcwd()
    current_directory =os.path.join(project_directory,'tests/api/json_folders')
    print(current_directory)
    file_name="payload_json.json"
    file_path=os.path.join(current_directory,file_name)
    with open(file_path, 'r') as file:
        loaded_payload = json.load(file)

    """updating payload start date and end date"""
    
    def append_current_date_to_json_file(file_path):
    # Read the existing JSON data from the file
        with open(file_path, 'r') as file:
            data = json.load(file)

    # Get current date in the specified format
        current_date = datetime.now() + timedelta(days=1)
        formatted_current_date = current_date.strftime("%Y-%m-%d %H:%M:%S")

    # Calculate tomorrow's date
        tomorrow_date = datetime.now() + timedelta(days=2)
        formatted_tomorrow_date = tomorrow_date.strftime("%Y-%m-%d %H:%M:%S")


    # Append current date to JSON data under the key 'startTime'
        loaded_payload['startTime'] = formatted_current_date

    # Append tomorrow's date to JSON data under the key 'endDate'
        loaded_payload['endTime'] = formatted_tomorrow_date    

    # Write the updated JSON data back to the file
    with open(file_path, 'w') as file:
        json.dump(loaded_payload, file, indent=4)

    # Write the updated JSON data back to the file
    with open(file_path, 'w') as file:
            json.dump(loaded_payload, file, indent=4)    

    # File path to your JSON file
    json_file_path = file_path

    # Call the method to append the current date to the JSON file
    append_current_date_to_json_file(json_file_path)
    load_pay=json.dumps(loaded_payload)
    json_finally=json.loads(load_pay)
    print("json_converted=",json_finally)
    

@when('I hit the new porter post request')
def make_post_request(context):
    print(">>>>>>>>>>>>>>>>>>>>When>>>>>>>>>>>>>>>>>>>")
    global response_content
    headers = {
        "accept": "*/*",
        "Accept-Language": "en-US",
        "facilityId": "0459",
        "Authorization": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImJhZWwta2V5LWlkIn0.eyJhdWQiOlsibXMvYWRtaW4iLCJtcy91c2VyIiwibXcvYWRtaW5hcHAiXSwibGFzdF9sb2dnZWRfaW4iOjE3MDMyNDI2ODEzMDcsInVzZXJfbmFtZSI6IjIiLCJzY29wZSI6WyJyb2xlX2FkbWluIiwicm9sZV9zdXBlcmFkbWluIl0sImV4cCI6MzE0MzI0MjY4MSwiYXV0aG9yaXRpZXMiOlsiU1VQRVJfQURNSU4iXSwianRpIjoiYTUxOTYyN2ItOTRjYi00ZTAyLWI0NTQtYmUwMTNmYTc4MTVkIiwiY2xpZW50X2lkIjoidHdhcHAifQ.XwdL8sPWk5VVh_u5udM4b3OkSKXcuJYIK-L8oWMaN1fkYRlrpBLJnkCtIJJRAi8ZzQ4FSjtDi99JoUNVl9KwJ3O7_TJie6jjXgJxBroC9cvZrpbRO9w_om_8ygbZys0r7Bh5BvzdqrG4aEYjpPFai5ENyKIz_Bd_u64Jk7dlOlebOKjCherXsuYzSK9k9PNVZ2snwVxqAxaI7Ocm1-x8HNjTMXuGFL3iFFKZ-3HQY1mnhF9KfB1umdNvFEWIRs--xJpKir9EaMQLL4_9UAe3XrsunKZiETzsFX74JGWXKnfsYDwYLArCGhQQKe5T-NXbEZxoXbZ6uqb-N81N5rZwgw",
        "Content-Type": "application/json",
    }
    response = requests.post(f"{BASE_URL}/api/porter/porter-requests", json=json_finally, headers=headers)
    allure.attach(f"{response}", name="Status_code", attachment_type=allure.attachment_type.TEXT)   
    print(">>>>>>>>>>>>>",response)
    context['response'] = response
    response_content=response.text
    allure.attach(f"{response_content}", name="Response_Body", attachment_type=allure.attachment_type.TEXT)   
    
@given('I construct the payload ready to be updated')
def load_payload(context):
    print(">>>>>>>>>>>>>>>>>>>>Given>>>>>>>>>>>>>>>>>>>")
    global json_finally
    # context.load_payload=None
    project_directory=os.getcwd()
    current_directory =os.path.join(project_directory,'tests/api/json_folders')
    print(current_directory)
    file_name="payload_json_put.json"
    # file_path="test\\json_folders\\payload_json_put.json"
    file_path=os.path.join(current_directory,file_name)
    with open(file_path, 'r') as file:
        loaded_payload = json.load(file)
        load_pay=json.dumps(loaded_payload)
        json_finally=json.loads(load_pay)
        print("json_converted=",json_finally)
        

@when('I hit the update put request')
def step_when_send_put_request(context):
    print("PUT")
    global response_content
    
    headers_put = {
        "accept": "*/*",
        "Accept-Language": "en-US",
        "facilityId": "0459",
        "Authorization": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImJhZWwta2V5LWlkIn0.eyJhdWQiOlsibXMvYWRtaW4iLCJtcy91c2VyIiwibXcvYWRtaW5hcHAiXSwibGFzdF9sb2dnZWRfaW4iOjE3MDMyNDI2ODEzMDcsInVzZXJfbmFtZSI6IjIiLCJzY29wZSI6WyJyb2xlX2FkbWluIiwicm9sZV9zdXBlcmFkbWluIl0sImV4cCI6MzE0MzI0MjY4MSwiYXV0aG9yaXRpZXMiOlsiU1VQRVJfQURNSU4iXSwianRpIjoiYTUxOTYyN2ItOTRjYi00ZTAyLWI0NTQtYmUwMTNmYTc4MTVkIiwiY2xpZW50X2lkIjoidHdhcHAifQ.XwdL8sPWk5VVh_u5udM4b3OkSKXcuJYIK-L8oWMaN1fkYRlrpBLJnkCtIJJRAi8ZzQ4FSjtDi99JoUNVl9KwJ3O7_TJie6jjXgJxBroC9cvZrpbRO9w_om_8ygbZys0r7Bh5BvzdqrG4aEYjpPFai5ENyKIz_Bd_u64Jk7dlOlebOKjCherXsuYzSK9k9PNVZ2snwVxqAxaI7Ocm1-x8HNjTMXuGFL3iFFKZ-3HQY1mnhF9KfB1umdNvFEWIRs--xJpKir9EaMQLL4_9UAe3XrsunKZiETzsFX74JGWXKnfsYDwYLArCGhQQKe5T-NXbEZxoXbZ6uqb-N81N5rZwgw",
        "Content-Type": "application/json",
    }

    response= requests.put(f"{BASE_URL}/api/porter/porter-requests/32287", json=json_finally, headers=headers_put)
    allure.attach(f"{response}", name="Status_code", attachment_type=allure.attachment_type.TEXT)   
    print(">>>>>>>>>>>>>",response)
    context['response'] = response
    response_content=response.text
    allure.attach(f"{response_content}", name="Response_Body", attachment_type=allure.attachment_type.TEXT)   

@then(parsers.parse('I should get "{response_body}" with success status code to be "{status_code_success}"'))
def step_then_verify_status_code(context, status_code_success,response_body):
    assert 'response' in context and isinstance(context['response'], requests.Response), "No valid response found in context"
    assert context['response'].status_code == int(status_code_success), f"Request failed with status code: {context['response_put'].status_code}"
    response_data = context['response'].json()
    print("Response_data=",response_data)
    desired_key = ['status',response_body]
    for word in desired_key:
        print("json_contains:",word)
        assert word in response_content, f"Expected word '{word}' not found in response content"
        allure.attach(f"{word}", name="Request Details Saved successfully Message", attachment_type=allure.attachment_type.TEXT) 