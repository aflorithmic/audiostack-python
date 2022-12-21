import json
import shutil

import requests

from audiostack.helpers.util import bcolors
from audiostack.helpers.response import Response
from audiostack.helpers.request_types import RequestTypes

import audiostack


def remove_empty(data):

    if not (isinstance(data, dict) or isinstance(data, list)):
        return data

    final_dict = {}
    for key, val in data.items():
        if val:
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

        if family:
            self.base_url = audiostack.api_base + f"/{family}"
        else:
            self.base_url = audiostack.api_base
   
    
    def make_header(self):

        return {
            "x-api-key": audiostack.api_key,
            "x-python-sdk-version": audiostack.sdk_version
            #"x-assume-org": audiostack.assume_org_id,
        }
    
    
    def resolve_response(self, r):
        if r.status_code >= 500:
            raise Exception("Internal server error - aborting")

        if self.DEBUG_PRINT:
            print(json.dumps(r.json(), indent=4))
        
        if "meta" in r.json():
            if "creditsUsed" in r.json()["meta"]:
                audiostack.billing_session += r.json()["meta"]["creditsUsed"]

        if r.status_code == 403:
            raise Exception("Not authorised - check API key is valid")
        
        if r.status_code >= 400:
            msg = r.json()["message"] + ". Errors listed as follows: \n\t" + '\t'.join(r.json()["errors"])
            raise Exception(msg)

        return {**r.json(), **{"statusCode" : r.status_code}}

    
    def send_upload_request(self, local_path, upload_url):
        with open(local_path, 'rb') as data:
            r = requests.put(url=upload_url, data=data)

            if r.status_code >= 400:
                raise Exception("Failed to upload file")

            return r.status_code


    def send_request(self, rtype, route, json=None, path_parameters=None, query_parameters=None, overwrite_base_url=None):
        
        if overwrite_base_url:
            url = overwrite_base_url
        else:
            url = self.base_url
        
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
            
            FUNC_MAP = {
                RequestTypes.POST : requests.post,
                RequestTypes.PUT : requests.put,
                RequestTypes.PATCH : requests.patch
            }
            
            return self.resolve_response(
                FUNC_MAP[rtype](
                    url=url, 
                    json=json, 
                    headers=self.make_header()
                )
            )
        elif rtype == RequestTypes.GET:
            
            if path_parameters:
                url = f"{url}/{path_parameters}"
                
            return self.resolve_response(
                requests.get(
                    url=url,
                    params=query_parameters,
                    headers=self.make_header()
                )
            )
        elif rtype == RequestTypes.DELETE:
            
            if path_parameters:
                url = f"{url}/{path_parameters}"

            return self.resolve_response(
                requests.delete(
                    url=url,
                    params=query_parameters,
                    headers=self.make_header()
                )
            )
    
    @staticmethod
    def download_url(url, name, destination):
        r = requests.get(
            url=url, 
            stream=True, 
            headers={"x-api-key": audiostack.api_key}
        )

        if r.status_code >= 400:
            raise Exception("Failed to download file")

        local_filename = f"{destination}/{name}"
        with open(local_filename, "wb") as f:
            shutil.copyfileobj(r.raw, f)