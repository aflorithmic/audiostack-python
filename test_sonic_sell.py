"""
This file tests all the functionality of sonicsell and produces one ad
"""

import os
import audiostack


audiostack.api_key = os.environ["AFLR_STAGING_KEY"]

# generate content

advert = audiostack.Content.Script.generate_advert(
    product_name="AWS LAMBDA",
    product_description="i love aws firecracker",
    mood="happy",
)

# voice
voices = audiostack.Speech.Voice.select_for_script(scriptId=advert.data["scriptId"])

# test with tone
voices = audiostack.Speech.Voice.select_for_content(
    content="hello world I am a sonic sell test", tone="confident"
)
# test without tone
voices = audiostack.Speech.Voice.select_for_content(
    content="hello world I am a sonic sell test"
)
# with scriptId
soundTemplates = audiostack.Production.Sound.Template.select_for_script(
    scriptId=advert.data["scriptId"]
)

# with mood
soundTemplates = audiostack.Production.Sound.Template.select_for_content(
    "hello world I am a sonic sell test", mood="exciting"
)
# without mood
soundTemplates = audiostack.Production.Sound.Template.select_for_content(
    "hello world I am a sonic sell test"
)
