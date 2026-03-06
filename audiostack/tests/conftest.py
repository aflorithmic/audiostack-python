import os
from typing import Dict, Generator
from uuid import UUID

import pytest

import audiostack
from audiostack.files.file import File
from audiostack.folders.folder import Folder
from audiostack.tests.utils import create_test_file_name, create_test_folder_name

audiostack.api_base = os.environ.get(
    "AUDIO_STACK_DEV_URL", "https://staging-v2.api.audio"
)
audiostack.api_key = os.environ.get("AUDIO_STACK_DEV_KEY", None)  # type: ignore


@pytest.fixture
def script_item() -> Generator[audiostack.Content.Script.Item, None, None]:
    script = audiostack.Content.Script.create(scriptText="hello sam")
    yield script
    audiostack.Content.Script.delete(scriptId=script.scriptId)


@pytest.fixture
def speech_item(
    script_item: audiostack.Content.Script.Item,
) -> Generator[audiostack.Speech.TTS.Item, None, None]:
    tts = audiostack.Speech.TTS.create(
        scriptId=script_item.scriptId,
        voice="isaac",
    )
    yield tts
    audiostack.Speech.TTS.delete(speechId=tts.speechId)


@pytest.fixture
def cleanup_resources() -> Generator[dict, None, None]:
    """Fixture to track and clean up test resources for files/folders tests."""

    resources: dict[str, list[str | None]] = {
        "file_ids": [],
        "folder_ids": [],
    }

    yield resources

    # Cleanup: delete all tracked resources
    for file_id in resources["file_ids"]:
        try:
            File.delete(fileId=UUID(file_id))
        except Exception:
            pass

    for folder_id in resources["folder_ids"]:
        try:
            Folder.delete(folderId=UUID(folder_id))
        except Exception:
            pass


@pytest.fixture
def test_file(cleanup_resources: dict) -> File.Item:
    """Fixture to create a test file for unit tests."""
    root_folder_id = Folder.get_root_folder_id()
    file = File.create(
        localPath="example.mp3",
        fileName=create_test_file_name() + ".mp3",
        folderId=UUID(root_folder_id),
    )
    cleanup_resources["file_ids"].append(file.fileId)
    return file


@pytest.fixture
def test_folder(cleanup_resources: dict) -> Folder.Item:
    """Fixture to create a test folder for unit tests."""
    folder = Folder.create(name=create_test_folder_name())
    cleanup_resources["folder_ids"].append(folder.folderId)
    return folder


@pytest.fixture
def correct_story_sample() -> Dict:
    story = {
        "title": "Robot Revolution - SINGLE VOICE STORY",
        "textSettings": {"useVoiceIntelligenceLayer": True, "language": "en"},
        "voices": [
            {
                "speakerIdentifier": "narrator",
                "alias": "wren",
                "voicePreset": "standard",
                "speed": 1.1,
            }
        ],
        "production": {"masteringPreset": "balanced"},
        "delivery": {"encoderPreset": "mp3", "public": True},
        "chapters": [
            {
                "title": "PT1 - discovery and hiding",
                "narratives": [
                    {"foreground": [{"speakerIdentifier": "narrator", "text": "test"}]}
                ],
            }
        ],
    }
    return story


@pytest.fixture
def post_story_good_response() -> Dict:
    mock_response = {
        "metadata": {
            "requestId": "request_id_5dfee7c2-549d-4c84-8f9f-be980cc0a304",
            "version": "123",
            "creditsUsed": 0.0,
            "creditsRemaining": 0.0,
        },
        "warnings": [],
        "message": "Story successfully created",
        "data": {"storyId": "4550fde5-4c63-4fd0-853f-148010cd6278"},
    }
    return mock_response


