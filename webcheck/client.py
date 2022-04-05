import json
import requests

from .model import GetRequestEntity

DEFAULT_HEADERS = {
    "Content-Type": "application/json"
}

class Client:

    """
    Server's address
    """
    address: str

    def __init__(self, address: str):
        self.address = address
    
    def put_get_request(self, payload: GetRequestEntity):
        '''
        Notify backend on a new GetRequestEntity 
        '''
        response = requests.put(f"{self.address}/api/v1/requests/get",
            headers=DEFAULT_HEADERS,
            data=json.dumps(payload.__dict__))

        if response.status_code != 200:
            raise Exception(f"Server failed with code {response.status_code}. {response.text}")