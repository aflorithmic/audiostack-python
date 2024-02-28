import audiostack
import os

audiostack.api_key = os.environ["AUDIO_STACK_DEV_KEY"]

# create script item
text = "AudioStack’s technology seamlessly integrates into your product or workflow and cuts your audio production cycles to seconds while making your budgets go further."
category = "my_custom_tags"
tags = ["happy", "sad", "valuable"]
number_of_results = 2

print("Recommend Tag endpoint")
item = audiostack.Content.RecommendTag.create(text=text, category=category, tags=tags, number_of_results=number_of_results)
print(item.response)

print("Recommend Tone endpoint")
item = audiostack.Content.RecommendTone.create(text=text, number_of_results=number_of_results)
print(item.response)

print("Recommend Mood endpoint")
item = audiostack.Content.RecommendMood.create(text=text, number_of_results=number_of_results)
print(item.response)

print("Cost for this session: ", audiostack.credits_used_in_this_session())