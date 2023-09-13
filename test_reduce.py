import audiostack
import os

audiostack.api_base = "https://staging-v2.api.audio"
audiostack.api_key = os.environ["AUDIO_STACK_DEV_KEY"]

# example 1
def publicis_examples(req):
    scriptText = f"""
    <as:section name="main" soundsegment="main"> 
    {req["text"]}
    </as:section>"""

    script = audiostack.Content.Script.create(scriptText=scriptText, scriptName="test")

    tts = audiostack.Speech.TTS.create(scriptItem=script, voice=req["voice"], speed=req["speed"])

    tts = audiostack.Speech.TTS.reduce(speechId=tts.speechId, targetLength=req["targetLength"])
    # tts.download()

    timelineProperties= {
        "forceLength" : req['targetLength'],
        "speechStart" : 0,
        "fadeIn" : 0,
        "fadeOut" : 0,
    }

    mix = audiostack.Production.Mix.create(speechItem=tts, exportSettings={"ttsTrack" : True}, masteringPreset="", timelineProperties=timelineProperties)

    encoder = audiostack.Delivery.Encoder.encode_mix(
        productionItem=mix,
        preset="custom",
        sampleRate=44100,
        bitDepth=16,
        public=False,
        format="wav",
        channels=2,
        loudnessPreset="podcast"
    )

    encoder.download(fileName=req["name"])
    print(encoder)

if __name__ == "__main__":

    examples = [
        {
            "name": "example1",
            "text": "During the Summer of Jeep, get fifteen percent below M S R P for an average of six thousand three hundred under M S R P on the twenty twenty three Jeep Cherokee Altitude Lux. And get no monthly payments for ninety days on twenty twenty three Jeep brand vehicles.",
            "voice": "Bryer",
            "speed": 1.00,
            "targetLength": 16
        },
        # {
        #     "name": "example2",
        #     "text": "Jeep Adventure Days is going on now. Hurry in for great deals. Well-qualified lessees get a low mileage lease on the twenty twenty three Jeep Grand Cherokee four by E for three ninety nine a month for twenty seven months with five thousand six ninety nine due at signing. Tax, title, license extra. No security deposit required. Call one eight eight eight nine two five Jeep for details. Requires dealer contribution and lease through Stellantis Financial.  Extra charge for miles over twenty two thousand five hundred. Includes seven thousand five hundred E V cap cost reduction. Not all customers will qualify. Residency restrictions apply. Take delivery by ten two. Jeep is a registered trademark.",
        #     "voice": "Conversational_antony",
        #     "speed": 1.20,
        #     "targetLength": 30
        # },
        # {
        #     "name": "example4",
        #     "text": "During Jeep adventure days, well-qualified lessees can lease the twenty twenty three Jeep Grand Cherokee four by E for three ninety nine a month.",
        #     "voice": "Conversational_kai",
        #     "speed": 1.00,
        #     "targetLength": 7
        # },

    ]

    for req in examples:
        res = publicis_examples(req)
        print(res)