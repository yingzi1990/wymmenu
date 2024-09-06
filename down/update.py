import requests
import zipfile
import os
from ..config.data import downserver,version

def check_for_updates():
    response = requests.get('https://example.com/latest_version')
    latest_version = response.text.strip()

    # Assuming you store the current version in a file
    with open('current_version.txt', 'r') as f:
        current_version = f.read().strip()

    if latest_version > current_version:
        download_update(latest_version)

def download_update(version):
    url = f'https://example.com/updates/{version}.zip'
    response = requests.get(url)
    with open('update.zip', 'wb') as f:
        f.write(response.content)

    with zipfile.ZipFile('update.zip', 'r') as zip_ref:
        zip_ref.extractall('path/to/update')

    # Optionally, restart the application
    os.system('restart_application_command')

check_for_updates()
