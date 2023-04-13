import requests
import json
import time
import os
from typing import Tuple, Optional
from zipfile import ZipFile

from ..constants import BGT_DATA_PATH

def download_bgt_data(wkt_geometry: str) -> Tuple[bool, Optional[str]]:
    url = 'https://api.pdok.nl/lv/bgt/download/v1_0/full/custom'
    head = {'accept': 'application/json',
            'Content-Type': 'application/json'}
    stat_head = {'accept': 'application/json'}
    data = {
        "featuretypes": [
            "bak",
            "gebouwinstallatie",
            "kunstwerkdeel",
            "onbegroeidterreindeel",
            "begroeidterreindeel"
        ],
        "format": "citygml",
        "geofilter": wkt_geometry
    }
    
    # Request data
    response = requests.post(url, headers=head, json=data)
    response_load = json.loads(response.text)
    
    # Check server status
    stat_link = "https://api.pdok.nl" + response_load['_links']['status']['href']
    status = json.loads(requests.get(stat_link, headers=stat_head).text)['status']
    if not status in ["PENDING", "RUNNING", "COMPLETED"]:
        return False, status
    while status != "COMPLETED":
        time.sleep(0.5)
        status_load = json.loads(requests.get(stat_link, headers=stat_head).text)
        status = status_load['status']

    # Create download link
    download_link = "https://api.pdok.nl" + status_load['_links']['download']['href']

    # Removes file if it exists already
    if os.path.isdir(BGT_DATA_PATH):
        os.remove(BGT_DATA_PATH)
    os.mkdir(BGT_DATA_PATH)

    # Save files
    dl_file = requests.get(download_link)
    zip_path = f"{BGT_DATA_PATH}/tmp.zip"
    open(zip_path, 'wb').write(dl_file.content)
    with ZipFile(zip_path, 'r') as zip:
        # We do not use zip.extractall, because it does not perform sanitization
        for file in zip.infolist():
            zip.extract(file, BGT_DATA_PATH)
    os.remove(zip_path)

    return True, None