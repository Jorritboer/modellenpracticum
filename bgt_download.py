import requests
import json
import time
import os

def download_bgt_area(filename: str, area: str):
    url = 'https://api.pdok.nl/lv/bgt/download/v1_0/full/custom'
    head = {'accept': 'application/json',
            'Content-Type': 'application/json'}
    stat_head = {'accept': 'application/json'}
    data = {
    "featuretypes": [
        "bak",
        "gebouwinstallatie",
        "kunstwerkdeel",
        "onbegroeidterreindeel"
    ],
    "format": "citygml",
    "geofilter": area
    }
    
    # Request data and receive request id
    response = requests.post(url, headers=head, json=data)
    response_load = json.loads(response.text)
    download_ID = response_load['downloadRequestId']
    
    # Check server status
    stat_link = "https://api.pdok.nl" + response_load['_links']['status']['href']
    status = json.loads(requests.get(stat_link, headers=stat_head).text)['status']
    if status != "RUNNING" and status != "COMPLETED":
        return None
    while status != "COMPLETED":
        time.sleep(0.5)
        status_load = json.loads(requests.get(stat_link, headers=stat_head).text)
        status = status_load['status']

    # Create download link
    download_link = "https://api.pdok.nl" + status_load['_links']['download']['href']

    # Removes file if it exists already
    if os.path.isfile(filename):
        os.remove(filename)

    # Save files
    dl_file = requests.get(download_link)
    open(filename,'wb').write(dl_file.content)    
    return filename

download_bgt_area("extract.zip", "POLYGON((155000 463000,155100 463000,155100 463100, 155000 463100, 155000 463000))")