import os
import audiostack

from audiostack.speech.diction import Diction

audiostack.api_base = os.environ.get("AUDIO_STACK_DEV_URL", "https://v2.api.audio")
audiostack.api_key = os.environ["AUDIO_STACK_DEV_KEY"]


def test_dict_list():
    # list words in default public dicts
    dicts = Diction.list()
    for d in dicts:
        assert d
        print(d.lang, d.content, d.words[0:10])

def test_dict_custom_list():
    # list words in custom dicts
    dicts = Diction.Custom.list()
    for d in dicts:
        print(d.lang, d.content, d.words[0:10])


def test_create():
    create = Diction.Custom.create_word(word="AFLR", replacement="aflorithmic", lang="global")
    assert create


def test_delete():
    response = Diction.Custom.delete_word(word="AFLR", lang="global")
    print(response)


def list_custom():
    # list words and replacements in a custom dict
    word_sets = Diction.Custom.list_words(lang="global")
    for w in word_sets:
        print(w.inputs, w.replacements)
