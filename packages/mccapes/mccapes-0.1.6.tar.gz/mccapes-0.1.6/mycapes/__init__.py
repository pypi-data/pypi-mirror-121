import sys
sys.path.append("..")
from .loginms import login as login_acc
import aiohttp
import datetime
import requests
from colorama import *
def capes(email, password):
    text = login_acc.login(email, password)
    token = text["access_token"]

    headers = {"Content-type": "application/json", "Authorization": "Bearer " + token}
    headers2 = {"Authorization": "Bearer " + token}
    name = "unperformed"
    r = requests.get(f"https://api.minecraftservices.com/minecraft/profile",headers=headers2).json()
    for item in r["capes"]:
        print(f"{Fore.BLUE}name {Fore.WHITE}:{Fore.GREEN} " + item['alias'])
        print(f"{Fore.BLUE}cape state {Fore.WHITE}:{Fore.GREEN} " + item['state'])
        print(f"{Fore.BLUE}cape id {Fore.WHITE}:{Fore.GREEN} " + item['id'])
        print(f"{Fore.BLUE}cape url {Fore.WHITE}:{Fore.GREEN} " + item['url'])