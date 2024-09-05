import json
import urllib.error
import urllib.request
import os

def getmenu(base_url,pids):
    url = f"{base_url}/api/Nodes/pageList?pids={pids}"
    try:
        response = urllib.request.urlopen(url, timeout=5)
        if response.getcode() == 200:
            data = response.read()
            res = json.loads(data)
            return res.get('data','')
        else:
            print(f"Failed to fetch news.json: HTTP Status {response.getcode()}")
            return {}
    except urllib.error.URLError as e:
        print(f"Error fetching news.json: {e.reason}")
        return {}
    except Exception as e:
        print(f"Error fetching wymcomfy news.json: {str(e)}")
        return {}