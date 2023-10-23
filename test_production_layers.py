import audiostack
import os

audiostack.api_key = "0b1173a6420c4c028690b7beff39hdik"
audiostack.api_base = "https://staging-v2.api.audio"

print(audiostack.Production.Mix.list_presets())

scriptText1 = """
<as:section name="main" soundsegment="main">
    Everything is rebuilt from scratch instrument by instrument. Trying to replicate the original template moods and melodies but changing sounds and melodies.
</as:section>
"""
scriptText = """
<as:section name="a"> 
The Code of Darkness
</as:section>

<as:section name="intro" soundsegment="intro"> 
In the sprawling city of Techville, nestled amidst a forest of towering skyscrapers, there lived a software developer named lars. He was an introverted genius, known throughout the tech industry for his unparalleled coding skills. But there was something peculiar about lars that sent shivers down the spines of his coworkers—he had an obsession with the darker side of programming.


</as:section>
<as:section name="main" soundsegment="main">
lars's fascination with the arcane and forbidden had led him to a remote corner of the internet where he stumbled upon a mysterious chat room. It was there that he encountered a shadowy group of hackers who called themselves The Black Coders. They promised power, wealth, and knowledge beyond imagination to anyone who could complete their sinister tasks.


</as:section>
<as:section name="outro" soundsegment="outro"> 
Intrigued and intoxicated by the allure of forbidden knowledge, lars agreed to join their ranks. Little did he know that he had just crossed a line from which there was no return.


</as:section>"""

scriptText = """
<as:section name="intro" soundSegment="intro">Introducing Fromage Fantastique, the luxurious cheese brand that brings the flavors of Europe straight to your plate. With a range of expertly crafted cheeses, each with a unique and unforgettable taste, elevate your culinary creations and impress your guests with the finest quality cheese.</as:section>
<as:section name="main" soundSegment="main">
    This is the second section and will be combined with the main music. The section name and soundsegment don't have to have the same name.
</as:section>
<as:section name="outro" soundSegment="outro">Hello from Audiostack. This is a test script. I hope you enjoy it.</as:section>
"""

scriptText2 = """
<as:section name="intro" soundSegment="intro">
    Fun Fact. Did you know there are two types of copyright protection? For years now, Audiostack has been breaking both of them. Until Now!!!
</as:section>

<as:section name="main" soundSegment="main">
These new sound templates closely mimic the original enough to keep the, pigs, off our back. Our in house audio engineers have been slaving away to recreate them all from scratch. There should probably be an AI for this, but wheres the fun of walking the line of legality.
</as:section>

<as:section name="outro" soundSegment="outro">
There are a now a total of 20, so called legal sound templates. They sound glorius and are technically royalty free. <as:break time="400ms"/> Enjoy these while they last, you never know when the judge will come after us.
</as:section>
"""


# scriptText = """

# <as:section name="main" soundsegment="main">
#    Once, in the remote countryside of Willowbrook, nestled beneath the shadowy embrace of ancient oaks and overgrown thorns, stood Hollow Manor—a decrepit mansion cloaked in eerie legends. Its sinister silhouette haunted the dreams of the townsfolk, casting a pall of dread over the land. No one dared venture near after dark, for they believed that malevolent spirits inhabited its desolate halls.

# </as:section>
# """

script = audiostack.Content.Script.create(scriptText=scriptText2)
print("response from creating script", script.response)
scriptId = script.scriptId

# create one tts resource
tts = audiostack.Speech.TTS.create(scriptItem=script, voice="bryer")
print(tts.speechId)

sound_template = "chromatic_jazz"
sound_layer = "default"
mix = audiostack.Production.Mix.create(speechItem=tts, soundTemplate=sound_template, masteringPreset="musicenhanced", soundLayer=sound_layer)# sectionProperties={"main" : {"endAt" : 120}})
print(mix)
#mix.download(fileName=st)

encoded = audiostack.Delivery.Encoder.encode_mix(productionItem=mix, preset="wav")
encoded.download(fileName=f"{sound_template}_{sound_layer}")

# # lets list what we created and deleted it 
# mix_files = audiostack.Production.Mix.list(scriptId=scriptId)
# print(mix_files.response)
# for mix in mix_files:
#     item = audiostack.Production.Mix.get(mix.productionId)  
#     r = item.delete()
#     print(r)

# print("Cost for this session: ", audiostack.credits_used_in_this_session())
