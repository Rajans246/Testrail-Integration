@tester
Feature: trackerwave

  @testrail-C011
  Scenario Outline: User logs into Demo TrackerWave application
    Given I launch Demo TrackerWave App
    When I enter a valid <EMAIL> and <PASSWORD>
    Then I should see the homepage
    Examples:
      | EMAIL    | PASSWORD |
      | username | password |
  
  Scenario Outline: User creates a porter request
    Given I am on the homepage
    When I create a request using following details <Servicegroup> , <Service> , <From> , <Remarks>
    Then I should see the requestId and <Remarks>
    Examples:
      | Servicegroup | Service     | From                                           | Remarks |
      | All          | Hand towels | Baby Room, Ground Floor,Test block,Trackerwave | remarks |