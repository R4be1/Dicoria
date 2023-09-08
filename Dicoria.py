import sys
import time
import mmh3
import json
import base64
import hashlib
import aiohttp
import asyncio
import traceback
from urllib.parse import urljoin
from urllib.parse import urlparse

async def requests_async_function_(tasks, URL=True, STATUS_CODE=True, TEXT_LENGTH=True, HEADERS=True, TEXT=True, CONTENT=False, semaphore=2048):
    media_type = ["image/","video/","audio/","application/zip","application/x-rar-compressed","application/x-tar","application/gzip","application/x-7z-compressed","application/pdf","application/msword","application/vnd.ms-excel","application/vnd.ms-powerpoint","application/font"]
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=700),connector=aiohttp.TCPConnector(ssl=False)) as session:
        _semaphore = asyncio.Semaphore(semaphore) if semaphore else asyncio.Semaphore()

        async def async_request(task):
            if not task: return dict()
            try:
                async with _semaphore:
                    start_time=time.time()
                    async with session.request(
                            url = urljoin( task.get( "webroot" ),task.get("path") ),
                            method = "GET" if not task.get( "data" ) else "POST",
                            timeout = aiohttp.ClientTimeout( total=174 ),
                            params = task.get( "params" ),
                            data = task.get( "data" )
                            ) as response:

                        if response is not None:
                            print(f"[{response.status}] {response.url}")

                            if TEXT_LENGTH==True and TEXT==True:
                                response.text = await response.text(errors="replace")
                                response.text_length = len( response.text )

                            elif TEXT_LENGTH==True and TEXT==False:
                                response.text = await response.text(errors="replace")
                                response.text_length = len( response.text )
                                response.text = str()

                            else:
                                response.text = await response.text(errors="replace") if TEXT else str()

                            response.content = await response.read() if CONTENT else str()
                            content_type = response.headers.get("Content-Type")

                            for _type in media_type:
                                if content_type and _type in content_type:
                                    response.text=str()

                        return {
                                "url" : str(response.url) if URL else str(),
                                "status_code" : response.status if STATUS_CODE else int(),
                                "text-length" : response.text_length if TEXT_LENGTH else int(),
                                "headers" : dict(response.headers) if HEADERS else dict(), 
                                "text" : str(response.text) if TEXT else str(), 
                                "content" : responses.content if CONTENT else bytes()
                                }

            except Exception as e:
                # print(f"\033[91m[!] {urljoin( task.get('webroot'), task.get('path')) }  Exception:{e}\033[0m")
                # print(f"[!] Exception:{traceback.format_exc()}")
                return dict()

        tasks = [asyncio.create_task(async_request(task)) for task in tasks]
        responses = await asyncio.gather(*tasks)
    return responses

def requests_responses(tasks, semaphore=2048) -> list():
    responses = asyncio.run(requests_async_function_(tasks,semaphore))
    return responses

class IdentCMS:
    def __init__(self):
        self.Fingers=list()
        self.CMSFinger1=json.load(open("CMSFinger1.json"))
        self.CMSFinger2=json.load(open("CMSFinger2.json"))

    def gen(self,webroot):
        finger_url=list()
        webroot=webroot[:-1] if webroot.endswith("/") else webroot

        finger_url.append(webroot+"/")
        finger_url.append(webroot+"/favicon.ico")

        for finger in self.CMSFinger1:
            finger_url.append( webroot+finger["url"] if finger["url"].startswith("/") else webroot+"/"+finger["url"] )

        finger_url=list( set(finger_url) )
        return finger_url


    def ident(self, response):
        if not response.get("url"):
            return self.Fingers

        for finger in self.CMSFinger1:
            if finger["url"] in response["url"] and finger["url"]!="/":
                if finger["md5"] and finger["md5"] == MD5(response["content"]):
                    self.Fingers.append( finger["name"] )

                elif finger["re"] and response["text"].find(finger["re"])!=-1:
                    self.Fingers.append( finger["name"] )

        for finger in self.CMSFinger2["fingerprint"]:

            if finger["method"]=="keyword" and finger["location"]=="body":
                if all([ response["text"].find(_keyword)!=-1 for _keyword in finger["keyword"] ]):
                    self.Fingers.append( finger["cms"] )

            elif finger["method"]=="keyword" and finger["location"]=="header":
                for _keyword in finger["keyword"]:
                    if _keyword in str( response["headers"] ):
                        self.Fingers.append( finger["cms"] )

            elif finger["method"]=="icon_hash" and response["url"].endswith(".ico"):
                for _hash in finger["keyword"]:
                    if HASH(response["content"])==_hash:
                        self.Fingers.append( finger["cms"] )

        self.Fingers=list( set(self.Fingers) )
        return self.Fingers

def Parameter(para):
    if para in sys.argv:
        para=sys.argv.index(para)
        para=sys.argv[para+1] if len(sys.argv) > para+1 else None
        return para

def progress_bar(title, iterable, bar_length=50):
    total_length = len(iterable)
    
    for index, item in enumerate(iterable):
        percent = (index + 1) / total_length

        arrow = '▆' * int(round(percent * bar_length) - 1)
        spaces = ' ' * (bar_length - len(arrow))

        sys.stdout.write(f'\r  [{title}] [{arrow + spaces}] {percent * 100:.2f}%')
        sys.stdout.flush()

        yield item


def HASH(content):
    icon_hash=mmh3.hash( base64.encodebytes(content) )
    return str(icon_hash)

def MD5(content):
    return hashlib.md5(content).hexdigest()

if __name__=="__main__":
    IdentCMSer=IdentCMS()
    print('''\033[1;5;31m
          _______    _________ 
  ____    \   _  \   \_____   \\
 /  _ \   /  /_\  \     /   __/
(  <_> )  \  \_/   \   |   |   
 \____/ /\ \_____  /   |___|   
        \/       \/    <___>  By Rebel.
    \033[0m''')

    if "-u" in sys.argv and Parameter("-u"):

        responses = requests_responses(
            [ {"webroot" : _ } for _ in IdentCMSer.gen(Parameter("-u")) ]
        )
      
        for response in progress_bar(f"Dicoria Identify CMS", responses):
            IdentCMSer.ident(response)

        print() 

        for finger in IdentCMSer.Fingers:
            print("    \033[1;31m"+finger+"\033[0m")

        print()

    else:
        print("How to use?  python3 Dicoria.py -u 'http://www.example.com' ")
