import typing
import aiohttp
import requests

class OpenRobotAPIError(Exception):
    """Base OpenRobot API Exception."""

class Forbidden(OpenRobotAPIError):
    """Recieved an 403 Error code from the API."""
    def __init__(self, resp, json_error):
        self.raw: dict = json_error
        self.response: typing.Union[aiohttp.ClientResponse, requests.Response] = resp
        self.message: str = json_error['message']
        self.error_code: int = json_error['error']['code']

        super().__init__(self.message)

class BadRequest(OpenRobotAPIError):
    """Recieved an 400 Error code from the API."""
    def __init__(self, resp, json_error):
        self.raw: dict = json_error
        self.response: typing.Union[aiohttp.ClientResponse, requests.Response] = resp
        self.message: str = json_error['message']
        self.error_code: int = json_error['error']['code']

        super().__init__(self.message)

class InternalServerError(OpenRobotAPIError):
    """Recieved an 500 Error code from the API."""
    def __init__(self, resp, json_error):
        self.raw: dict = json_error
        self.response: typing.Union[aiohttp.ClientResponse, requests.Response] = resp
        self.message: str = json_error['message']
        self.error_code: int = json_error['error']['code']

        super().__init__(self.message)

class NoTokenProvided(OpenRobotAPIError):
    """No token was provided."""
    def __init__(self):
        super().__init__('No token was provided.')