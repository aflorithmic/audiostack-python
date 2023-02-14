import audiostack
import os

audiostack.api_key = os.environ["AUDIO_STACK_DEV_KEY"]


scriptText = "hello this is sentence 1"
scriptText2 = "hello this is sentence 1"

script = audiostack.Content.Script.create(scriptText=scriptText)
script2 = audiostack.Content.Script.create(scriptText=scriptText2)
print("response from creating script", script.response)
scriptId = script.scriptId

# create one tts resource
tts1 = audiostack.Speech.TTS.create(scriptItem=script, voice="joanna")
tts2 = audiostack.Speech.TTS.create(scriptItem=script2, voice="joanna")

media = audiostack.Content.Media.create(filePath="here.wav")

# needs to be created
mix = audiostack.Production.Timeline.create(timeline=
    [
        {
            "name" : "track1",
            "type" : "speech",
            "files" : [
                {
                    "speechId" : tts1.speechId,
                    "section" : "",
                    "start" : 1.0,
                    "end" : 10.0
                },
                {
                    "speechId" : tts2.speechId,
                    "section" : "",
                    "start" : 14.0,
                    "end" : 24.0
                }   
            ]
        },
        {
            "name" : "track2",
            "type" : "media",
            "files" : [
                {
                    "mediaId" : media.mediaId,
                    "start" : 0.0,
                    "end" : 25.0
                }
            ]
        },
        {
            "name" : "track3",
            "type" : "media",
            "files" : [
                {
                    "mediaId" : media.mediaId2,
                    "start" : 0.0,
                    "end" : 25.0
                }
            ]
        },
        # in a later version
         {
            "name" : "track3",
            "type" : "soundTemplate",
            "using" : 'tuney'
        }
    ]
)


mix = audiostack.Production.Timeline.create(timeline=
    [
        {
            "name" : "track1",
            "type" : "speech",
            "files" : [
                {
                    "speechId" : tts1.speechId,
                    "section" : "",
                    "start" : 1.0,
                    "end" : 10.0
                },
                {
                    "speechId" : tts2.speechId,
                    "section" : "",
                    "start" : 14.0,
                    "end" : 24.0
                }   
            ]
        },
        {
            "name" : "track2",
            "type" : "media",
            "files" : [
                {
                    "mediaId" : media.mediaId,
                    "start" : 0.0,
                    "end" : 25.0
                }
            ]
        },
        # in a later version
         {
            "name" : "track3",
            "type" : "soundTemplate",
            "using" : 'tuney'
        }
    ]
)








# now generate several different templates of this
for st in ["time_horizon_10", "sonic_convalescence_10"]:#:, "roomtone", "lifestylepodcast", "cityechoes"]:
    print("Mixing and encoding a preview of", st)
    mix = audiostack.Production.Mix.create(speechItem=tts, soundTemplate=st)
    #mix.download(fileName=st)

    encoded = audiostack.Delivery.Encoder.encode_mix(productionItem=mix, preset="mp3")
    encoded.download(fileName=st)

# lets list what we created and deleted it 
mix_files = audiostack.Production.Mix.list(scriptId=scriptId)
print(mix_files.response)
for mix in mix_files:
    item = audiostack.Production.Mix.get(mix.productionId)  
    r = item.delete()
    print(r)

print("Cost for this session: ", audiostack.credits_used_in_this_session())
