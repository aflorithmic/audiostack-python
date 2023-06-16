import audiostack
import os

audiostack.api_key = os.environ["AUDIO_STACK_DEV_KEY"]


script = audiostack.Content.Script.create(
    scriptText="""<as:section name="main" soundSegment="main">Unleash your inner athlete with this men's athletic fit short sleeve running top! Made from one hundred percent polyester dry-fit fabric, it's moisture-wicking, breathable, and not easily deformed - perfect for any workout. The reflective strips on the back and sleeves make it ideal for low visibility situations. Whether you're training, exercising, or enjoying outdoor activities such as running, hiking or cycling sporting this t-shirt is a must-have. Don't settle for less than the best - upgrade your workout wardrobe today!</as:section>"""
)
print(script)
speech = audiostack.Speech.TTS.create(
    scriptItem=script,
    voice="jollie",
    speed=1,
)
print(speech)
prod = audiostack.Production.Mix.create(
    speechItem=speech,
    soundTemplate="feellikedancing",
    timelineProperties={"forceLength": 30},
)
print(prod)
print(audiostack.Delivery.Encoder.encode_mix(productionItem=prod, preset="mp3_high").url)



{
    "intro" : {"endAt" : 10},
    "main" : {"endAt" : 20},
    "outro" : {"endAt" : 30}
}