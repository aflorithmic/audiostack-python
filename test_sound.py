import audiostack
import os

audiostack.api_key = os.environ["AUDIO_STACK_DEV_KEY"]

# list templates that are custom (user uploaded)
templates = audiostack.Production.Sound.Template.list(type="custom")
print("CUSTOM----\n\n")
for t in templates:
    print("\t", t.templateName, "---", t.description)
    
# list public templates
templates = audiostack.Production.Sound.Template.list(type="standard")
print("STANDARD----\n\n")
for t in templates:
    print("\t", t.templateName, "---", t.description)

# list sound parameters
r = audiostack.Production.Sound.Parameter.get()
print(r.data)

print("Cost for this session: ", audiostack.credits_used_in_this_session())
