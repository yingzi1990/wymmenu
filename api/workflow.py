import json
import urllib.error
import urllib.request
import os
from ..config.data import apiserver,config_path
def getworkflow(id):
    # 读取整个文件内容
    with open(f"{config_path}/token.txt", 'r', encoding='utf-8') as file:
        token = file.read()
    if not token:
        raise Exception("Token is empty")
    url = f"{apiserver}/api/Nodes/pageInfo?id={id}&password={token}"
    try:
        response = urllib.request.urlopen(url, timeout=5)
        if response.getcode() == 200:
            data = response.read()
            res = json.loads(data)
            return res.get('data','')
        else:
            raise Exception(f"Failed to fetch file.json: HTTP Status {response.getcode()}")
    except urllib.error.URLError as e:
        raise Exception(f"Error fetching file.json: {e.reason}")
    except Exception as e:
        raise Exception(f"Error fetching file.json: {str(e)}")