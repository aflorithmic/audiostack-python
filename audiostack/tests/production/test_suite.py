import os
from unittest.mock import patch

import audiostack
from audiostack.content.file import File
from audiostack.production.suite import Suite

audiostack.api_base = os.environ.get("AUDIO_STACK_DEV_URL", "https://v2.api.audio")
audiostack.api_key = os.environ["AUDIO_STACK_DEV_KEY"]  # type: ignore

test_constants = {}


def test_create() -> None:
    r = File.create(localPath="example.mp3", uploadPath="example.mp3", fileType="audio")
    test_constants["fileId"] = r.fileId
    print(r)


def test_denoise() -> None:
    with patch("audiostack.production.suite.Suite.DENOISE_ENDPOINT", "suite/test"):
        r = Suite.denoise(test_constants["fileId"], wait=False)
        assert isinstance(r, Suite.PipelineInProgressItem)
        test_constants["pipelineId"] = r.pipelineId


def test_transcribe() -> None:
    with patch("audiostack.production.suite.Suite.TRANSCRIBE_ENDPOINT", "suite/test"):
        r = Suite.transcribe(test_constants["fileId"], language="en", wait=False)
        assert isinstance(r, Suite.PipelineInProgressItem)


def test_get() -> None:
    r = Suite.get(test_constants["pipelineId"])
    assert isinstance(r, Suite.PipelineFinishedItem)
    for f in r.convert_new_files_to_items():
        f.download()
