"""
send status log to s3
"""


import boto
from uuid import getnode as get_mac
import time
import platform

def send_log(type=None):
    assert type in ['start','finish','crash']
    
    ts = time.time()
    
    AWS_ACCESS_KEY_ID = None
    AWS_SECRET_ACCESS_KEY =None
    bucket_name = 'myconnectome-log'
    
    conn = boto.connect_s3(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
    bucket = conn.get_bucket(bucket_name)
    
    mac = get_mac()
    
    k = bucket.new_key('%s:%d:%d'%(type,mac,ts))
    k.set_contents_from_string(' '.join(platform.uname()))
    
