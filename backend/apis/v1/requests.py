from datetime import datetime
import json
from flask import request
from flask_restful import Resource, reqparse

from repository import Repository

class FrequentWebsite(Resource):
    repository: Repository

    def __init__(self, repository: Repository):
        self.repository = repository

    def get(self):
        return self.repository.find_frequent_website()

class TimeFrame(Resource):
    repository: Repository

    def __init__(self, repository: Repository):
        self.repository = repository

    def get(self):
        args = dict(request.args)
        for key in ('from', 'to'):
            if key not in args:
                return f"'{key}' parameter is required", 400

        from_time = datetime.fromisoformat(args['from'])
        to_time = datetime.fromisoformat(args['to'])

        result = self.repository.find_in_time_frame(from_time, to_time)
        dicts = [item.to_dict() for item in result]
        return json.dumps(dicts, default=str)

class Get(Resource):
    '''
    An API for the Get Requests resource.

    This is a terrible name. 
    '''
    repository: Repository

    def __init__(self, repository: Repository):
        self.repository = repository

    def get(self):
        args = dict(request.args)

        entities = []
        if 'id' not in args:
            entities = self.repository.all_get_requests()
        else:
            entity = self.repository.find_get_request_by_id(args['id'])
            if entity is not None:
                entities.append(entity)

        dicts = [entity.to_dict() for entity in entities]
        return json.dumps(dicts, default=str)

    def put(self):
        try:
            data = request.get_json()
            self.repository.insert_get_request(
                id=data["id"],
                timestamp=float(data["timestamp"]),
                duration=float(data["duration"]),
                target_url=data["target_url"],
                response_code=int(data["response_code"]))
            return 'Ok', 200
        except Exception as error:
            # Of course, better error handling will be thought of
            return str(error), 500
