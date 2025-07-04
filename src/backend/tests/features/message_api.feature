Feature: Message Processing API
  As a client of the Semker API
  I want to submit messages for asynchronous processing
  So that I can get processing updates and results

  Background:
    Given the Semker API server is running
    And the API is accessible at "http://localhost:8000"

  Scenario: Submit a message for processing
    When I submit a message with content "Hello, Behave test!" from sender "behave_test"
    Then I should receive a message ID
    And the response status should be "received"
    And the response should include a timestamp

  Scenario: Get message status
    Given I have submitted a message with content "Test message" from sender "test_user"
    When I request the message status
    Then I should get the message details
    And the status should be either "received" or "processed"

  Scenario: Get processing updates
    Given I have submitted a message with content "Update test message" from sender "update_test"
    When I request updates for the message
    Then I should get a list of updates
    And eventually the message should be processed

  Scenario: List all messages
    Given I have submitted multiple messages
    When I request the list of all messages
    Then I should get a summary of all messages
    And the response should include total message count

  Scenario: Health check endpoint
    When I check the health endpoint
    Then the service should respond with status "healthy"
    And the response should include uptime information
    And the response should include version information
