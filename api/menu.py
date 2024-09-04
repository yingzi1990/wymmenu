import json
import urllib.error
import urllib.request
import os
from ..config.config import load_json, save_json
nowpath = os.path.dirname(os.path.abspath(__file__))
file_path =  os.path.join(os.path.join(nowpath, ".."),'config')
file_name = os.path.join(file_path,'config.josn')

def get_menu(base_url="http://192.168.1.11:8085"):
    url = f"{base_url}/api/test/menu"
    try:
        response = urllib.request.urlopen(url, timeout=5)
        print(f"Successfully fetched menu.json from {base_url}")
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
        print(f"Error fetching BizyAir news.json: {str(e)}")
        return {}