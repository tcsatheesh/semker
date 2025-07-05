from uuid import uuid4
from datetime import datetime, timezone
import json
import logging
import httpx

from typing import Dict, Any


class JsonFormatter(logging.Formatter):
    def format(
        self,
        record: logging.LogRecord,
    ) -> str:
        _log_record: dict[str, str] = {
            "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S.%f"),
            "message": json.loads(record.getMessage()),
        }
        return json.dumps(_log_record)


_logger = logging.getLogger("openai.httpx")
_file_handler = logging.FileHandler("httpx.jsonl")
_file_handler.setLevel(logging.INFO)
_json_formatter = JsonFormatter()
_file_handler.setFormatter(_json_formatter)
_logger.addHandler(_file_handler)


async def request_interceptor(request: httpx.Request) -> None:
    """
    An asynchronous function to intercept outgoing requests.
    """
    if not request.headers.get("x-ms-request-id"):
        request.headers["x-ms-request-id"] = str(uuid4())


async def response_interceptor(response: httpx.Response) -> None:
    """
    An asynchronous function to intercept incoming responses.
    """
    cloned_response = None
    try:
        # Clone the response to safely read content without blocking further processing
        # Note: This might not be suitable for very large streaming responses.
        cloned_response = await response.aread()  # Ensures content is loaded
    except Exception as e:
        _logger.warning(f"  Could not read response body for logging: {e}")

    # Check for specific status codes
    if response.status_code >= 400:
        _logger.error(f"  Request failed with status code: {response.status_code}")

    _request_body = response.request.content.decode("utf-8")
    _response_body = cloned_response.decode("utf-8") if cloned_response else None
    _rr: Dict[str, Dict[str,Any ]] = {
        "Request": {
            "Method": response.request.method,
            "URL": str(response.request.url),
            "Headers": dict(response.request.headers),
            "Body": json.loads(_request_body),
        },
        "Response": {
            "Status Code": response.status_code,
            "Headers": dict(response.headers),
            "Body": json.loads(cloned_response) if cloned_response else None,
        },
    }
    _logger.info(json.dumps(_rr))


async def error_interceptor(request: httpx.Request, exc: httpx.RequestError) -> None:
    """
    An asynchronous function to intercept errors during requests.
    """
    _logger.error(f"Request Error: {request.method} {request.url} - {exc}")
