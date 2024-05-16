from audiostack.content.file import File, Folder
from audiostack.content.media import Media
from audiostack.content.recommend import RecommendMood, RecommendTag, RecommendTone
from audiostack.content.script import Script


def list_projects():
    from audiostack.content.root_functions import Root

    return Root.list_projects()


def list_modules():
    from audiostack.content.root_functions import Root

    return Root.list_modules()


def generate(prompt: str, max_length: int = 100):
    from audiostack.content.root_functions import Root

    return Root.generate(prompt, max_length)
