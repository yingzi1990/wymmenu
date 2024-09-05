import json
import urllib.error
import urllib.request
import os

def getworkflow(base_url,id):
    url = f"{base_url}/api/Nodes/pageInfo?id={id}"
    try:
        response = urllib.request.urlopen(url, timeout=5)
        if response.getcode() == 200:
            data = response.read()
            res = json.loads(data)
            return res.get('data','')
        else:
            print(f"Failed to fetch file.json: HTTP Status {response.getcode()}")
            return {}
    except urllib.error.URLError as e:
        print(f"Error fetching file.json: {e.reason}")
        return {}
    except Exception as e:
        print(f"Error fetching file.json: {str(e)}")
        return {}