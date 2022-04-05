'''
Bootstrapping logic.

Even if we decided not to load everything on import,
we can expose to the user a single function "bootstrap".

In adition, bootstrapper only bootstraps (makes sense) other objects in the application,
it doesn't have it's own logic - Ideally at least, here it performs the event muxing and decides
on the server's address. In a real project this should be externalize.

Even without a bootstrapper, On different circumstances, a consumer of the package could make his own bootstrapping logic.
This is especially true for development purposes, tests or advanced usage of the underlying features of this package.

To give some examples -
1. For tests, we could bootstrap the application with a mock client and assert performed requests
2. A user who would want to intercept the data himself can add another listener to the bus
3. A developer who would like to try different enhancement logic can replace a single enhancer
4. etc...
'''
import os
import logging
import pymitter

from .client import Client
from .enhancements import registry

def get_server_address() -> str:
    '''
    Other forms of configuration can be provided.
    Also, centralization of all configurations is preferred, but I seemed an overkill.
    '''
    return os.environ.get('WEBCHECK_SERVER_ADDRESS', 'http://localhost:5000')

def with_suppressed_errors(body):
    def suppressed(*args, **kwargs):
        try:
            body(*args, **kwargs)
        except Exception as error:
            logging.warn(error)
    return suppressed
    
def bootstrap():
    '''
    Bootstrap application with all known enhancers
    '''
    client = Client(get_server_address())
    bus = pymitter.EventEmitter()

    # TODO: Probably, in a more complex environment they mux logic should be externalized.
    # Anyway, we suppress the errors as well and log them. We don't want to interrupt
    # the user's normal flow of operation.
    bus.on('intercepted.get-request', with_suppressed_errors(client.put_get_request))

    context = registry.Context(bus)

    for enhance in registry.get_known_enhancements():
        enhance(context)
    