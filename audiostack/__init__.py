sdk_version = "2.7.1"
api_base = "https://v2.api.audio"
api_key = None
assume_org_id = None
app_info = None

TIMEOUT_THRESHOLD_S = 300

from audiostack import content as Content  # noqa: F401
from audiostack import delivery as Delivery  # noqa: F401
from audiostack import production as Production  # noqa: F401
from audiostack import speech as Speech  # noqa: F401
from audiostack.docs.docs import Documentation  # noqa: F401

billing_session = 0


def credits_used_in_this_session() -> float:
    return float("{:.2f}".format(billing_session))
