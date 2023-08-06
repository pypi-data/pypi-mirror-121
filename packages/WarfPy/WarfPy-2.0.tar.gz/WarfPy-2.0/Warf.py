import os
import json
from dotenv import load_dotenv
import requests
import datetime
from datetime import datetime
from copy import deepcopy

r = 'https://api.warframestat.us/pc/en'
void = 'https://api.warframestat.us/pc/voidTrader'

website = requests.get(r)
website2 = requests.get(void)
data = json.loads(website.content)
void_data = json.loads(website2.content)


def LoadDiscordToken():
    load_dotenv()


def LoadRequirements():
    print('Loading All Configs')
    os.system("pip install -r requirements.txt")
    print('Done!')

def warframe_all():
    return data['news']
    
def warframe_news():
    style = {}
    things = []
    number = 0
    for item in data['news']:
        number = number + 1
        item, item2 = item['message'], item['link']

        style = {f"{number}": f"{item}", f"Link{number}": f"{item2}"}

        things.append(deepcopy(style))
    json_obj = json.dumps(things)
    json_real = json.loads(json_obj)
    return json_real


def warframe_void():
    isActive = void_data['active']
    location = void_data['location']
    inventory = void_data['inventory']
    activeUntil = void_data['endString']
    send = {"isActive": f"{isActive}", "location": f"{location}",
            "inventory": f"{inventory}", "activeUntil": f"{activeUntil}"}
    send_data = json.loads(json.dumps(send))
    return send_data





            

            
        



#         /\       #
#  Key Foundation  #
#------------------#
#      End Code    #
#         \/       #


# Created and mantained by Blake Thompson
# Directly contact me through discord or email
# Email: blakethompsonbat@gmail.com
# Discord: N/A
