# -*- coding: utf-8 -*-
"""
download file using requests

Created on Fri Jul  3 09:13:04 2015

@author: poldrack
"""
import requests
import os
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from requests import Session, exceptions

# from http://stackoverflow.com/questions/16694907/how-to-download-large-file-in-python-with-requests-py
def DownloadFile(url,local_filename):
    if not os.path.exists(os.path.dirname(local_filename)):
        os.makedirs(os.path.dirname(local_filename))
    s=requests.Session()
    s.mount('http://',HTTPAdapter(max_retries=Retry(total=10,status_forcelist=[500])))
    
    connect_timeout = 10.0

    r = s.get(url=url,timeout=(connect_timeout, 10.0))
    #except requests.exceptions.ConnectTimeout:
    #    print "Too slow Mojo!"
        
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
    return 
