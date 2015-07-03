# -*- coding: utf-8 -*-
"""
download file using requests

Created on Fri Jul  3 09:13:04 2015

@author: poldrack
"""
import requests
import os

# from http://stackoverflow.com/questions/16694907/how-to-download-large-file-in-python-with-requests-py
def DownloadFile(url,local_filename):
    if not os.path.exists(os.path.dirname(local_filename)):
        os.makedirs(os.path.dirname(local_filename))
    r = requests.get(url)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
    return 
