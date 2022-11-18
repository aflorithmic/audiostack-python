import os
import audiostack
import json

audiostack.api_key = os.environ["AUDIO_STACK_DEV_KEY"]

r = audiostack.Documentation.docs_for_service(audiostack.Content.Script)
print(json.dumps(r, indent=4))