import audiostack
import os


audiostack.api_key = os.environ["AUDIO_STACK_DEV_KEY"]
audiostack.assume_org_id = "my_other_org_id" 

text = """<as:section name="main"> 
  Feeling Hungry, looking for something to eat!
  why not try our new double quarter pounder from <as:placeholder id="brand"></as:placeholder>.
  Come and visit us at <as:placeholder id="location">your local restaurant</as:placeholder>
</as:section>
"""

script = audiostack.Content.Script.create(scriptText=text)
print(script)

speech = audiostack.Speech.TTS.create(scriptItem=script, audience={"location" : "Hyde Park, London"}, voice="sara")
print(speech)

speech.download()


{"data": {"projectName": "untitled", "moduleName": "untitled", "scriptName": "untitled", "scriptId": "cee0b79b-7800-4241-9138-8ea53692d862", "scriptText": "<as:section name=\"main\">   Feeling Hungry, looking for something to eat!  why not try our new double quarter pounder from epic burgers.  Come and visit us at <as:placeholder id=\"location\"></as:placeholder></as:section>", "metadata": "{}", "creationDate": "2023-05-16T13:09:38.568683", "lang": "en", "sections": [{"name": "main", "soundSegment": "", "contentType": "tts", "content": "Feeling Hungry, looking for something to eat!   why not try our new double quarter pounder from epic burgers.   Come and visit us at {{location}}", "placeholders": {"location": ""}, "parent": "", "subSections": [], "uuid": "43cb181c-66b4-4dec-97da-5ad8b4279444"}]}, "meta": {"version": "2.0.0", "requestId": "f67cc9b9-f1ab-43a2-b347-490966245e62", "creditsUsed": 0.1, "creditsRemaining": 99999569646.19}, "message": "Script created", "warnings": [], "statusCode": 200}
{"data": {"projectName": "untitled", "moduleName": "untitled", "scriptName": "untitled", "scriptId": "aa55a82a-7c81-4bfe-b6d2-5da11bcf503e", "scriptText": "<as:section name=\"main\">   Feeling Hungry, looking for something to eat!  why not try our new double quarter pounder from epic burgers.  Come and visit us at <as:placeholder id=\"location\">your local resturant</as:placeholder></as:section>", "metadata": "{}", "creationDate": "2023-05-16T13:09:38.568683", "lang": "en", "sections": [{"name": "main", "soundSegment": "", "contentType": "tts", "content": "Feeling Hungry, looking for something to eat!   why not try our new double quarter pounder from epic burgers.   Come and visit us at {{location|your local resturant}}", "placeholders": {"location": "your local resturant"}, "parent": "", "subSections": [], "uuid": "14cde12a-ab36-4b87-b5e8-62f37e3c6d17"}]}, "meta": {"version": "2.0.0", "requestId": "4beb4123-3328-4fa8-b561-93a662256be8", "creditsUsed": 0.1, "creditsRemaining": 99999569646.61}, "message": "Script created", "warnings": [], "statusCode": 200}