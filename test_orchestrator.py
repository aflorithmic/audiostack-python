import os
import audiostack
import json
from time import time


if __name__ == "__main__":
    t0 = time()
    audiostack.api_key = "0b1173a6420c4c028690b7beff39c0ad"

    script = audiostack.Content.Script.create(
        scriptText="Happy {{holiday}} employee {{name}}. For this occasion you can have 3 drinks on us! Lucky you!!"
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
        "holiday": [
            "hanukkah",
            "birthday",
            "christmas",
            "easter",
            "thanksgiving",
            "day of independence",
            "new year",
            "all saints",
            "constitution day",
            "valentine's day",
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
        soundTemplateList=["copacabana"],
    )
    mastered_files = audiostack.Production.Mix.list(scriptId=script.scriptId)
    print(mastered_files.response)
    print("TOTAL TIME b4 download:", time() - t0)

    for mf in mastered_files:
        audiostack.Delivery.Encoder.encode_mix(
            productionId=mf.productionId, preset="mp3_high"
        ).download(mf.productionId, "./files")
    print("TOTAL TIME after download:", time() - t0)
    """
    for tts in tts_files:
        print("getting", tts.speechId)
        # simple syntax, get TTS and then download
        item = audiostack.Speech.TTS.get(tts.speechId)
        print(item.response)
        item.download(autoName=True)
    """
