'''
A Very simple flask application, providing REST API to our storage
'''
import argparse
from dataclasses import dataclass
from flask import Flask
from flask_restful import Api

from repository import Repository

import apis.v1.requests

@dataclass
class StartupArguments:
    port: int
    debug: bool

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=5000)
    parser.add_argument("--debug", action="store_const", default=False, const=True)
    return parser.parse_args()

def main(startup_arguments: StartupArguments):
    repository = Repository()
    repository.connect()

    app = Flask(__name__)
    api = Api(app)

    # Note that the "get" in the route is not as in GET action
    api.add_resource(apis.v1.requests.Get,
        '/api/v1/requests/get',
        resource_class_args=(repository, ))

    api.add_resource(apis.v1.requests.FrequentWebsite,
        '/api/v1/requests/frequent-website',
        resource_class_args=(repository, ))

    api.add_resource(apis.v1.requests.TimeFrame,
        '/api/v1/requests/time-frame',
        resource_class_args=(repository, ))

    app.run(
        port=startup_arguments.port,
        debug=startup_arguments.debug)

if __name__ == '__main__':
    args = parse_args()
    main(StartupArguments(
        port=args.port,
        debug=args.debug
    ))