sdk_version = "1.3.1"
api_base = "https://v2.api.audio"
api_key = None
assume_org_id = None
app_info = None


from warnings import warn

from audiostack import content as Content
from audiostack import delivery as Delivery
from audiostack import production as Production
from audiostack import speech as Speech
from audiostack.docs.docs import Documentation

warn(
    "Future releases (`^2.0.0`) of the AudioStack SDK will only support python `^3.8.1`",
    DeprecationWarning,
    stacklevel=2,
)


billing_session = 0


def credits_used_in_this_session():
    return float("{:.2f}".format(billing_session))
