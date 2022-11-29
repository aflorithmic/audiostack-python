import audiostack as aust

aust.api_key = "0b1173a6420c4c028690b7beff39c0ad"


so = aust.Content.Script.create(scriptText="Essa")
print(so)
print(so.__dict__)
