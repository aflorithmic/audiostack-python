import os

sdk_version = os.environ["CIRCLE_TAG"]
print(sdk_version)
sdk_version.split("v")[-1]

with open("audiostack/__init__.py", "r") as f:
    lines = f.readlines()
    lines[0] = f"""sdk_version =  "{sdk_version}"""

print(lines)
