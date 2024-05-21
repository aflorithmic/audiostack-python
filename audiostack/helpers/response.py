import json


class Response:
    statusCode: int

    # mututally exclusive
    errors: list = []
    data: dict = {}

    meta: dict
    message: str
    warnings: list

    def __repr__(self) -> str:
        if self.statusCode >= 200:
            return json.dumps({"data": self.data})
        else:
            return ""

    def __str__(self) -> str:
        return "member of Test"
