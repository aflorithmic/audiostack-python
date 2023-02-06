from audiostack.helpers.request_interface import RequestInterface
from audiostack.helpers.request_types import RequestTypes
from audiostack.helpers.api_item import APIResponseItem
from audiostack.helpers.api_list import APIResponseList
from audiostack.content.media import Media

from typing import Union
import requests
import shutil

class Sound():
    interface = RequestInterface(family="production/sound")

    # ----------------------------------------- TEMPLATE -----------------------------------------
    class Template():
        
        class Item(APIResponseItem):
            
            def __init__(self, response) -> None:
                super().__init__(response)

                if "template" in self.data: #
                    self.data = self.data["template"]

                self.templateName = self.data["templateName"]
                self.collections = self.data["collections"]
                self.genre = self.data["genre"]
                self.description = self.data["description"]
                self.tempo = self.data["tempo"]
                self.tags = self.data["tags"]
                

        class List(APIResponseList):
            def __init__(self, response, list_type) -> None:
                super().__init__(response, list_type)

            def resolve_item(self, list_type, item):
                if list_type == "templates":
                    return Sound.Template.Item({"data" : item})
                else:
                    raise Exception()

        @staticmethod
        def list(
            tags: Union[str, list] = "", 
            contents: Union[str, list] = "",
            collections: Union[str, list] = "",
            genre: str = "",
            tempo: str = "",
            type: str = "all"
            ) -> list:
            
            if type not in ["all", "custom", "standard"]:
                raise Exception("Invalid type supplied, should be 'all', 'custom', 'standard'")
            
            query_params = {
                "tags" : tags,
                "contents" : contents,
                "collections" : collections,
                "genre" : genre,
                "tempo" : tempo,
                "type" : type
            }
            r = Sound.interface.send_request(rtype=RequestTypes.GET, route="template", query_parameters=query_params)
            return Sound.Template.List(r, list_type="templates")
        

        def create(templateName: str, description: str=""):
            body = {
                "templateName" : templateName,
                "description" : description
            }
            r = Sound.interface.send_request(rtype=RequestTypes.POST, route="template", json=body)
            print(r)
            return Sound.Template.Item(r)


        def delete(templateName: str):
            r = Sound.interface.send_request(rtype=RequestTypes.DELETE, route="template", path_parameters=templateName)
            return APIResponseItem(r)


        def update(
            templateName: str, 
            description: str ="", 
            genre: str="", 
            collections: list=None, 
            tags: list=None):

            body = {
                "templateName" : templateName,
                "description" : description,
                "genre" : genre,
                "collections" : collections,
                "tags" : tags,
            }
            print(body)
            r = Sound.interface.send_request(rtype=RequestTypes.PUT, route="template", json=body)
            return Sound.Template.Item(r)


        def generate(energy):


            url = "https://api.soundstripe.com/v1/songs"
            headers = {
                "accept": "application/vnd.api+json",
                "content-type": "application/vnd.api+json",
                "Authorization": "Token 5CHhcP8gDa3Dn6yUYsAn8cedxEctdY0BYp2MZJLUYVIusDG0zpgnid2GCBO0KWFP"
            }

            response = requests.get(url, headers=headers, params={"filter[energy]" : energy, "filter[duration][max]" : 120})

            if response.json()["data"]:
                songId = response.json()["data"][0]["relationships"]["audio_files"]["data"][0]["id"]
                
                for resource in response.json()["included"]:
                    if resource["id"] == songId: 
                        print(resource)
                        url = resource["attributes"]["versions"]["wav"]
                        print(url)
                        r = requests.get(
                            url=url, 
                            stream=True, 
                            headers=headers
                        )

                        if r.status_code >= 400:
                            raise Exception("Failed to download file")

                        local_filename = f"file.wav"
                        with open(local_filename, "wb") as f:
                            shutil.copyfileobj(r.raw, f)
            print("Uploading......")
            mediaId = Media.create(local_filename).mediaId
            print(mediaId)
            try:
                Sound.Template.delete("soundstripe")
            except:
                pass
            r = Sound.Template.create("soundstripe", "hello world")
            print(r.message)
            r = Sound.Segment.create(mediaId, "soundstripe", "main")
            print(r.message)

    # ----------------------------------------- TEMPLATE SEGMENT -----------------------------------------
    class Segment():
        def create(mediaId: str, templateName: str, soundSegmentName: str):
            segment = {
                "templateName" : templateName,
                "segmentName" : soundSegmentName,
                "mediaId" : mediaId
            }
            r = Sound.interface.send_request(rtype=RequestTypes.POST, route="segment", json=segment)
            print(r)
            return Sound.Template.Item(r)



    # ----------------------------------------- TEMPLATE PARAMETERS -----------------------------------------
    class Parameter():
        
        @staticmethod
        def get() -> dict:
            r = Sound.interface.send_request(rtype=RequestTypes.GET, route="parameter")
            return APIResponseItem(r)