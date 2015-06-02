"""
send status log to s3
"""


import boto
from uuid import getnode as get_mac
import time
import platform
from boto.s3.connection import S3Connection

def send_log(type=None):
    assert type in ['start','finish','crash']
    
    ts = time.time()
    
    bucket_name = 'myconnectome-log'
    
    conn = S3Connection(anon=True)
    bucket = conn.get_bucket(bucket_name)
    
    mac = get_mac()
    
    k = bucket.new_key('%s:%d:%d'%(type,mac,ts))
    k.set_contents_from_string(' '.join(platform.uname()))
    
