"""Step definitions for the Semker API BDD tests."""

import time
from datetime import datetime
from typing import Any, Dict, List

import requests
from behave import given, when, then  # type: ignore


# Base URL for the API
base_url: str = "http://localhost:8000"


def get_test_headers() -> Dict[str, str]:
    """Generate test headers with required conversation ID."""
    import uuid
    return {
        "x-ms-conversation-id": str(uuid.uuid4()),
        "Content-Type": "application/json"
    }


@given('the Semker API server is running')  # type: ignore
def step_given_server_running(context: Any) -> None:
    """Verify that the API server is accessible"""
    try:
        response: requests.Response = requests.get(f"{base_url}/health", timeout=5)
        assert response.status_code == 200
        context.server_running = True
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        context.server_running = False
        assert False, "API server is not running or not accessible"


@given('the API is accessible at "{url}"')  # type: ignore
def step_given_api_accessible(context: Any, url: str) -> None:
    """Set the API base URL"""
    global base_url
    base_url = url
    context.base_url = url


@given('I have submitted a message with message "{message}"')  # type: ignore
def step_given_message_submitted(context: Any, message: str) -> None:
    """Submit a message and store the response"""
    message_data: Dict[str, str] = {
        "message": message
    }
    
    headers = get_test_headers()
    response: requests.Response = requests.post(f"{base_url}/messages", json=message_data, headers=headers)
    assert response.status_code == 201
    
    context.submitted_message = response.json()
    context.message_id = context.submitted_message["message_id"]


@given('I have submitted multiple messages')  # type: ignore
def step_given_multiple_messages_submitted(context: Any) -> None:
    """Submit multiple messages for testing"""
    messages: List[Dict[str, str]] = [
        {"message": "First test message"},
        {"message": "Second test message"},
        {"message": "Third test message"}
    ]
    
    # Initialize list without type annotation on assignment
    submitted_messages: List[Dict[str, Any]] = []
    for message_data in messages:
        response: requests.Response = requests.post(f"{base_url}/messages", json=message_data, headers=get_test_headers())
        assert response.status_code == 201
        submitted_messages.append(response.json())
    
    context.submitted_messages = submitted_messages


@when('I submit a message with message "{message}"')  # type: ignore
def step_when_submit_message(context: Any, message: str) -> None:
    """Submit a message to the API"""
    message_data: Dict[str, str] = {
        "message": message
    }
    
    context.response = requests.post(f"{base_url}/messages", json=message_data, headers=get_test_headers())
    if context.response.status_code == 201:
        context.response_data = context.response.json()


@when('I submit an invalid message without message')  # type: ignore
def step_when_submit_invalid_message_no_message(context: Any) -> None:
    """Submit a message without message field"""
    message_data: Dict[str, str] = {}
    
    context.response = requests.post(f"{base_url}/messages", json=message_data)



@when('I request the message status')  # type: ignore
def step_when_request_message_status(context: Any) -> None:
    """Request status for a previously submitted message"""
    assert hasattr(context, 'message_id'), "No message ID available"
    
    context.response = requests.get(f"{base_url}/messages/{context.message_id}/status")
    if context.response.status_code == 200:
        context.response_data = context.response.json()


@when('I request status for message ID "{message_id}"')  # type: ignore
def step_when_request_status_for_id(context: Any, message_id: str) -> None:
    """Request status for a specific message ID"""
    context.response = requests.get(f"{base_url}/messages/{message_id}/status")


@when('I request updates for the message')  # type: ignore
def step_when_request_updates(context: Any) -> None:
    """Request updates for a previously submitted message"""
    assert hasattr(context, 'message_id'), "No message ID available"
    
    context.response = requests.get(f"{base_url}/messages/{context.message_id}/updates")
    if context.response.status_code == 200:
        context.response_data = context.response.json()


@when('I request updates for message ID "{message_id}"')  # type: ignore
def step_when_request_updates_for_id(context: Any, message_id: str) -> None:
    """Request updates for a specific message ID"""
    context.response = requests.get(f"{base_url}/messages/{message_id}/updates")


@when('I request the list of all messages')  # type: ignore
def step_when_request_all_messages(context: Any) -> None:
    """Request the list of all messages"""
    context.response = requests.get(f"{base_url}/messages")
    if context.response.status_code == 200:
        context.response_data = context.response.json()


@when('I check the health endpoint')  # type: ignore
def step_when_check_health(context: Any) -> None:
    """Check the health endpoint"""
    context.response = requests.get(f"{base_url}/health")
    if context.response.status_code == 200:
        context.response_data = context.response.json()


