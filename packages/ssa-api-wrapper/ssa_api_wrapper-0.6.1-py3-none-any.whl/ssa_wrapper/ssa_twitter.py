import requests
import json

def latesttweet():
    url = 'https://PhoneguyAPI.phoneguytech75.repl.co/ssa/latesttweet'
    response = requests.get(url)
    json_data = json.loads(response.text)
    return json_data
