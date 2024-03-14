import os
import audiostack

from audiostack.content.file import File
from audiostack.production.suite import Suite

audiostack.api_base = os.environ.get("AUDIO_STACK_DEV_URL", "https://v2.api.audio")
audiostack.api_key = os.environ["AUDIO_STACK_DEV_KEY"]

test_constants = {}

def test_create():
    r = File.create(localPath="example.mp3", uploadPath="example.mp3", fileType="audio")
    test_constants["fileId"] = r.fileId
    print(r)


def test_denoise():
    r = Suite.denoise(test_constants["fileId"], wait=False)
    assert isinstance(r, Suite.PipelineInProgressItem)
    test_constants["pipelineId"] = r.pipelineId


def test_get():
    r = Suite.get(test_constants["pipelineId"])
    assert isinstance(r, Suite.PipelineFinishedItem)
    for f in r.convert_new_files_to_items():
        f.download()
