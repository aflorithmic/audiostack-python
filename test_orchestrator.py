import os
import audiostack
import json
from time import time
from audiostack.helpers.request_interface import RequestInterface

# ISSUES:
# Lots of shaven yaks for this demo. Fixed some bugs here and there, but there are still issues to be addressed for Audioform to be fully functional.
#
# ProvisionedThroughput in sound templates dynamo causes throtthling. Change BillingType to PAY_PER_DEMAND
# Mastering ocasionally times out.
# Encoder cannot find a file, or throws an error 'Expecting value: line 1 column 1 (char 0)' in ~20% of cases.
# Add productionId to encoder's response
#

if __name__ == "__main__":
    t0 = time()
    audiostack.api_key = "0b1173a6420c4c028690b7beff39c0ad"

    script = audiostack.Content.Script.create(
        scriptText="""
        <<sectionName::intro>>
        May the joy that you have spread in the past come back to you on this day. Wishing you a very happy birthday {{name}}!
        <<sectionName::main>>
        May you be gifted with life’s biggest joys and never-ending bliss. After all, you yourself are a gift to earth, so you deserve the best.
        Forget the past; look forward to the future, for the best things are yet to come.
        <<sectionName::outro>> 
        Enjoy your special day, happy to have you with us!
        """
    )
    print(script.response)

    audience = {
        "name": [
            "Sam",
            "Timo",
            "Peadar",
            "Bjorn",
            "Matt",
            "Lars",
            "Marcin",
            "Maria",
            "Hugo",
            "Liana",
            "Tim",
        ],
    }

    voices = [
        "Tony",
        "Zoe",
        "Hunter",
        "Hudson",
        "Sonia",
        "Liam",
        "Ryan",
        "Jenny",
        "Elizabeth",
        "Gabriel",
    ]

    r = audiostack.Orchestrator.Audioform.create_speech(
        audience=audience, scriptItem=script, voices=voices
    )
    print(r)

    tts_files = audiostack.Speech.TTS.list(scriptId=script.scriptId)
    print(tts_files.response)
    speech_create_time = time() - t0
    t0 = time()
    r = audiostack.Orchestrator.Audioform.create_mastering(
        speechIdList=[d["speechId"] for d in tts_files.response["data"]["speechIds"]],
        soundTemplateList=[
            "copacabana",
            "deepsea",
            "bullmarket",
            "breakingnews",
            "parisianmorning",
            "summerlove",
            "driftingoff",
            "hotwheels",
            "triggerhappy",
            "heatwave",
        ],
        forceLengthList=[30],
    )
    mastered_files = audiostack.Production.Mix.list(scriptId=script.scriptId)
    print(mastered_files.response)
    mix_create_time = time() - t0
    t0 = time()
    pids = [mf.productionId for mf in mastered_files]
    r = audiostack.Orchestrator.Audioform.batch_encode(pids, presets=["mp3_high"])
    batch_encode_time = time() - t0

    print("SPEECH", speech_create_time)
    print("MIX", mix_create_time)
    print("ENCODE", batch_encode_time)
    for i, ob in enumerate(r):
        url = ob.get("data", {}).get("url", "")
        if not url:
            print("FAIL")
            print(ob)
        else:
            RequestInterface.download_url(url, f"{url.split('/')[9]}.mp3", "./files")
