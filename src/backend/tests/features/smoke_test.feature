Feature: Basic API Test
  As a developer
  I want to verify the basic API functionality
  So that I can ensure the BDD test setup is working

  @smoke
  Scenario: API is accessible
    Given the Semker API server is running
    When I check the health endpoint
    Then the service should respond with status "healthy"
