import httpx
import re
import base64
import hashlib
import yarl
from Cryptodome.Cipher import AES


client = httpx.Client(headers={'user-agent':'UWU'})


ajax_url = "https://solarmovie.pe/ajax/"
key = bytes(client.get("https://raw.githubusercontent.com/BlipBlob/blabflow/main/keys.json").json()["key"],"utf-8")


#decryption shit
def md5(data):
    return hashlib.md5(data).digest()

def get_key(salt):
    x = md5(key+salt)
    currentkey = x
    while(len(currentkey) < 48):
        x = md5(x+key+salt)
        currentkey += x
    return currentkey
    

def unpad(s):
    
    return s[:-ord(s[len(s) - 1:])]

def decrypt(data):
    k = get_key(
        base64.b64decode(data)[8:16]
    )
    
    
    

    dec_key = k[:32]
   
    iv = k[32:]
    
    
    p= AES.new(dec_key,AES.MODE_CBC,iv=iv).decrypt(
        base64.b64decode(data)[16:]
    )
    
    
    return p
    
    
    

movie_url = "https://solarmovie.pe/movie/watch-thor-love-and-thunder-free-66670"

movie_id = re.findall(r"\d+",movie_url)[0]





x = client.get(f"{ajax_url}movie/episodes/{movie_id}").text
#get sid
sid =re.findall(r'data-linkid="(\d+)"',x)[0]

#iframe link
iframe_link=client.get(f"{ajax_url}sources/{sid}").json()["link"]
print(iframe_link)

iframe_id = re.findall(r'embed-\d-v2\/(.*)\?',iframe_link)[0]
print(iframe_id)
host = yarl.URL(iframe_link).host
print(host)
#final_link = re.findall(r'(https:\/\/.*\/embed-4-v2)',iframe_link)[0].replace("embed-4-v2","ajax/embed-4-v2/")
#print(final_link)

r=client.get(f"https://{host}/ajax/embed-4/getSources?id={iframe_id}",
             headers={
                 'X-Requested-With': 'XMLHttpRequest'
             }).json()

print(r)

if r['encrypted'] :
    print(decrypt(r["sources"]))
else:
    print(r['sources'][0]['file'])
    




