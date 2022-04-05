'''
Enhancement for the requests module
'''

from time import time
from typing import Callable, Dict, Sequence
from uuid import uuid4 as generate_uuid
import wrapt
import requests

from webcheck.model import GetRequestEntity
from webcheck.enhancements.registry import enhancement, Context

def get_decorator(context: Context):
    def wrapper(
            wrapped: Callable[[any], requests.Response], 
            instance: any, 
            args: Sequence[any], 
            kwargs: Dict[any, any]):

        nonlocal context
        timestamp = time()
        result = wrapped(*args, **kwargs)
        
        if '__unwrap' not in kwargs:
            context.bus.emit("intercepted.get-request", GetRequestEntity(
                id=str(generate_uuid()),
                timestamp=timestamp,
                duration=time() - timestamp,
                target_url=result.url,
                response_code=result.status_code
            ))

        return result
    return wrapper

@enhancement
def enhance_get_function(context: Context):
    wrapt.wrap_function_wrapper('requests', 'get', get_decorator(context))