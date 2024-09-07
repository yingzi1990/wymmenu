import os
import sys
from .route import *
from .config.data import config_path

WEB_DIRECTORY = "./js"

token_name = f"{config_path}/token.txt"
if not os.path.isfile(token_name):
    # 文件不存在，创建文件
    with open(token_name, 'w') as file:
        file.write('')