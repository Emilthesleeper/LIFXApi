import requests

class MissingArgument:
    def __init__(self,error) -> None:
        self.error=error
        print(self.error)

class LIFX:
    def __init__(self,token,**options) -> None:
        self.token=token
        self.headers={"Authorization": "Bearer %s" % token,}
    def list_all_lights(self):
        return requests.get('https://api.lifx.com/v1/lights/all', headers=self.headers).json()
    def toggle_power(self, duration=1, namearg=None):
        lamps=self.list_all_lights()
        possible=False
        if namearg !=None:
            for a in lamps:
                if a["id"] == namearg:
                    possible=True
                elif a["product"]["name"]==namearg or a["product"]["identifier"]==namearg or a["uuid"]==namearg:
                    namearg==a["id"]
                    possible=True
        if possible ==True:
            return requests.post(f'https://api.lifx.com/v1/lights/{namearg}/toggle', headers=self.headers, json={"duration:": duration}).json()
        else:
            print("Error, wrong arg \"namearg\" or str \"namearg\" not given.")
    def set_state(self, namearg=None, power:str=None, color_hex:str=None, brightness:int=None, duration:int=None, infrared:int=None, fast:bool=None):
        color=color_hex
        lamps=self.list_all_lights()
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