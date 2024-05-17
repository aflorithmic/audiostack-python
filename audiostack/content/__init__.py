from audiostack.content.file import File, Folder  # noqa: F401
from audiostack.content.media import Media  # noqa: F401
from audiostack.content.recommend import (  # noqa: F401
    RecommendMood,
    RecommendTag,
    RecommendTone,
)
from audiostack.content.script import Script  # noqa: F401


def list_projects():
    from audiostack.content.root_functions import Root

    return Root.list_projects()


def list_modules():
    from audiostack.content.root_functions import Root

    return Root.list_modules()


def generate(prompt: str, max_length: int = 100):
    from audiostack.content.root_functions import Root

    return Root.generate(prompt, max_length)
