import audiostack

audiostack.api_key = "your key here"

script = audiostack.Content.Script.create(
    scriptText="""
<as:section name="intro" soundsegment="intro">
Hey there, <as:placeholder id="username">friend</as:placeholder>! Welcome to Audiostack - the audio creation platform that allows you to create high quality audio assets using just a few lines of code.
</as:section>
<as:section name="main" soundsegment="main">
Whether it's a podcast, a video, a game, or an app, Audiostack has you covered. You can create voiceovers, sound effects, music, and more.
</as:section>
<as:section name="outro" soundsegment="outro">
We are excited to see what you'll create with our product!
</as:section>
"""
)
tts = audiostack.Speech.TTS.create(
    scriptItem=script, voice="isaac", audience={"username": "mate"}
)

tts = audiostack.Speech.TTS.remove_padding(speechId=tts.speechId)

mix = audiostack.Production.Mix.create(
    speechItem=tts,
    soundTemplate="chill_vibes",
)

enc = audiostack.Delivery.Encoder.encode_mix(productionItem=mix, preset="mp3_high")
enc.download(fileName="example")
