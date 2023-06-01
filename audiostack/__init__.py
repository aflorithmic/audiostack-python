sdk_version = "0.0.7"
api_base = "https://v2.api.audio"
api_key = None

api_version = "0.0.7"
verify_ssl_certs = True
proxy = None
default_http_client = None
app_info = None
enable_telemetry = True
max_network_retries = 0


from audiostack import content as Content
from audiostack import speech as Speech
from audiostack import production as Production
from audiostack import delivery as Delivery
from audiostack.docs.docs import Documentation

billing_session = 0


def credits_used_in_this_session():
    return float("{:.2f}".format(billing_session))
