import sys
sys.path.append("..")
from .loginms import login as login_acc
import aiohttp
import datetime
import requests
from colorama import *
from datetime import datetime
def names(email, password):
    try:
        text = login_acc(email, password)
        token = text["access_token"]

        headers = {"Content-type": "application/json", "Authorization": "Bearer " + token}
        headers2 = {"Authorization": "Bearer " + token}
        headers3 = {"Content-type": "application/json"}


        f = requests.get(f"https://api.minecraftservices.com/minecraft/profile",headers=headers2).json()
        playername = f['name']
        f2 = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{playername}").json()
        uuid = f2['id']


        
        r = requests.get(f"https://api.mojang.com/user/profiles/{uuid}/names").json()
        for name in r:
            names = name['name']
            try:
                time = name['changedToAt']
                ts = int(time)
                print(f"{Fore.BLUE}Name {Fore.WHITE}:{Fore.GREEN} " + names)
                print(f"{Fore.WHITE}")
            except:
                pass
    except:
        pass