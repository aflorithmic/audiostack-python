import json


class APIResponseItem:
    def __init__(self, response):
        self.response = response

        if "data" in response:
            self.data = self.response["data"]
        if "message" in response:
            self.message = self.response["message"]
        if "meta" in response:
            self.meta = self.response["meta"]

            # for key in self.data:
            #     assert key != "data"
            #     self.__dict__[key] = self.data["key"]

    def print_response(self, indent=0):
        if indent:
            return json.dumps(self.response, indent=indent)
        else:
            return self.response

    def __str__(self) -> str:
        return json.dumps(self.response)
