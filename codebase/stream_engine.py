import subprocess


def stream(istermux,streaming_data):
    termux_args = ['am','start','--user','0','-a','android.intent.action.VIEW','-d',streaming_data['link'],'-n']
    if istermux == "True":
        if streaming_data['player'] == "mpv":
           termux_args.append('is.xyz.mpv/.MPVActivity')
           mpv = subprocess.Popen(termux_args,stdout=subprocess.DEVNULL)
           mpv.wait()
        else:
            termux_args.append('org.videolan.vlc/org.videolan.vlc.gui.video.VideoPlayerActivity')
            vlc = subprocess.Popen(termux_args,stdout=subprocess.DEVNULL)
            vlc.wait()
    
    else:
        video_args =[
            streaming_data["player"],
            f"{streaming_data['link']}",
            "--sub-file={}".format(streaming_data["subtitle_link"])
        ]
        
        video = subprocess.Popen(video_args,stdout=subprocess.DEVNULL)
        video.wait()        
        
        
            