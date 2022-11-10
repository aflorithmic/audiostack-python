import json
import shutil

import requests


from audiostack.helpers.util import bcolors
from audiostack.helpers.response import Response
from audiostack.helpers.request_types import RequestTypes

import audiostack


def remove_empty(d):
    final_dict = {}
    for a, b in d.items():
        if b:
            if isinstance(b, dict):
                final_dict[a] = remove_empty(b)
            elif isinstance(b, list):
                final_dict[a] = list(filter(None, [remove_empty(i) for i in b]))
            else:
                final_dict[a] = b
    return final_dict

class RequestInterface:
    
    # disable debug print
    DEBUG_PRINT = False
    

    def __init__(self, family: str) -> None:
        self.base_url = audiostack.api_base + f"/{family}"
        
   
    def make_header(self):
        # I guess we might attach something here for testing?
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
        
        return {**r.json(), **{"statusCode" : r.status_code}}
#        return Response(**{**{"statusCode" : r.status_code}, **r.json() })
    
    def send_request(self, rtype, route, json=None, path_parameters=None, query_parameters=None, overwrite_base_url=None):
        
        if overwrite_base_url:
            url = overwrite_base_url + "/" + route
        else:
            url = self.base_url + "/" + route
        if rtype not in RequestTypes.valid_types:
            assert False
        
        if json:
            json = remove_empty(json)
        if query_parameters:
            query_parameters = remove_empty(query_parameters)
        
        # these requests are all the same input parameters.
        if rtype in [RequestTypes.POST, RequestTypes.PUT, RequestTypes.PATCH]:
            

                
            func_map = {
                RequestTypes.POST : requests.post,
                RequestTypes.PUT : requests.put,
                RequestTypes.PATCH : requests.patch
            }
            
            return self.resolve_response(
                func_map[rtype]
                (
                    url=url, 
                    json=json, 
                    headers=self.make_header()
                )
            )
        if rtype == RequestTypes.GET:
            
            if path_parameters:
                url = f"{url}/{path_parameters}"
                
            return self.resolve_response(
                requests.get(
                    url=url,
                    params=query_parameters,
                    headers=self.make_header()
                )
            )
                
        if rtype == RequestTypes.DELETE:
            
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
        r = requests.get(url, stream=True)
        local_filename = f"{destination}/{name}"
        with open(local_filename, "wb") as f:
            shutil.copyfileobj(r.raw, f)