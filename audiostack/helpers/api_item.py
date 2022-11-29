import json


class APIResponseItem:
    def __init__(self, response):
        self.response = response
        if "data" in response:
            self.data = self.response["data"]
            # for key in self.data:
            #     assert key != "data"
            #     self.__dict__[key] = self.data["key"]

    def response(self, indent=0):
        if indent:
            return json.dumps(self.response, indent=indent)
        else:
            return self.response


# class APIList():