@then('I should receive a message ID')  # type: ignore
def step_then_receive_message_id(context: Any) -> None:
    """Verify that a message ID was returned"""
    assert context.response.status_code == 201
    assert "message_id" in context.response_data
    assert context.response_data["message_id"] is not None
    context.message_id = context.response_data["message_id"]


@then('the response status should be "{expected_status}"')  # type: ignore
def step_then_response_status(context: Any, expected_status: str) -> None:
    """Verify the response status field"""
    assert "status" in context.response_data
    assert context.response_data["status"] == expected_status


@then('the response should include a timestamp')  # type: ignore
def step_then_response_includes_timestamp(context: Any) -> None:
    """Verify that a timestamp is included in the response"""
    assert "received_at" in context.response_data
    # Verify it's a valid datetime string
    datetime.fromisoformat(context.response_data["received_at"].replace('Z', '+00:00'))


@then('I should get the message details')  # type: ignore
def step_then_get_message_details(context: Any) -> None:
    """Verify that message details are returned"""
    assert context.response.status_code == 200
    assert "message_id" in context.response_data
    assert "status" in context.response_data
    assert "content" in context.response_data
    assert "timestamp" in context.response_data


@then('the status should be either "{status1}" or "{status2}" or "{status3}"')  # type: ignore
def step_then_status_one_of_three(context: Any, status1: str, status2: str, status3: str) -> None:
    """Verify the status is one of the three expected values"""
    actual_status: str = context.response_data["status"]
    assert actual_status in [status1, status2, status3], f"Status '{actual_status}' is not one of '{status1}', '{status2}', or '{status3}'"


@then('the status should be either "{status1}" or "{status2}"')  # type: ignore
def step_then_status_either_or(context: Any, status1: str, status2: str) -> None:
    """Verify the status is one of the expected values"""
    actual_status: str = context.response_data["status"]
    assert actual_status in [status1, status2], f"Status '{actual_status}' is not '{status1}' or '{status2}'"


@then('I should get a list of updates')  # type: ignore
def step_then_get_list_of_updates(context: Any) -> None:
    """Verify that a list of updates is returned"""
    assert context.response.status_code == 200
    assert isinstance(context.response_data, list)


@then('eventually the message should be processed')  # type: ignore
def step_then_eventually_processed(context: Any) -> None:
    """Wait for message processing and verify completion"""
    max_attempts: int = 10
    for _ in range(max_attempts):
        response: requests.Response = requests.get(f"{base_url}/messages/{context.message_id}/updates")
        if response.status_code == 200:
            updates: List[Any] = response.json()
            if updates and any(update["status"] in ["completed", "failed"] for update in updates):
                return
        time.sleep(1)
    
    assert False, "Message was not processed within the expected time"


@then('I should get a summary of all messages')  # type: ignore
def step_then_get_summary_all_messages(context: Any) -> None:
    """Verify that a summary of all messages is returned"""
    assert context.response.status_code == 200
    assert "messages" in context.response_data
    assert isinstance(context.response_data["messages"], list)


@then('the response should include total message count')  # type: ignore
def step_then_response_includes_total_count(context: Any) -> None:
    """Verify that total message count is included"""
    assert "total_messages" in context.response_data
    assert isinstance(context.response_data["total_messages"], int)


@then('the service should respond with status "{expected_status}"')  # type: ignore
def step_then_service_status(context: Any, expected_status: str) -> None:
    """Verify the service health status"""
    assert context.response.status_code == 200
    assert context.response_data["status"] == expected_status


@then('the response should include uptime information')  # type: ignore
def step_then_response_includes_uptime(context: Any) -> None:
    """Verify that uptime information is included"""
    assert "uptime_seconds" in context.response_data
    assert isinstance(context.response_data["uptime_seconds"], (int, float))


@then('the response should include version information')  # type: ignore
def step_then_response_includes_version(context: Any) -> None:
    """Verify that version information is included"""
    assert "version" in context.response_data
    assert context.response_data["version"] is not None


@then('I should get a {status_code:d} error')  # type: ignore
def step_then_get_error(context: Any, status_code: int) -> None:
    """Verify that the expected error status code is returned"""
    assert context.response.status_code == status_code


@then('I should get a 422 validation error')  # type: ignore
def step_then_get_validation_error(context: Any) -> None:
    """Verify that a 422 validation error is returned"""
    assert context.response.status_code == 422


@then('the error message should indicate "{expected_message}"')  # type: ignore
def step_then_error_message_indicates(context: Any, expected_message: str) -> None:
    """Verify that the error message contains expected text"""
    if context.response.headers.get('content-type', '').startswith('application/json'):
        error_data: Dict[str, Any] = context.response.json()
        assert "detail" in error_data
        assert expected_message in error_data["detail"]
