import audiostack
import os

audiostack.api_key = os.environ["AUDIO_STACK_DEV_KEY"]
audiostack.api_base = "https://staging-v2.api.audio"

print(audiostack.Production.Mix.list_presets())

scriptText = """
<as:section name="intro" soundsegment="intro"> 
    Our in house audio expert Guillem has replaced and rebuilt our pulse sound templates. This will help un block an angry customer
</as:section>
<as:section name="main" soundsegment="main">
    he did this in less than 2 hours and built everything from scratch
</as:section>
<as:section name="outro" soundsegment="outro"> 
    he mixed and masted this in no time. Lets give him a big thank you!
</as:section>"""

scriptText = """
<as:section name="main" soundsegment="main">
    Our in house audio expert Guillem has replaced and rebuilt our pulse sound templates. This will help un block an angry customer.
        he did this in less than 2 hours and built everything from scratch.     he mixed and masted this in no time. Lets give him a big thank you!


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

<as:section name="intro" soundsegment="intro"> 
In the dimly lit corridors of an old, decrepit software company known as CyberCorp, a shadowy figure loomed. His name was Pedar, the enigmatic Chief Technology Officer. Few had ever glimpsed his face, and those who had were never the same again.



</as:section>
<as:section name="main" soundsegment="main">
Rumors about Pedar swirled through the company like a chilling winter wind. Some said he was a genius who could code with unnatural speed and precision, while others whispered that he had made a sinister pact with the digital demons that lurked in the darkest corners of the internet.



</as:section>
<as:section name="outro" soundsegment="outro"> 
One fateful evening, the development team found themselves working late into the night, racing to meet a critical project deadline. The air was thick with tension, and the fluorescent lights overhead flickered ominously. As the clock struck midnight, the team heard a faint, rhythmic tapping echoing through the hallway.



</as:section>"""


# scriptText = """

# <as:section name="main" soundsegment="main">
#    Once, in the remote countryside of Willowbrook, nestled beneath the shadowy embrace of ancient oaks and overgrown thorns, stood Hollow Manor—a decrepit mansion cloaked in eerie legends. Its sinister silhouette haunted the dreams of the townsfolk, casting a pall of dread over the land. No one dared venture near after dark, for they believed that malevolent spirits inhabited its desolate halls.

# </as:section>
# """

script = audiostack.Content.Script.create(scriptText=scriptText)
print("response from creating script", script.response)
scriptId = script.scriptId

# create one tts resource
tts = audiostack.Speech.TTS.create(scriptItem=script, voice="willow")
print(tts.speechId)

# now generate several different templates of this
for st in ["spooky_strings"]:# ["pulse_v2", "pulse"]:#, "openup", "hotwheels", "whatstillremains"]:#  "lifestylepodcast", "cityechoes"]:
    print("Mixing and encoding a preview of", st)
    mix = audiostack.Production.Mix.create(speechItem=tts, soundTemplate=st)# sectionProperties={"main" : {"endAt" : 120}})
    print(mix)
    #mix.download(fileName=st)

    encoded = audiostack.Delivery.Encoder.encode_mix(productionItem=mix, preset="mp3")
    encoded.download(fileName=st)

# # lets list what we created and deleted it 
# mix_files = audiostack.Production.Mix.list(scriptId=scriptId)
# print(mix_files.response)
# for mix in mix_files:
#     item = audiostack.Production.Mix.get(mix.productionId)  
#     r = item.delete()
#     print(r)

# print("Cost for this session: ", audiostack.credits_used_in_this_session())
