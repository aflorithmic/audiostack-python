import audiostack

audiostack.api_key = "your key"

# Create a script
script = audiostack.Content.Script.create(
    scriptName="Marathon Conversation",
    scriptText="""
<as:section name='m0'>
Good morning, Coco! How are you today?
</as:section>
<as:section name='s0'>
Hi Wren! I'm doing great, thanks for asking. How about you?
</as:section>
<as:section name='m1'>
I'm good, thanks. So, Coco, I heard you recently completed a marathon. How was the experience?
</as:section>
<as:section name='s1'>
Oh, it was incredible! Crossing that finish line after months of training was such a rewarding feeling. The atmosphere, the support from fellow runners and spectators—it was all so motivating.
</as:section>
<as:section name='m2'>
That sounds amazing. What inspired you to take on such a challenge?
</as:section>
<as:section name='s2'>
Well, I've always been passionate about pushing my limits and staying active. Running a marathon was a personal goal of mine for a long time, and I finally decided to commit to it this year. Plus, I wanted to raise awareness and funds for a charity close to my heart.
</as:section>
<as:section name='m3'>
That's commendable.
</as:section>
""",
)

print("The script ID is:", script.scriptId)

# Create TTS files
tts = audiostack.Speech.TTS.create(
    scriptId=script.scriptId,
    sections={
        "m0": {"voice": "Wren"},
        "s0": {"voice": "Coco"},
        "m1": {"voice": "Wren"},
        "s1": {"voice": "Coco"},
        "m2": {"voice": "Wren"},
        "s2": {"voice": "Coco"},
        "m3": {"voice": "Wren"},
    },
)

print("The speechID is:", tts.speechId)

# Mix the TTS files
mix = audiostack.Production.Mix.create(speechId=tts.speechId)

print("The productionID is:", mix.productionId)

# Encode the mix as mp3
encode = audiostack.Delivery.Encoder.encode_mix(
    productionId=mix.productionId,
    preset="mp3_high",
    public=True,
    loudnessPreset="podcast",
)

print("The URL to the mp3 file is:", encode.url)
