import os
import shutil
import requests
import json
import time
from typing import List, Tuple, Optional
from zipfile import ZipFile

from ..constants.paths import BGT_DATA_PATH
from ..helpers.hash import bgt_hash


def download_bgt_data(
    wkt_geometry: str, layer_names: str
) -> Tuple[bool, Optional[str]]:
    path_prefix = os.path.join(BGT_DATA_PATH, bgt_hash(wkt_geometry))
    zip_path = f"{path_prefix}.zip"

    if os.path.exists(zip_path):
        return True, "taken from cache"

    if not os.path.exists(BGT_DATA_PATH):
        os.makedirs(BGT_DATA_PATH)

    url = "https://api.pdok.nl/lv/bgt/download/v1_0/full/custom"
    head = {"accept": "application/json", "Content-Type": "application/json"}
    stat_head = {"accept": "application/json"}
    data = {
        "featuretypes": layer_names,
        "format": "citygml",
        "geofilter": wkt_geometry,
    }

    # Request data
    response = requests.post(url, headers=head, json=data)
    if response.status_code != 202:
        return False, response._content.decode("utf-8")
    response_load = json.loads(response.text)

    # Check server status
    stat_link = "https://api.pdok.nl" + response_load["_links"]["status"]["href"]
    status = json.loads(requests.get(stat_link, headers=stat_head).text)["status"]
    if not status in ["PENDING", "RUNNING", "COMPLETED"]:
        return False, status
    while status != "COMPLETED":
        time.sleep(0.5)
        status_load = json.loads(requests.get(stat_link, headers=stat_head).text)
        status = status_load["status"]

    # Create download link
    download_link = "https://api.pdok.nl" + status_load["_links"]["download"]["href"]

    # Save files
    dl_file = requests.get(download_link)
    open(zip_path, "wb").write(dl_file.content)
    with ZipFile(zip_path, "r") as zip:
        # We do not use zip.extractall, because it does not perform sanitization
        for file in zip.infolist():
            zip.extract(file, BGT_DATA_PATH)
            shutil.move(
                os.path.join(BGT_DATA_PATH, file.filename),
                f"{path_prefix}_{file.filename}",
            )

    return True, None
