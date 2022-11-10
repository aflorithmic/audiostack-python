import json

class APIResponse():
    
    def __init__(self, response):
        self.response = response
        self.data = self.response["data"]
    
    def response(self, indent=0):
        if indent:
            return json.dumps(self.response, indent=indent)
        else:
            return self.response
        
#class APIList():