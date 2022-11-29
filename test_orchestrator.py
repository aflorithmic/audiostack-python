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
# Encoder ocasionally cannot find a file.
#
if __name__ == "__main__":
    t0 = time()
    audiostack.api_key = "0b1173a6420c4c028690b7beff39c0ad"

    script = audiostack.Content.Script.create(
        scriptText="<<sectionName::intro>>Happy birthday {{name}}! <<sectionName::main>>For this occasion you can have 3 drinks on us! Lucky you!!"
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
    print("Speech create time:", time() - t0)

    r = audiostack.Orchestrator.Audioform.create_mastering(
        speechIdList=[d["speechId"] for d in tts_files.response["data"]["speechIds"]],
        soundTemplateList=[
            "copacabana",
            "deepsea",
            "bullmarket",
            "breakingnews",
            "bluewater",
            "articles",
            "driftingoff",
            "hotwheels",
            "house",
            "heatwave",
        ],
    )
    mastered_files = audiostack.Production.Mix.list(scriptId=script.scriptId)
    print(mastered_files.response)
    print("TOTAL TIME b4 download:", time() - t0)

    pids = [mf.productionId for mf in mastered_files]
    r = audiostack.Orchestrator.Audioform.batch_encode(pids, presets=["mp3_high"])

    for i, ob in enumerate(r):
        url = ob.get("data", {}).get("url", "")
        if not url:
            print("FAIL")
            print(ob)
        else:
            RequestInterface.download_url(url, f"{i}.mp3", "./files")
    print("TOTAL TIME after download:", time() - t0)
