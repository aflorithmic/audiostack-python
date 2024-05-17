import os

import audiostack
from audiostack.speech.predict import Predict

audiostack.api_base = os.environ.get("AUDIO_STACK_DEV_URL", "https://v2.api.audio")
audiostack.api_key = os.environ["AUDIO_STACK_DEV_KEY"]  # type: ignore

long_text = """
In the sprawling city of Techville, nestled amidst a forest of towering skyscrapers, there lived a software developer named lars. He was an introverted genius, known throughout the tech industry for his unparalleled coding skills. But there was something peculiar about lars that sent shivers down the spines of his coworkers—he had an obsession with the darker side of programming.
lars's fascination with the arcane and forbidden had led him to a remote corner of the internet where he stumbled upon a mysterious chat room. It was there that he encountered a shadowy group of hackers who called themselves The Black Coders. They promised power, wealth, and knowledge beyond imagination to anyone who could complete their sinister tasks.
Intrigued and intoxicated by the allure of forbidden knowledge, lars agreed to join their ranks. Little did he know that he had just crossed a line from which there was no return.
"""


def test_list() -> None:
    voices = Predict.list()
    print(voices)
    for v in voices:
        assert isinstance(v, str)


def test_predict() -> None:
    item = Predict.predict(text=long_text, voice="sara")
    assert item.length  # type: ignore
