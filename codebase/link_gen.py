from .httpclient import HttpClient
import re
from .utils import *


#global shit
req = HttpClient()
ajax_url = "https://solarmovie.pe/ajax/"

def get_final_link(ismovie,id):
    """
    get final streaming link and subtitle links

    Args:
        ismovie (bool): true/false
        id (str): movie_id / series_id
    return:
        streaming_link/quality ,subtitle/language
        
    """
    if ismovie:
        #if movie
        r=req.get(f"{ajax_url}movie/episodes/{id}").text
        
        #get the first server id
        sid = re.findall(r'data-linkid="(\d+)"',r)[0]
        
    else:
        r=req.get(f"{ajax_url}v2/episode/servers/{id}/#servers-list").text
                
        #get the first server id
        sid = re.findall(r'data-id="(\d+)"',r)[0]
    
    #generate rabbit stream link
    
    iframe_link =req.get(f"{ajax_url}sources/{sid}").json()["link"]
    #print(iframe_link)
    
    #get final stuff
    iframe_id = re.findall(r'embed-\d.*\/(.*)\?',iframe_link)[0]
    #final_link = re.findall(r'(https:\/\/.*\/embed-4)',iframe_link)[0].replace("embed-4","ajax/embed-4/")
    # final_link = f"https://{yarl.URL(iframe_link).host}/ajax/embed-4/"
    
    # #final req
    # x = req.get(
    #     f"{final_link}getSources?id={iframe_id}",
    #     headers={
    #         'X-Requested-With': 'XMLHttpRequest'
    #     }
    # ).json()
    #print(x)
    
    #ws simulation
    key , x = websock_simulation(iframe_id)
    """
    subtitles
    """    
    languages = [x["tracks"][i]["label"] for i in range(len(x["tracks"]))]        
    subtitles = [x["tracks"][i]["file"] for i in range(len(x["tracks"]))]
    '''
    final link part
    '''
    final_link = re.findall(r'{"file":"(.*?)"'
        ,decrypt(x["sources"],bytes(key,"utf-8")))[0]
    
    qualities,links = quality_parse(final_link)
    
    return languages,subtitles,qualities,links