from .httpclient import HttpClient
import base64
import re
import json
import hashlib
from Cryptodome.Cipher import AES
from websocket import create_connection as ct

#global shit
req = HttpClient()
raw_domain = "https://rabbitstream.net:443"
domain = base64.b64encode(raw_domain.encode()).decode().replace("\n", "").replace("=", ".")

#decryption phrase
#pass_phrase = bytes(req.get("https://raw.githubusercontent.com/BlipBlob/blabflow/main/keys.json").json()["key"],"utf-8")

#regex
VTOKEN = r"po.src='https://www.gstatic.com/recaptcha/releases/(.*?)/recaptcha__en.js"
RECAPTOKEN = r'id="recaptcha-token" value="(.*?)"'

CODE_REGEX = r"""^\d*"""
SID_REGEX = r'{"sid":"(.*?)"'
SOURCE_REGEX = r"""\{.*\}"""

def gettoken(key):
    """
    return recap token
    """
    r=req.get(
        f"https://www.google.com/recaptcha/api.js?render={key}",
        headers={
            'cacheTime':'0'
        }
    ).text
    vtoken = re.findall(VTOKEN,r)[0]
    r=req.get(f"https://www.google.com/recaptcha/api2/anchor?ar=1&hl=en&size=invisible&cb=cs3&k={key}&co={domain}&v={vtoken}").text
    recap_token = re.findall(RECAPTOKEN,r)[0]
    
    j=json.loads(
        req.post(
            f"https://www.google.com/recaptcha/api2/reload?k={key}",
            data={
                "v" : vtoken,
                "k" : key,
                "c" : recap_token,
                "co" : domain,
                "sa" : "",
                "reason" : "q"
            },
            headers={
                'cacheTime':'0'
            }
        ).text.replace(")]}'",'')
        
    )
    
    return j[1]

def md5(data):
    return hashlib.md5(data).digest()


def get_key(salt,pass_phrase):
    '''
    function to generate key for decryption
    '''
    x = md5(pass_phrase+salt)
    current_key = x
    
    while(len(current_key) < 48):
        x = md5(x+pass_phrase+salt)
        current_key += x

    return current_key    

def decrypt(data,key):
    '''
    new function to decrypt data
    
    '''
    k = get_key(
        base64.b64decode(data)[8:16],key
    )
    
    dec_key = k[:32]
    iv = k[32:]
    
    try:
            
        p = AES.new(dec_key,AES.MODE_CBC,iv=iv).decrypt(
            base64.b64decode(data)[16:]
        ).decode()
        
        return p
    except:
        print("[*]Decryption failed")
        exit()

def quality_parse(link):
    """
    for quality parsing
    """
    links = []
    qualities =[]
    
    
    r=req.get(link)
    
    s=r.text.replace("#EXTM3U\n","").strip().split("\n")
    for i in range(0,len(s)-2+1,2):
        q=s[i].split(",")[-1].split("x")[-1] + "p"
        qualities.append(q)
        links.append(s[i+1]) 
        
    return qualities,links

#websocket simulation
def websock_simulation(iframe_id):
    '''
    will return decryption key, sources and tracks
    '''
    ws = ct("wss://wsx.dokicloud.one/socket.io/?EIO=4&transport=websocket")
    p = ws.recv()
    code = re.findall(CODE_REGEX,p)[0]
    
    #dirty impleamentation
    if code == "0":
        ws.send("40")
        p=ws.recv()
        
        code = re.findall(CODE_REGEX,p)[0]
        
        if code == "40":
            key =re.findall(SID_REGEX,p)[0]
            
            ws.send(
                '42["getSources",{"id":"'+iframe_id+'"}]'
            )
            p =ws.recv()
            x = json.loads(re.findall(SOURCE_REGEX,p)[0])
            
    return key,x