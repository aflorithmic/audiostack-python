import contextlib
import json
import shutil
from contextvars import ContextVar
from typing import Any, Callable, Dict, Generator, Optional, Union

import requests

import audiostack
from audiostack.helpers.request_types import RequestTypes

_current_trace_id: ContextVar[Optional[str]] = ContextVar(
    "current_trace_id", default=None
)


def remove_empty(data: Any) -> Any:
    if not (isinstance(data, dict) or isinstance(data, list)):
        return data

    final_dict = {}
    for key, val in data.items():  # type: ignore
        if (
            val or isinstance(val, int) or isinstance(val, float)
        ):  # val = int(0), float(0) should not be removed
            if isinstance(val, dict):
                final_dict[key] = remove_empty(val)
            elif isinstance(val, list):
                final_dict[key] = list(filter(None, [remove_empty(i) for i in val]))
            else:
                final_dict[key] = val
    return final_dict


class RequestInterface:
    # disable debug print
    DEBUG_PRINT = False

    def __init__(self, family: str) -> None:
        self.family = family

    @staticmethod
    def make_header(headers: Optional[dict] = None) -> dict:
        new_headers = {
            "x-api-key": audiostack.api_key,
            "x-python-sdk-version": audiostack.sdk_version,
        }
        current_trace_id = _current_trace_id.get()
        if current_trace_id is not None:
            new_headers["x-customer-trace-id"] = current_trace_id
        if audiostack.assume_org_id:
            new_headers["x-assume-org"] = audiostack.assume_org_id
        if headers:
            new_headers.update(headers)
        return new_headers

    def resolve_response(self, r: Any) -> Union[dict, list]:
        if r.status_code == 204:
            return {"statusCode": r.status_code}

        try:
            response_json = r.json()
        except (ValueError, json.JSONDecodeError):
            return {"statusCode": r.status_code, "message": r.text}

        if self.DEBUG_PRINT:
            print(
                json.dumps(response_json, indent=4)
                if isinstance(response_json, (dict, list))
                else response_json
            )

        if r.status_code >= 500:
            print(r.text)
            raise Exception("Internal server error - aborting")

        if r.status_code == 403:
            exc = response_json.get(
                "message", "Not authorised - check API key is valid"
            )
            raise Exception(exc)

        if r.status_code >= 400:
            # Error responses should be dicts
            if isinstance(response_json, dict):
                if "message" in response_json:
                    msg = response_json["message"]
                    if "errors" in response_json and response_json["errors"]:
                        msg += ". Errors listed as follows: \n\t" + "\t".join(
                            response_json["errors"]
                        )
                    else:
                        msg += ". No additional error details provided."
                else:
                    msg = str(response_json)
                raise Exception(msg)
            else:
                raise Exception(str(response_json))

        # Handle successful list responses (200-299)
        if isinstance(response_json, list):
            return (
                response_json  # Return list directly for endpoints that return arrays
            )

        # Handle successful dict responses
        if isinstance(response_json, dict):
            if "meta" in response_json:
                if "creditsUsed" in response_json["meta"]:
                    audiostack.billing_session += response_json["meta"]["creditsUsed"]

            return {**response_json, **{"statusCode": r.status_code}}

        return {"statusCode": r.status_code, "message": str(response_json)}

    def send_upload_request(
        self, local_path: str, upload_url: str, mime_type: str
    ) -> int:
        with open(local_path, "rb") as data:
            r = requests.put(
                url=upload_url, data=data, headers={"Content-Type": mime_type}
            )
            if r.status_code >= 400:
                raise Exception("Failed to upload file")

            return r.status_code

    def send_request(
        self,
        rtype: str,
        route: str,
        json: Optional[dict] = None,
        path_parameters: Optional[Union[dict, str]] = None,
        query_parameters: Optional[Union[dict, str]] = None,
        overwrite_base_url: Optional[str] = None,
        headers: Optional[dict] = None,
    ) -> Any:
        if overwrite_base_url:
            url = overwrite_base_url
        else:
            if self.family:
                url = f"{audiostack.api_base}/{self.family}"
            else:
                url = audiostack.api_base

        if route:
            url += "/" + route

        if rtype not in RequestTypes.valid_types:
            assert False

        if json:
            json = remove_empty(json)
        if query_parameters:
            query_parameters = remove_empty(query_parameters)

        # these requests are all the same input parameters.
        if rtype in [RequestTypes.POST, RequestTypes.PUT, RequestTypes.PATCH]:
            FUNC_MAP: Dict[str, Callable] = {
                RequestTypes.POST: requests.post,
                RequestTypes.PUT: requests.put,
                RequestTypes.PATCH: requests.patch,
            }

            return self.resolve_response(
                FUNC_MAP[rtype](url=url, json=json, headers=self.make_header(headers))
            )
        elif rtype == RequestTypes.GET:
            if path_parameters:
                url = f"{url}/{path_parameters}"

            return self.resolve_response(
                requests.get(
                    url=url, params=query_parameters, headers=self.make_header(headers)
                )
            )
        elif rtype == RequestTypes.DELETE:
            if path_parameters:
                url = f"{url}/{path_parameters}"

            return self.resolve_response(
                requests.delete(
                    url=url, params=query_parameters, headers=self.make_header(headers)
                )
            )

    @classmethod
    def download_url(cls, url: str, name: str, destination: str) -> None:
        r = requests.get(url=url, stream=True, headers=cls.make_header())

        if r.status_code >= 400:
            raise Exception("Failed to download file")

        local_filename = f"{destination}/{name}"
        with open(local_filename, "wb") as f:
            shutil.copyfileobj(r.raw, f)


@contextlib.contextmanager
def use_trace(trace_id: str) -> Generator[None, None, None]:
    token = _current_trace_id.set(trace_id)
    try:
        yield
    finally:
        _current_trace_id.reset(token)
