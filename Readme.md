<!-- Goals: -->

#### Mobile:
pytest --browser Mobile -k "mobile" -v -s -p no:allure_pytest --alluredir=allure_report\mobile

Mobile report: allure serve allure_report\mobile 


#### API:
pytest --alluredir=allure_report/Api/ -k 'API' -v -s -p no:allure_pytest 
 
API report : allure serve allure_report\Api
 
 
#### Web:
pytest --browser Chrome --env demo -k "tester" -v -s -p no:allure_pytest  --alluredir=allure_report/WEB/

Web report : allure serve allure_report\WEB

#### To activate Environment
.venv\scripts\activate


#### To install dependencies
pip install -r requirements.txt


PS: For running locally on your device you'd need the following tools
- Android: ADB, Appium Server
- iOS: Appium Server, Xcode

The instances have to be running for a successful execution.


### Test Reports
The test report can be accessed from the jenkins matching the parameters above.