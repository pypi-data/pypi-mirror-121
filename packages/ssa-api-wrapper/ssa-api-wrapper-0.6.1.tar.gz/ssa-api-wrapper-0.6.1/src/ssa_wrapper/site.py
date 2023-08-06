import requests
import json



def working():
  url = 'https://PhoneguyAPI.phoneguytech75.repl.co/ssa/site'
  response = requests.get(url)
  json_data = json.loads(response.text)
  working = json_data['working']
  return working

def status():
   url = 'https://PhoneguyAPI.phoneguytech75.repl.co/ssa/site'
   response = requests.get(url)
   json_data = json.loads(response.text)
   working = json_data['status']
   return working
