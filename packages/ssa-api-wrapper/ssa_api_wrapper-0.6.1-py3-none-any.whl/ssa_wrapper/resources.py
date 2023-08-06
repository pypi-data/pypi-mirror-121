import requests
import json


def sharepoint():
    url = 'https://PhoneguyAPI.phoneguytech75.repl.co/ssa/sharepoint'
    response = requests.get(url)
    json_data = json.loads(response.text)
    working = json_data['url']
    return working

def remote():
    url = 'https://PhoneguyAPI.phoneguytech75.repl.co/ssa/remote'
    response = requests.get(url)
    json_data = json.loads(response.text)
    working = json_data['url']
    return working
