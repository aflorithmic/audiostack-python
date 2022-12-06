import audiostack
import os
import pytest 

def test_voice_assetion():
    audiostack.api_key = os.environ["AUDIO_STACK_DEV_KEY"]

    

    
    with pytest.raises(Exception) as exc:
        scriptText = """
        <<soundSegment::intro>><<sectionName::intro>> Hello <<soundSegment::main>> <<sectionName::main>> this is main <<soundSegment::outro>><<sectionName::outro>> goodbye
        """
        script = audiostack.Content.Script.create(scriptText=scriptText)
        audiostack.Speech.TTS.create(scriptItem=script, voice=2)
    assert repr(exc) == "<ExceptionInfo Exception('voice argument should be a string') tblen=2>"

