from .api_item import APIResponseItem


class APIResponseList(APIResponseItem):
    def __init__(self, response, list_type):
        super().__init__(response)
        self.idx = 0
        self.list_type = list_type
        self.items = self.response["data"][list_type]

    def __iter__(self):
        return self

    def __next__(self):
        self.idx += 1
        try:
            item = self.items[self.idx - 1]
            return self.resolve_item(self.list_type, item)

        except IndexError:
            self.idx = 0
            raise StopIteration

    def __getitem__(self, x):
        if isinstance(x, slice):
            return [
                self.resolve_item(self.list_type, x)
                for x in self.items[x.start : x.stop]
            ]
        else:
            return self.resolve_item(self.list_type, x)

    # child classes should override this method, failing to do so will raise an exception!
    def resolve_item(self, list_type):
        raise Exception()
