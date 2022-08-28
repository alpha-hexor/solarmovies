import sys
from codebase.search import *
from codebase.link_gen import *
from codebase.stream_engine import *
from fzf import process,fzf_prompt
import os
import json
import platform

#load the settings
f=open(os.getcwd()+"\\settings.json")
data = json.load(f)
istermux = data['istermux']
player = data['video_player']
quality = data["quality"]

#fzf executable
if platform.system() == "Windows":
    process.EXECUTABLE = os.getcwd()+"\\fzf.exe"

streaming_data={}
streaming_data["player"] = player


query = ""
if len(sys.argv) < 2 :
    query = input("[*]Search movie/series: ").replace(" ","-")
    
else:
    for i in sys.argv[1:]:
        query=query+i+"-"
    query = query.strip("-")

shows = search(query)

show_to_watch = fzf_prompt(shows)

if "/tv/" in show_to_watch:
    #if series
    show_id = re.findall(r'\d+',show_to_watch)[0]
    season_ids = get_seasons(show_id)
    x=int(input(f"[*]Available Seasons-{len(season_ids)}: "))
    episode_ids =get_episodes(season_ids[x-1])
    y=int(input(f"Available Episodes-{len(episode_ids)}: "))
    languages,subtitles,qualities,links=get_final_link(False,episode_ids[y-1])
else:
    #if movie
    movie_id = re.findall(r'\d+',show_to_watch)[0]
    languages,subtitles,qualities,links=get_final_link(True,movie_id)
    
if istermux == "False":
    #get subtitles
    s=fzf_prompt(languages)
    streaming_data["subtitle_link"] = subtitles[languages.index(s)]

if quality == "low" or quality == "Low":

    streaming_data["link"] = links[-1]
    

elif quality == "high" or quality == "High":
    streaming_data["link"] = links[0]

else:
    q = fzf_prompt(qualities)
    streaming_data["link"] = links[qualities.index(q)]
    
stream(istermux,streaming_data)
    

   
        
    
    
    

    