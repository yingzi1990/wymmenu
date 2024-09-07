import json
import urllib.request
import urllib.error
from ..config.data import apiserver,config_path

def login(code):
    url = f"{apiserver}/api/Nodes/login?code={code}"
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            if response.getcode() == 200:
                res = response.read()
                resdata = json.loads(res)
                if resdata.get('code')== 1:
                    # 登录成功
                    data = resdata.get('data', {})
                    token = data.get('password', '')
                    # 存储 token 到文件
                    with open(f"{config_path}/token.txt", 'w', encoding='utf-8') as file:
                        file.write(token)
                    return token
                else:
                    raise Exception(f"api error code:{resdata.get('code','')}")
            else:
                raise Exception(f"Error login: HTTP Status {response.getcode()}")
    except urllib.error.URLError as e:
        raise Exception(f"Error login: {e.reason}")
    except json.JSONDecodeError as e:
        raise Exception(f"Error decoding JSON: {str(e)}")
    except Exception as e:
        raise Exception(f"{str(e)}")
