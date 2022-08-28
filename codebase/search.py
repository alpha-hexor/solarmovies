from .httpclient import HttpClient
import re

req = HttpClient()

#global shit
url = "https://solarmovie.pe/"
movie_regex = r'"(/movie/.*?)"'
tv_regex = r'"(/tv/.*?)"'

def search(query):
    """
    function to search movies and shows
    """
    r=req.get(f"{url}search/{query}").text
    #print(r)
    x = re.findall(movie_regex,r) + re.findall(tv_regex,r)
    x = list(set(x))
    return x   

def get_seasons(id):
    """
    function to return no. of seasons and season ids
    """
    r=req.get(f"{url}ajax/v2/tv/seasons/{id}").text
    ids = re.findall(r'data-id="(\d+)"',r)
    return ids

def get_episodes(id):
    """
    function to get episode id and no. of episodes
    """
    r=req.get(f"{url}ajax/v2/season/episodes/{id}").text
    #print(r)
    ids = re.findall(r'data-id="(\d+)"',r)
    return ids