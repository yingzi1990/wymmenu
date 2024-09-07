import json
import urllib.error
import urllib.request
import os
from ..config.data import apiserver,config_path
def getworkflow(id):
    # 读取整个文件内容
    with open(f"{config_path}/token.txt", 'r', encoding='utf-8') as file:
        token = file.read()
    url = f"{apiserver}/api/Nodes/pageInfo?id={id}&password={token}"
    try:
        response = urllib.request.urlopen(url, timeout=5)
        if response.getcode() == 200:
            res = response.read()
            resdata = json.loads(res)
            if resdata.get('code')== 1:
                return resdata.get('data','')
            else:
                raise Exception(f"api error code:{resdata.get('code','')}")
        else:
            raise Exception(f"Failed to fetch file.json: HTTP Status {response.getcode()}")
    except urllib.error.URLError as e:
        raise Exception(f"{e.reason}")
    except Exception as e:
        raise Exception(f"{str(e)}")