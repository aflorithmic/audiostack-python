import audiostack
import os

audiostack.api_key = os.environ["AUDIO_STACK_DEV_KEY"]

templates = audiostack.Production.Sound.Template.list(type="custom")
print("CUSTOM----\n\n")
for t in templates:
    print("\t", t.templateName, "---", t.description)
    
templates = audiostack.Production.Sound.Template.list(type="standard")
print("STANDARD----\n\n")
for t in templates:
    print("\t", t.templateName, "---", t.description)

r = audiostack.Production.Sound.Parameter.get()
print(r)