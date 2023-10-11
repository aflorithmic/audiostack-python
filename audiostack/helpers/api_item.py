import json


class APIResponseItem:
    def __init__(self, response):
        self.response = response
        
        # extra specific fields
        self.status_code = response.get("statusCode", 0)
        self.data = response.get("data", {})
        self.message = response.get("message", "")
        self.meta = response.get("meta", {})
        self.bytes = response.get("bytes", None)
        

    def print_response(self, indent=0):
        if indent:
            return json.dumps(self.response, indent=indent)
        else:
            return self.response

    def __str__(self) -> str:
        if self.bytes:
            return "bytes object"
        else:
            return json.dumps(self.response)
