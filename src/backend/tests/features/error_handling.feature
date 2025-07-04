Feature: API Error Handling
  As a client of the Semker API
  I want proper error responses for invalid requests
  So that I can handle errors appropriately

  Background:
    Given the Semker API server is running

  Scenario: Request status for non-existent message
    When I request status for message ID "non-existent-id"
    Then I should get a 404 error
    And the error message should indicate "Message with ID non-existent-id not found"

  Scenario: Request updates for non-existent message
    When I request updates for message ID "invalid-message-id"
    Then I should get a 404 error
    And the error message should indicate "Message with ID invalid-message-id not found"

  Scenario: Submit message with missing message
    When I submit an invalid message without message
    Then I should get a 422 validation error
