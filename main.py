import youtube_dl, os
from pytube import YouTube 
from pytube.cli import on_progress
import datetime

def Download_Partially():
    # 獲得基本資訊
    date_string = datetime.date.today().strftime("%Y-%m-%d")
    URL = input("VIDEO URL: ")
    FROM = input("START TIME: (hh:mm:ss) ")
    TO = input ("END TIME: (hh:mm:ss) ")
    TARGET = input("FILE NAME: ") + f"{date_string}" + ".mp4" 

    # 用 Youtube-dl 獲取影片所有 metadata
    with youtube_dl.YoutubeDL({'format': 'best'}) as ydl:
        result = ydl.extract_info(URL, download=False)
        video = result['entries'][0] if 'entries' in result else result

    # 使用 ffmpeg 切割下載
    url = video['url']
    os.system('ffmpeg -i "%s" -ss %s -t %s -c:v copy -c:a copy "%s"' % (url, FROM, TO, TARGET))

def Just_Download():
    url = input("VIDEO URL: ")
    NAME = input("FILE NAME: ")
    print('Downloading...') 
    date_string = datetime.date.today().strftime("%Y-%m-%d")
    yt = YouTube (url, on_progress_callback=on_progress, use_oauth=True, allow_oauth_cache=True)    
    stream = yt.streams.filter (progressive=False, file_extension='mp4').get_highest_resolution ()
    print ('Now downloading:', yt.title)
    print ('Size:', round (stream.filesize/1000000), 'MB')
    stream.download (filename= f"{NAME} {date_string}")
    print ('Done!')

print("How do you like your download?")
print("1. Just download the whole video")
print("2. Download part of the video")
option = input("(1 or 2)")

if option == "1":
    Just_Download()
elif option == "2":
    Download_Partially()
else:
    print("wrong option, please restart.")


