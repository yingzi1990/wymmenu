import os

version = "1000"
apiserver = "https://test.aiworkow.cn"
downserver = "https://test.aiworkow.cn"

# 获取当前文件的绝对路径
config_file_data = os.path.abspath(__file__)
# 获取当前文件的目录
config_path = os.path.dirname(config_file_data)
# 设置 BASE_PATH 为当前目录的上级目录
base_path = os.path.dirname(config_path)
# 下载模块目录
download_path = os.path.join(base_path, "down")
#api模块目录
api_path = os.path.join(base_path, "api")
