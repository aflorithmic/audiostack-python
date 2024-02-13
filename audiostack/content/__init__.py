from audiostack.content.script import Script
from audiostack.content.media import Media
from audiostack.content.file import File, Folder
from audiostack.content.recommend import RecommendTag, RecommendMood, RecommendTone


def list_projects():
    from audiostack.content.root_functions import Root

    return Root.list_projects()


def list_modules():
    from audiostack.content.root_functions import Root

    return Root.list_modules()

def generate(prompt: str, max_length: int = 100):
    from audiostack.content.root_functions import Root

    return Root.generate(prompt, max_length)