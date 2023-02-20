import json


class Response:
    statusCode: int

    # mututally exclusive
    errors: list = []
    data: dict = {}

    meta: dict
    message: str
    warnings: list

    def __repr__(self):
        if self.statusCode >= 200:
            return json.dumps({"data": self.data})

    def __str__(self):
        return "member of Test"
