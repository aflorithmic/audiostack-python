from typing import Dict
from unittest.mock import MagicMock, patch

import pytest

from audiostack.creator import Story


@pytest.fixture
def correct_story_sample() -> Dict:
    story = {
        "title": "Master Chef Prince - Multiple voices",
        "voices": [
            {
                "speakerIdentifier": "female_journalist",
                "alias": "rj_suhana",
                "voicePreset": "expressive",
                "speed": 1.05,
            },
            {
                "speakerIdentifier": "narrator",
                "alias": "aakash",
                "voicePreset": "expressive",
                "speed": 1.05,
            },
            {
                "speakerIdentifier": "royal_star_hotel_owner",
                "alias": "raghav",
                "voicePreset": "expressive",
                "speed": 1.05,
            },
            {
                "speakerIdentifier": "chairman",
                "alias": "bunty",
                "voicePreset": "expressive",
                "speed": 1.05,
            },
            {
                "speakerIdentifier": "uncle_of_prince_master_chef",
                "alias": "danish_khan",
                "voicePreset": "expressive",
                "speed": 1.05,
            },
            {
                "speakerIdentifier": "aunty_of_master_chef",
                "alias": "reet",
                "voicePreset": "expressive",
                "speed": 1.05,
            },
            {
                "speakerIdentifier": "roma",
                "alias": "payal",
                "voicePreset": "expressive",
                "speed": 1.05,
            },
            {
                "speakerIdentifier": "munna",
                "alias": "suman_chatterjee",
                "voicePreset": "expressive",
                "speed": 1.05,
            },
            {
                "speakerIdentifier": "raju",
                "alias": "harsh",
                "voicePreset": "expressive",
                "speed": 1.05,
            },
            {
                "speakerIdentifier": "supervisor_aman",
                "alias": "jeet_yadav",
                "voicePreset": "expressive",
                "speed": 1.05,
            },
        ],
        "production": {"masteringPreset": "balanced"},
        "delivery": {"encoderPreset": "mp3", "public": True},
        "chapters": [
            {
                "title": "PT1 - The mystery begins",
                "narratives": [
                    {
                        "foreground": [
                            {
                                "speakerIdentifier": "narrator",
                                "text": "Mumbai police ने जब files खोलीं, तो सबके होश उड़ गए। Master Chef Prince के नाम से तीन शहरों में, तीन अलग-अलग death certificates। आखिर एक आदमी तीन बार कैसे मर सकता है?",
                            },
                            {
                                "speakerIdentifier": "narrator",
                                "text": "Master Chef Prince, वो chef जिनकी हर recipe करोड़ों में बिकती थी। जिनके चेहरे को आज तक दुनिया ने नहीं देखा। आखिर आज वो दिन आ ही गया, जब दुनिया पहली बार Prince को बिना mask देखेगी। लेकिन उनके face reveal से पहले ही Royal Star के gate पर एक mysterious लिफाफा मिला। जिसके अंदर, सिर्फ एक लाइन लिखी थी।",
                            },
                            {
                                "speakerIdentifier": "narrator",
                                "text": "अगर master chef का चेहरा दुनिया ने देखा, तो खून बहेगा।",
                            },
                            {
                                "speakerIdentifier": "narrator",
                                "text": "उधर, लोग अपने master chef की सिर्फ एक झलक पाने के लिए बेसब्री से इंतजार कर रहे थे।",
                            },
                            {
                                "speakerIdentifier": "female_journalist",
                                "text": "मुंबई की सबसे luxurious hotel, Royal Star। आज yahan पर दुनिया के नंबर 1 chef, Master Chef Prince की grand welcome ceremony चल रही है। Media, hotel tycoons, और hazaaro fans, सब बस एक ही शख्स का इंतजार कर रहे हैं। और वो हैं, humaare iconic Master Chef, Prince।",
                            },
                            {
                                "speakerIdentifier": "female_journalist",
                                "text": "ये सिर्फ एक chef नहीं, एक जादूगर है। जो लगातार तीन बार world chef championship जीत चुके हैं। इसी लिए ये हैं world के number one chef। लेकिन आज तक, किसी ने इन्हें देखा नहीं। हमेशा inhone mask पहनकर अपनी identity छुपाए रखी है, लेकिन…",
                            },
                            {
                                "speakerIdentifier": "female_journalist",
                                "text": "आज पहली बार, ये अपना चेहरा, duniya ko दिखाएंगे।",
                            },
                            {
                                "speakerIdentifier": "narrator",
                                "text": "हर कोई master chef के आने का बेसब्री से इंतजार कर रहा था। यहां तक कि बड़े-बड़े hotels के मालिक भी master chef का wait कर रहे थे, क्योंकि वे उनके साथ deal करना चाहते थे।",
                            },
                            {
                                "speakerIdentifier": "female_journalist",
                                "text": "तो आइए चलते हैं इन mashhoor hotels के owners के पास, और जानते हैं कि वे master chef के साथ किस तरह की deal करना चाहते हैं?",
                            },
                            {
                                "speakerIdentifier": "royal_star_hotel_owner",
                                "text": "अगर master chef हमारे hotel के साथ जुड़ जाते हैं, तो मैं उनके साथ 50 करोड़ की deal sign करूंगा।",
                            },
                            {
                                "speakerIdentifier": "chairman",
                                "text": "मैं तो उनके साथ 100 करोड़ की deal भी करने को तैयार हूं। बस वो एक बार मेरे hotel के साथ जुड़ जाएं।",
                            },
                            {
                                "speakerIdentifier": "uncle_of_prince_master_chef",
                                "text": "रुको। रुको सब। मैं हूं Prince का uncle, और मैंने already एक deal finalize कर दी है। तो बकवास बंद करो तुम सब।",
                            },
                            {
                                "speakerIdentifier": "aunty_of_master_chef",
                                "text": "क्या बकवास है ये? तुम उसके uncle? मैं हूं उसकी real aunty। मैंने उसे बचपन से पाला है। जो मैं कहूंगी, वही होगा।",
                            },
                            {
                                "speakerIdentifier": "narrator",
                                "text": "चारों तरफ media में खलबली मच गई। हर किसी के दिमाग में सिर्फ एक ही सवाल था। आखिर master chef गए कहां?",
                            },
                        ]
                    }
                ],
            }
        ],
    }
    return story


