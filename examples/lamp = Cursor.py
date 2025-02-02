import threading
import requests
import nltk

class MissingArgument:
    def __init__(self,error) -> None:
        self.error=error
        print(self.error)

class LIFX:
    def __init__(self,token,**options) -> None:
        self.token=token
        self.headers={"Authorization": "Bearer %s" % token,}
    def lamps(self):
        return requests.get('https://api.lifx.com/v1/lights/all', headers=self.headers).json()
    def toggle(self,namearg=None):
        lamps=self.lamps()
        possible=False
        if namearg !=None:
            for a in lamps:
                if a["id"] == namearg:
                    possible=True
                elif a["product"]["name"]==namearg or a["product"]["identifier"]==namearg or a["uuid"]==namearg:
                    namearg==a["id"]
                    possible=True
        if possible ==True:
            return requests.post(f'https://api.lifx.com/v1/lights/{namearg}/toggle', headers=self.headers).json()
        else:
            print("Error, wrong arg \"namearg\" or str \"namearg\" not given.")
    def put(self,namearg=None,power:str=None,color_hex:str=None,brightness:int=None,duration:int=None,infrared:int=None,fast:bool=None):
        color=color_hex
        lamps=self.lamps()
        possible=False
        if namearg !=None:
            for a in lamps:
                if a["id"] == namearg:
                    possible=True
                    save=a
                elif a["product"]["name"]==namearg or a["product"]["identifier"]==namearg or a["uuid"]==namearg:
                    namearg=a["id"]
                    save=a
                    possible=True
        for a in lamps:
            if a["id"]==namearg:
                save=a
        if power==None:
            power=save["power"]
        if color==None:
            color="#ffffff"
        if brightness==None:
            brightness=save["brightness"]
        if duration==None:
            duration=0
        if duration >=3155760000.0:
            return "Duration can't be higher than 10 years in seconds"
        if infrared==None:
            infrared=0
        if fast ==None:
            fast=False
        payload={
            "power":power,
            "color":color,
            "brightness":brightness,
            "duration":duration,
            "infrared":infrared,
            "fast":fast,
        }
        if possible ==True:
            return requests.put(f'https://api.lifx.com/v1/lights/{namearg}/state', headers=self.headers,data=payload).json()
        else:
            raise MissingArgument("Error, wrong arg \"namearg\" or str \"namearg\" not given.")

import time
import pyautogui
from PIL import ImageGrab

lifx=LIFX(token="")
lamp_id=""
run=True



def do_loop():
    global run, lamp_id
    while run:
        time.sleep(0.5)
        image = ImageGrab.grab(include_layered_windows=True)
        pos=pyautogui.position()
        print((pos.x+3,pos.y+3))
        try:
            rgb=image.getpixel((pos.x+3,pos.y+3))
            image.getcolors()
            color='#%02x%02x%02x' % rgb
            print(color)
            brightness=sum([rgb[0],rgb[1],rgb[2]])/3/2.55
            brightness/=100
            print(brightness)
            lifx.put(namearg=lamp_id,power="on",color_hex=color,brightness=brightness,duration=0.6)
        except KeyboardInterrupt:
            exit()
        except Exception as e:
            print(e.args[0])

t1=threading.Thread(target=do_loop)
t1.start()
input()
run=False
t1.join()
lifx.put(namearg=lamp_id,power="off",duration=2)