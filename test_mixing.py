
import audiostack
import os



if __name__ == "__main__":
    audiostack.api_key = os.environ["AUDIO_STACK_DEV_KEY"]


    scriptText = """<<soundSegment::intro>><<sectionName::intro>> Hello <<soundSegment::main>> 
    <<sectionName::main>> this is main <<soundSegment::outro>><<sectionName::outro>> goodbye"""

    script = audiostack.Content.Script.create(scriptText=scriptText)
    print("response from creating script", script.response)
    scriptId = script.scriptId


    tts = audiostack.Speech.TTS.create(scriptItem=script, voice="liam")
    print(tts.speechId)
    for st in ["vinylhits", "openup", "hotwheels", "whatstillremains", "sunsetbeachcafe", "hourglass", "feelinggood"]:
        print("Mixing and encoding a preview of", st)
        mix = audiostack.Production.Mix.create(speechItem=tts, soundTemplate=st)
        print(mix.productionId)
        encoded = audiostack.Delivery.Encoder.encode_mix(productionItem=mix, preset="ogg")
        encoded.download(fileName=st)


    mix_files = audiostack.Production.Mix.list(scriptId=scriptId)
    print(mix_files.response)
    for mix in mix_files:
        item = audiostack.Production.Mix.get(mix.productionId)  
        r = item.delete()
        print(r)

    print("Cost for this session: ", audiostack.credits_used_in_this_session())