sdk_version = "1.2.1"
api_base = "https://v2.api.audio"
api_key = None
assume_org_id = None
app_info = None


from audiostack import content as Content
from audiostack import speech as Speech
from audiostack import production as Production
from audiostack import delivery as Delivery
from audiostack.docs.docs import Documentation

billing_session = 0


def credits_used_in_this_session():
    return float("{:.2f}".format(billing_session))
