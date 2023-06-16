import json


class APIResponseItem:
    def __init__(self, response):
        self.response = response
        self.status_code = response["statusCode"]
        
        if "data" in response:
            self.data = self.response["data"]
        if "message" in response:
            self.message = self.response["message"]
        if "meta" in response:
            self.meta = self.response["meta"]
        if "bytes" in response:
            self.bytes = self.response["bytes"]

    def print_response(self, indent=0):
        if indent:
            return json.dumps(self.response, indent=indent)
        else:
            return self.response

    def __str__(self) -> str:
        if hasattr(self, "bytes"):
            return "bytes object"
        else:
            return json.dumps(self.response)
