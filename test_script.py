import audiostack

audiostack.api_key = "0b1173a6420c4c028690b7beff39c0ad"


# create script item
item = audiostack.Content.Script.create(scriptText="hello sam", projectName="__test")
print(item.response)

# update the script item
item = item.update("hello updated project")
print(item.response)

#delete script item
r = item.delete()
print(r)

# list all script items
script_list = audiostack.Content.Script.list(projectName="__test")
print(script_list.response)

# iterate over responses, script_item will of type Script.Item
for script_item in script_list:
    print(script_item.scriptId, script_item.scriptText[0:200])

