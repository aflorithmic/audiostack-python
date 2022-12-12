from audiostack.helpers.request_interface import RequestInterface
from audiostack.helpers.request_types import RequestTypes
from audiostack.helpers.api_item import APIResponseItem
from audiostack.speech.tts import TTS


from concurrent.futures import ThreadPoolExecutor
from itertools import product

class Audioform():
    interface = RequestInterface(family="orchestrator")
    
    # class Item(APIResponseItem):
        
    #     def __init__(self, response) -> None:
    #         super().__init__(response)
    #         self.url = self.data["url"]
    #         self.format = self.data["format"]

    #     def download(self, fileName="default", path="./") -> None:
            
    #         full_name = f"{fileName}.{self.format}"
    #         RequestInterface.download_url(self.url, destination=path, name=full_name)
            
        
    @staticmethod
    def create_speech(
        audience: dict,
        scriptId="", 
        scriptItem=None, 
        voice: str="", 
        speed: float=1.0,
        silencePadding: str="", 
        effect: str="",
        sections: dict={},
        useDictionary: bool=False,
        useTextNormalizer: bool=False,
        ) -> object:
                
        if scriptId and scriptItem:
            raise Exception("scriptId or scriptItem should be supplied not both")
        if not (scriptId or scriptItem):
            raise Exception("scriptId or scriptItem should be supplied")
            
        if scriptItem:
            scriptId = scriptItem.scriptId
            
        audiences = []
        if not isinstance(audience, dict):
            raise Exception(f"audience should be type dict but is type {type(audience)}")
        for key, value in audience.items():
            assert isinstance(value, list)
        
        #https://stackoverflow.com/questions/64645075/how-to-iterate-through-all-dictionary-combinations    
        keys, values = zip(*audience.items())
        results = [dict(zip(keys, p)) for p in product(*values)]
        for r in results:
            print(r)
        
        bodies = []
        for parameters in results:
            body = {
                "scriptId": scriptId,
                "voice" : voice,
                "speed" : speed,
                "silencePadding" : silencePadding,
                "effect" : effect,
                "audience" : parameters,
                "sections" : sections, 
                "useDictionary" : useDictionary,
                "useTextNormalizer" : useTextNormalizer
            }
            bodies.append(body)
                
        
        return Audioform.__awesome(scriptId, bodies=bodies)

    
    def __awesome(scriptId, bodies):
        with ThreadPoolExecutor() as exec:
            futures = {}
            for i, body in enumerate(bodies):
                futures[i] = exec.submit(
                    TTS.create, **body
                )

            
            for i, body in enumerate(bodies):

                exception = futures[i].exception()
                if exception:
                    raise RuntimeError(exception)
                
                
                r = futures[i].result()
                print(r)
                
        return f"use scriptId {scriptId} to list all created files."        
            
        



# import requests
# import time
# import os
# import json
# from functools import wraps
# import re

# import nltk
# nltk.data.path.append("/var/task/nltk_data")

# from nltk import tokenize




# STAGE = os.environ.get("STAGE", "staging")
# #STAGE = "prod"

# def time_and_print(func):
    
#     @wraps(func)
#     def timing(*args, **kwargs):
#         # print(args)
#         # print(kwargs)
#         start_time = time.time()
#         a = func(*args, **kwargs)
#         #print(func.__name__, "{:.4f}".format(time.time() - start_time))
#         return a
#     return timing


# class NormaliserInterface():
    
#     @time_and_print   
#     def ping_normaliser(text, language, use_internal_textprocessors, split_into_sentences, max_retry=3):
            
#         r = requests.post(
#             url=f"https://ms-normalizer.normalizer-{STAGE}.k8.aflr.io/normalize",
#             json={"text": text.lower(), "lang": language,  "use_text_processor" : use_internal_textprocessors, "split_into_sentences" : split_into_sentences},
#             timeout=8
#         )
        
#         if r.status_code == 200:
#             return r.text
#         else:
#             max_retry -= 1
#             if max_retry > 0:
#                 return NormaliserInterface.ping_normaliser(text, language, use_internal_textprocessors, split_into_sentences, max_retry)
#             else:
#                 return text
            
    
    
#     def group_list_of_strings(input: list, limit: int) -> list:
#         output = []
#         while input:
#             counter = limit
#             i = 0
#             while counter > 0 and i < len(input):
#                 if counter - len(input[i]) < 0:
#                     break
#                 else:
#                     counter -= len(input[i])
#                 i += 1
#             to_remove = input[0:i+1]
#             output.append(' '.join(to_remove))
#             input = input[i+1:]
        
#         return output  
    
#     def extra_split(sentences: list):
        
#         items_out = []
        
#         for s in sentences:
#             # cant use sub as each might be different
#             res = re.finditer("\d+?\.", s)
#             if res:
#                 for i in res:
#                     print(i.group(0))
#                     # cant split here otherwise we could end up with double entries
#                     s = s.replace(i.group(0), i.group(0)+"~*&^")
#                 # now we split
#                 out = s.split("~*&^")
#                 items_out += out
#             else:
#                 items_out.append(s)
            
#         return items_out    
    
#     @time_and_print
#     def ping_normaliser_in_parallel(text, language, use_internal_textprocessors):
        
#         lang_map = {
#             "de" : "german"
#         }
#         token_lang = lang_map[language] if language in lang_map else "english"
        
#         sentences = tokenize.sent_tokenize(text, language=token_lang)
#         sentences = NormaliserInterface.extra_split(sentences)
        
#         print(sentences)
        
#         # Dont need to set max_workers as it will be allocated dynamically based on available processors.
#         with ThreadPoolExecutor() as exec:
#             futures = {}
#             for i, t in enumerate(sentences):
#                 futures[i] = exec.submit(
#                     NormaliserInterface.ping_normaliser, t, language, use_internal_textprocessors, False
#                 )

#             #maps = {}
#             text_all = ""
#             for i, t in enumerate(sentences):

#                 exception = futures[i].exception()
#                 if exception:
#                     raise RuntimeError(exception)
                
#                 r = futures[i].result()
#                 #maps[i] = {"input" : t, "output" : r}
#                 text_all = text_all + r #+ str(i) 
            
#             text_all = text_all.replace("\"\"", "")

#             return text_all
        
#         return text          
