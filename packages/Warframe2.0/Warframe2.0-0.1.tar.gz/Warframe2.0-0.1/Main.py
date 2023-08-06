import os
import json
from dotenv import load_dotenv
import requests
import datetime
from datetime import datetime

def LoadFiles():
    load_dotenv()

def warframe():
    #         /\       #
    #      Imports     #
    #------------------#
    #      Requests    #
    #         \/       #
    r = 'https://api.warframestat.us/pc/en'

    website = requests.get(r)
    data = json.loads(website.content)

    time = ''

    events = []
    for item in data['news']:
        Link, Link2 = item['message'], item['link']
        time = item['date']
        style = f"""
    {Link}
    Link: {Link2}
        
        """
        events.append(style)
    list_count = len(events)
    index = list_count//2

    split_list, split_list_other = events[:index], events[index:]
    split_count = len(split_list)
    index2 = split_count//2
    split_last = split_list[:index2]

    linked = "\n".join(f'{a}. {b}' for a, b in enumerate(split_last, 1))
    print(linked)
    events.clear

    #         /\       #
    #      Requests    #
    #------------------#
    #        Time      #
    #         \/       #
    current_time = datetime.now()
    time_current = f"{current_time.year}-{current_time.month}-{current_time.day}"
    final_time_current = time_current.replace('-', '')
    splitat = 10
    left, right = time[:splitat], time[splitat:]

    left_fixed = ''.join(left[i] for i in range(len(left)) if i != 5)

    final_time_json = left_fixed.replace('-', '')

    # Comparison Numbers Below, Real Numbers Above
    final_latest = int(final_time_json)

    final_current = int(final_time_current)
    print(time_current)
    print(left_fixed)


    if final_current > final_latest:
        print('Dude ur so low')
        print(Link)
    else:
        print('Dude ur so high')

    with open('info.png', 'r') as f:
        data = json.load(f)
        f.close

#         /\       #
#  Time Detector   #
#------------------#
#  Key Foundation  #
#         \/       #
def LoadSecrets():
    secrets = 'AreaKey'

    l = os.getenv(secrets)
    if l is None:
        exit(1)
    print(l)
    l1 = os.getenv(str(l))
    print(l1)
    l2 = bool(os.getenv(str(l1)))

#         /\       #
#  Key Foundation  #
#------------------#
#      End Code    #
#         \/       #


# Created and mantained by Blake Thompson
# Directly contact me through discord or email
# Email: blakethompsonbat@gmail.com
# Discord: N/A