@pytest.fixture
def post_story_response() -> Dict:
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
def get_story_response() -> Dict:
    mock_response = {
        "metadata": {
            "requestId": "request_id_367e6a21-0ffc-4b39-aaea-8381fab60d2a",
            "version": "123",
            "creditsUsed": 0.0,
            "creditsRemaining": 0.0,
        },
        "warnings": [],
        "message": "Build successfully retreived",
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


# ============================================================================
# STORY.ITEM TESTS
# ============================================================================


def test_post_story_response(post_story_response: Dict) -> None:
    item = Story.Item(post_story_response)
    assert item.story_id == post_story_response["data"]["storyId"]
    assert item.audioform_status_code is None
    assert item.story_result == {}
    assert item.audioforms == []
    assert item._errors == ""


def test_post_story_no_storyid() -> None:
    mock_response = {
        "metadata": {
            "requestId": "request_id_5dfee7c2-549d-4c84-8f9f-be980cc0a304",
            "version": "123",
            "creditsUsed": 0.0,
            "creditsRemaining": 0.0,
        },
        "warnings": [],
        "message": "Story successfully created",
        "data": {},
    }

    item = Story.Item(mock_response)
    assert item.story_id == ""
    assert item.audioform_status_code is None
    assert item.story_result == {}
    assert item.audioforms == []
    assert item._errors == ""


def test_get_story_response(get_story_response: Dict) -> None:
    mock_response_id = get_story_response["data"]["audioforms"][0]["header"][
        "audioformId"
    ]

    item = Story.Item(get_story_response)
    assert item.story_id == get_story_response["data"]["storyId"]
    assert item.audioform_status_code == 200
    assert item.audioforms == get_story_response["data"]["audioforms"]
    assert item.story_result == get_story_response["data"]["storyResult"]
    assert item.is_success is True
    assert item.is_failed is False
    assert item.get_audioform_count == 1


def test_get_story_failed_build() -> None:
    mock_response = {
        "metadata": {
            "requestId": "request_id_367e6a21-0ffc-4b39-aaea-8381fab60d2a",
            "version": "123",
            "creditsUsed": 0.0,
            "creditsRemaining": 0.0,
        },
        "warnings": [],
        "message": "Build successfully retreived",
        "data": {"statusCode": 500, "message": "Failed to generate story"},
    }
    item = Story.Item(mock_response)
    assert item.story_id == ""
    assert item.audioform_status_code == 500
    assert item.audioforms == []
    assert item._errors == "Failed to generate story"
    assert item.is_success is False
    assert item.is_failed is True


# ============================================================================
# STORY.CREATE TESTS
# ============================================================================


@patch("audiostack.creator.story.Story.interface.send_request")
def test_create_story(
    mock_send: MagicMock, correct_story_sample: Dict, post_story_response: Dict
) -> None:
    mock_send.return_value = post_story_response
    item = Story.create(story=correct_story_sample)
    mock_send.assert_called_once_with(
        rtype="POST", route="story", json={"story": correct_story_sample}
    )
    assert item.story_id == post_story_response["data"]["storyId"]
    assert item.audioform_status_code is None
    assert item.audioforms == []
    assert item.story_result == {}
    assert item._errors == ""


def test_create_not_dict() -> None:
    story = "hello engineer, hope you're having a good day"
    with pytest.raises(Exception):
        Story.create(story=story)  # type: ignore


def test_create_no_story() -> None:
    with pytest.raises(Exception):
        Story.create()  # type: ignore


# ============================================================================
# STORY.GET TESTS
# ============================================================================


@patch("audiostack.creator.story.Story.interface.send_request")
def test_get_story(mock_send: MagicMock, get_story_response: Dict) -> None:
    mock_send.return_value = get_story_response

    item = Story.get("test", wait=True)
    assert item.story_id == get_story_response["data"]["storyId"]
    assert item.audioform_status_code == 200
    assert item.is_success is True
    assert item.is_failed is False
    assert item.get_audioform_count == 1


@patch("audiostack.creator.story.Story.interface.send_request")
def test_get_polling(mock_send: MagicMock) -> None:
    mock_send.side_effect = [
        {"statusCode": 202},
        {"statusCode": 202},
        {"statusCode": 202},
        {"statusCode": 200, "data": {"storyId": "test", "statusCode": 200}},
    ]

    with patch("time.sleep", return_value=None):
        result = Story.get("test", wait=True)

    assert result.is_success is True
    assert mock_send.call_count == 4


@patch("audiostack.creator.story.Story.interface.send_request")
def test_get_no_wait(mock_send: MagicMock) -> None:
    mock_send.side_effect = [
        {"statusCode": 202},
        {"statusCode": 202},
        {"statusCode": 202},
        {"statusCode": 200, "data": {"storyId": "test", "statusCode": 200}},
    ]

    with patch("time.sleep", return_value=None):
        result = Story.get("test", wait=False)

    assert result.is_success is False
    assert mock_send.call_count == 1


@patch("audiostack.creator.story.Story.interface.send_request")
def test_get_timeout(mock_send: MagicMock) -> None:
    mock_send.return_value = {"statusCode": 202}

    with patch("time.sleep", return_value=None):
        with pytest.raises(TimeoutError) as e:
            Story.get("test", wait=True, timeoutThreshold=1)

    assert "Story polling timed out" in str(e.value)
    assert "test" in str(e.value)