@pytest.fixture
def get_story_good_response() -> Dict:
    mock_response = {
        "metadata": {
            "requestId": "request_id_367e6a21-0ffc-4b39-aaea-8381fab60d2a",
            "version": "123",
            "creditsUsed": 0.0,
            "creditsRemaining": 0.0,
        },
        "warnings": [],
        "message": "Build successfully retreived",
        "statusCode": 200,
        "data": {
            "statusCode": 200,
            "storyId": "4550fde5-4c63-4fd0-853f-148010cd6278",
            "storyResult": {
                "title": "TEst story",
                "textSettings": {"useVoiceIntelligenceLayer": False},
                "voices": [
                    {
                        "speakerIdentifier": "alex",
                        "alias": "wren",
                        "speed": 1.0,
                        "voicePreset": "expressive",
                    }
                ],
                "sounds": {
                    "soundDesigns": [
                        {
                            "soundDesignIdentifier": "dark_ambient",
                            "type": "asset",
                            "alias": "bare_minimum",
                        }
                    ]
                },
                "production": {"mixingPreset": "recommended"},
                "delivery": {
                    "loudnessPreset": "streaming",
                    "encoderPreset": "mp3",
                    "public": True,
                },
                "chapters": [
                    {
                        "title": "PT1",
                        "narratives": [
                            {
                                "foreground": [
                                    {
                                        "text": "Bob always hated the quiet. The city had a way of humming at night—pipes clicking, neon buzzing, someone laughing three floors down. That hum died the moment the woman stepped out of the alley. Silence folded around her like a held breath. She smiled at Bob as if she already knew his name. “Lost?” she asked. Bob should’ve kept walking. He had a bag of takeout going cold in his hand, a podcast paused mid-sentence in his ear. Normal life. Microwave lights and unread emails. Instead, he pulled out an earbud and answered like an idiot. “Just… taking the long way home.” Her eyes caught the streetlight and reflected it wrong. Too bright. Like glass dipped in fire. She moved fast. Not running—arriving. One second the alley was five steps away, the next her fingers were on his wrist, cool as river stones. The takeout hit the pavement. The bag split. Soy sauce bled across concrete. “Wait—” Bob said, and then her teeth were in his neck. Pain exploded and then vanished. The world narrowed to a roaring warmth, like falling asleep in a hot bath. His knees buckled. She held him up effortlessly, whispering something he couldn’t understand—words that scraped at his brain, old and hungry. Bob felt his heart fighting. Each beat weaker than the last. Thump. Thump. Stop. Panic finally hit. He tried to scream, but all that came out was a breath. She pulled back too soon. Her lips were red now. Smiling again. “Not yet,” she said, almost fondly. She sliced her own palm with a nail. Dark blood welled up, thick and slow. She pressed it to his mouth. Every instinct screamed no. His body said yes. The first swallow was fire. The second was lightning. The third shattered him. Bob’s heart gave one final, stubborn beat—and quit. He died on the pavement with his cheek in soy sauce and his phone buzzing in his pocket.",
                                        "speakerIdentifier": "alex",
                                    }
                                ],
                                "background1": [
                                    {
                                        "soundDesignIdentifier": "dark_ambient",
                                        "useSmartFit": True,
                                        "duration": 113.9625,
                                    }
                                ],
                            }
                        ],
                    }
                ],
            },
            "audioforms": [
                {
                    "header": {
                        "version": "3",
                        "audioformId": "cc92b301-5b26-49a8-872e-6d3c24ac5b2b",
                    },
                    "assets": {
                        "alex": {
                            "type": "voice",
                            "voiceAlias": "wren",
                            "speed": 1.0,
                            "voicePreset": "expressive",
                        },
                        "dark_ambient": {
                            "type": "soundTemplate",
                            "soundTemplateAlias": "bare_minimum",
                            "segment": "main",
                            "duration": 154.05566666666667,
                            "uri": "https://staging-v2.api.audio/file/540a85a0-4f4c-4eab-a2a7-0ae3b83a735e",
                        },
                        "1.1": {
                            "type": "tts",
                            "text": "Bob always hated the quiet. The city had a way of humming at night—pipes clicking, neon buzzing, someone laughing three floors down. That hum died the moment the woman stepped out of the alley. Silence folded around her like a held breath. She smiled at Bob as if she already knew his name. “Lost?” she asked. Bob should’ve kept walking. He had a bag of takeout going cold in his hand, a podcast paused mid-sentence in his ear. Normal life. Microwave lights and unread emails. Instead, he pulled out an earbud and answered like an idiot. “Just… taking the long way home.” Her eyes caught the streetlight and reflected it wrong. Too bright. Like glass dipped in fire. She moved fast. Not running—arriving. One second the alley was five steps away, the next her fingers were on his wrist, cool as river stones. The takeout hit the pavement. The bag split. Soy sauce bled across concrete. “Wait—” Bob said, and then her teeth were in his neck. Pain exploded and then vanished. The world narrowed to a roaring warmth, like falling asleep in a hot bath. His knees buckled. She held him up effortlessly, whispering something he couldn’t understand—words that scraped at his brain, old and hungry. Bob felt his heart fighting. Each beat weaker than the last. Thump. Thump. Stop. Panic finally hit. He tried to scream, but all that came out was a breath. She pulled back too soon. Her lips were red now. Smiling again. “Not yet,” she said, almost fondly. She sliced her own palm with a nail. Dark blood welled up, thick and slow. She pressed it to his mouth. Every instinct screamed no. His body said yes. The first swallow was fire. The second was lightning. The third shattered him. Bob’s heart gave one final, stubborn beat—and quit. He died on the pavement with his cheek in soy sauce and his phone buzzing in his pocket.",
                            "voiceRef": "alex",
                            "anchor": "724df7fa-0179-43a3-853c-c0453527b26c",
                            "targetDuration": 113.9625,
                            "targetDurationSpeedUpLimit": 1.2,
                            "targetDurationSlowDownLimit": 1.2,
                            "duration": 113.96081632653062,
                            "uri": "https://staging-v2.api.audio/file/f38cd458-f696-4253-99a7-a4555a3c2e23",
                        },
                        "dark_ambient SNIPPET": {
                            "type": "soundTemplateSnippet",
                            "soundTemplateRef": "dark_ambient",
                            "targetDuration": 113.9625,
                            "readPosition": 0.0,
                            "duration": 113.9625,
                            "uri": "https://staging-v2.api.audio/file/5c6adf20-7f91-4ba6-a767-f9acd6a720e5",
                        },
                    },
                    "production": {
                        "arrangement": {
                            "sections": [
                                {
                                    "layers": [
                                        {
                                            "clips": [
                                                {
                                                    "assetRef": "1.1",
                                                    "marginStart": 0.2,
                                                    "marginEnd": 0.2,
                                                    "fadeIn": 0.1,
                                                    "fadeOut": 0.1,
                                                    "blendBase": False,
                                                    "blendElement": False,
                                                    "placement": "foreground",
                                                    "position": 0.45,
                                                    "duration": 113.96081632653062,
                                                }
                                            ],
                                            "alignment": "start",
                                            "position": 0.25,
                                            "duration": 114.36081632653062,
                                        },
                                        {
                                            "clips": [
                                                {
                                                    "assetRef": "dark_ambient SNIPPET",
                                                    "blendBase": False,
                                                    "blendElement": False,
                                                    "placement": "foreground",
                                                    "position": 0.25,
                                                    "duration": 113.9625,
                                                }
                                            ],
                                            "alignment": "start",
                                            "position": 0.25,
                                            "duration": 113.9625,
                                        },
                                    ],
                                    "paddingStart": 0.25,
                                    "paddingEnd": 0.25,
                                    "position": 0.0,
                                    "duration": 114.86081632653062,
                                }
                            ],
                            "fadeIn": 0.5,
                            "fadeOut": 0.5,
                            "position": 0.0,
                            "duration": 114.86081632653062,
                        },
                        "mixingPreset": "balanced",
                    },
                    "delivery": {
                        "loudnessPreset": "streaming",
                        "encoderPreset": "mp3",
                        "public": True,
                        "uri": "https://staging-v2.api.audio/public-file/d9e64162-2f11-4abc-855f-340b83d2b414",
                        "extension": "mp3",
                    },
                }
            ],
        },
    }
    return mock_response
