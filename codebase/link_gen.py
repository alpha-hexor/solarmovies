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
    
    r=req.get(f"{ajax_url}get_link/{sid}")
    rabbit_link = r.json()["link"]
    
    #get final stuff
    rabbit_id = rabbit_link.split("/")[-1].split("?")[0]
    
    r =req.get(
        rabbit_link,
        headers={'referer':'https://solarmovie.pe/'}
    ).text

    site_key = re.findall(r"recaptchaSiteKey = '(.*?)'",r)[0]
    times = re.findall(r"recaptchaNumber = '(.*?)'",r)[0]
    token = gettoken(site_key)
    
    #final req
    x = req.get(f"https://rabbitstream.net/ajax/embed-4/getSources?id={rabbit_id}&_token={token}&_number={times}",headers={'X-Requested-With': 'XMLHttpRequest'}).json()
    
    """
    subtitles
    """    
    languages = [x["tracks"][i]["label"] for i in range(len(x["tracks"]))]        
    subtitles = [x["tracks"][i]["file"] for i in range(len(x["tracks"]))]
    '''
    final link part
    '''
    final_link = x["sources"][0]["file"]
    
    qualities,links = quality_parse(final_link)
    
    return languages,subtitles,qualities,links