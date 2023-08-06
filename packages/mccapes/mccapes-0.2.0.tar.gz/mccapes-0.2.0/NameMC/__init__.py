import sys
sys.path.append("..")
import aiohttp
import datetime
import requests
from colorama import *
import webbrowser

def namemc_dropping(length, lang, searches):
    webbrowser.open_new(f"https://nl.namemc.com/minecraft-names?sort=asc&length_op=eq&length={length}&lang={lang}&searches={searches}")
def namemc_name(name):
    webbrowser.open_new(f"https://nl.namemc.com/search?q={name}")