from flask import json, Response


class ApiResponse(Response):
    def __init__(self, data=None, **kwargs):
        if isinstance(data, str):
            # assume `data` a status message for the user
            kwargs['response'] = json.dumps({'message': data})
        else:
            # just convert it to JSON
            kwargs['response'] = json.dumps(data)
        super(ApiResponse, self).__init__(**kwargs)