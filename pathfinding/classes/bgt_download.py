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
        "onbegroeidterreindeel",
        "begroeidterreindeel"
    ],
    "format": "citygml",
    "geofilter": area
    }
    
    # Request data
    response = requests.post(url, headers=head, json=data)
    response_load = json.loads(response.text)
    
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

def download_bgt_from_rdc(filename: str, start: tuple[int, int], end: tuple[int, int]) :
    # The proportion of extra distance we download around the points
    extra_area = 0.1

    # The distance between the points
    horizontal_dist = abs(start[0]-end[0])
    vertical_dist = abs(start[1]-end[1])

    # The corners of the area we want to download
    left = int(min(start[0], end[0])-horizontal_dist*extra_area)
    right = int(max(start[0], end[0]) + horizontal_dist*extra_area)
    up = int(max (start[1], end[1]) + vertical_dist*extra_area)
    down = int(min(start[1], end[1]) - vertical_dist*extra_area)

    area = "POLYGON((" + str(left) + " " + str(down) + "," + str(left) + " " + str(up) + "," + str(right) + " " + str(up) + "," + str(right) + " " + str(down) + "," + str(left) + " " + str(down) + "))"
    return(download_bgt_area(filename, area))