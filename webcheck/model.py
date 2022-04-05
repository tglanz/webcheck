'''
Core model for the application.

Shouldn't have dependencies on the rest of the application objects.
'''
from dataclasses import dataclass

@dataclass
class GetRequestEntity:
    '''
    An entity describing a GET request 
    '''
    id: str
    timestamp: float
    duration: float
    target_url: str
    response_code: int
