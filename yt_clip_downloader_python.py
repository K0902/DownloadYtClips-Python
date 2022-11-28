from requests_html import HTMLSession
from bs4 import BeautifulSoup as bs
import re
import json
import os
import random
import time



# init session



def video_info(url):
    session = HTMLSession() # initialise the session
    time.sleep(5) #ensure there is no Future exception was never retrieved error 
    # download HTML code
    response = session.get(url)
    # execute Javascript
    response.html.render(timeout=60)
    # create beautiful soup object to parse HTML
    soup = bs(response.html.html, "html.parser")
    #Initialize the result
    result = {}
    #Title
    result["title"] = soup.find("meta", itemprop="name")['content']
    #Time Stamp
    result["timeStamp"] = soup.find("div", {"class": "ytp-fine-scrubbing-seek-time"}).text
    # get the duration of the video
    result["duration"] = soup.find("span", {"class": "ytp-time-duration"}).text


    return result

def download():
    
    url = input("What is the url of the youtube clip? ")
    res = int(input("What resolution would you like the clip downloaded in? [2160/1440/1080/720/480/360/240/144] "))
    ext = input("What extension would you like the output to have? [3gp/aac/flv/m4a/mp3/mp4/ogg/wav/webm] ")
    original_file_name_question = input("Would you like to keep the title of the youtube video [Y/N} ")
    if original_file_name_question == "Y".upper():
        keep_original_title = True
    else:
        file_name = input("What would you like the file name to be? ")
        

    data = video_info(url)
    
    duration = "00:0" + data['duration']
    
    timeStamp = data['timeStamp']
    
    if keep_original_title == True:
        file_name = data['title']

    #The download command to be sent to the command line
    download_command = ('youtube-dl -f "bestvideo[height<=' + str(res) + '][ext=mp4]+bestaudio/best[height<=' + str(res) + '][ext=m4a]/' + str(ext) + '" --external-downloader ffmpeg --external-downloader-args "-ss ' + timeStamp + ' -t ' + duration + '" -o "' + str(file_name) + '" "' + url + '"') 
    print(download_command)
    os.system(download_command)

download()
