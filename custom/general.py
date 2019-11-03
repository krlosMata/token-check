import urllib.request
import json

def getApi(_stringApi):
    req = urllib.request.Request(_stringApi, headers={'User-Agent': 'Mozilla/5.0'})   
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
    return data

def getApiSign(_req): 
    with urllib.request.urlopen(_req) as response:
        data = json.loads(response.read().decode())
    return data

def getApiSign(_stringApi,_headers): 
    req = urllib.request.Request(_stringApi, _headers={'User-Agent': 'Mozilla/5.0'})   
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
    return data

def readJson(arxiu):
  with open(str(arxiu)) as conf_file:
    variable = json.load(conf_file)
  return variable

def writeJson(variable, arxiu):
  with open(str(arxiu), 'w+') as conf_file:
    json.dump(variable,conf_file)