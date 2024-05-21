import os
import subprocess

poetry_version = subprocess.run(
    ["poetry", "version", "--short"], capture_output=True, text=True
).stdout.rstrip("\n")
sdk_version = os.environ["CIRCLE_TAG"]
print(sdk_version)
sdk_version = sdk_version.split("v")[-1]

if sdk_version != poetry_version:
    raise RuntimeError(
        f"CIRCLE_TAG (from git) `{sdk_version}` does not match poetry version (from pyproject.toml) `{poetry_version}`."
    )

with open("audiostack/__init__.py", "r") as f:
    lines = f.readlines()
    lines[0] = f"""sdk_version = "{sdk_version}"\n"""


with open("audiostack/__init__.py", "w") as f:
    f.writelines(lines)
