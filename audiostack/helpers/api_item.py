import json

class APIResponseItem():
    
    def __init__(self, response):
        self.response = response
        
        if "data" in response:
            self.data = self.response["data"]
    
    def response(self, indent=0):
        if indent:
            return json.dumps(self.response, indent=indent)
        else:
            return self.response
                

#class APIList():