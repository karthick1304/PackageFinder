import urllib
import json
import requests
def getRepoData(repourl):
      repourl=str(repourl)
      with urllib.request.urlopen(repourl) as url:
        data = json.loads(url.read().decode()) 
        return data