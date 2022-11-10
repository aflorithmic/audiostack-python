import audiostack

audiostack.api_key = "0b1173a6420c4c028690b7beff39c0ad"


# t1
response, script_list = audiostack.Content.Script.list(projectName="__test")

for script_item in script_list:
    print(script_item.scriptId)

#response, items = audiostack.Content.Script.list_projects(list_projects