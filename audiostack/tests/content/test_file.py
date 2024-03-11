import os
import audiostack

from audiostack.content.file import File

audiostack.api_base = os.environ.get("AUDIO_STACK_DEV_URL", "https://v2.api.audio")
audiostack.api_key = os.environ["AUDIO_STACK_DEV_KEY"]

test_constants = {}


def test_create():
    r = File.create(localPath="example.mp3", uploadPath="example.mp3", fileType="audio")
    test_constants["fileId"] = r.fileId
    print(r)


def test_get():
    r = File.get(test_constants["fileId"])
    print(r)


def test_modify():
    r = File.modify(fileId=test_constants["fileId"], category="test")
    print(r)


def test_search():
    files = File.search()
    for f in files:
        print(f)

    files = File.search(source="pythonSDK")
    for f in files:
        print(f)


def test_delete():
    r = File.get(test_constants["fileId"])
    r = r.delete()
    print(r)


def test_create_2():
    r = File.create(
        localPath="example.mp3",
        uploadPath="example.mp3",
        fileType="audio",
        category="sounds",
        tags=["a", "b"],
        metadata={"hello": "world"},
    )
    test_constants["fileId"] = r.fileId
    print(r)
    r.delete()
