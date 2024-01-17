@API
Feature: Testing POST Request

@post
Scenario: Creating a new porter request
   Given I construct the payload to create a new porter request
   When I hit the new porter post request
   Then I should get "Request Details Saved successfully" with success status code to be "200"
   
@put
 Scenario: Updating data with a PUT request
   Given I construct the payload ready to be updated
   When I hit the update put request
   Then I should get "Request updated successfully" with success status code to be "200"