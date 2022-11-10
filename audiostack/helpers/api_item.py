import json

class APIItem():
    
    def __init__(self, response):
        self.response = response
    
    def response(self, indent=0):
        if indent:
            return json.dumps(self.response, indent=indent)
        else:
            return self.response