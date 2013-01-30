#!/usr/bin/python

import logging
import sys, os
import boto
from boto.s3.key import Key

logging.getLogger('boto').setLevel(logging.DEBUG)
bucket_name = 'odd-bigre'
conn = boto.connect_s3(*[ _.strip() for _ in open('deploy.keys').read().split('\n') ])
bucket = conn.get_bucket(bucket_name)

for (dirpath, dirnames, filenames) in os.walk(sys.argv[1]):
    for fn in filenames:
        path = os.path.join(dirpath, fn)
        print path
        k = Key(bucket)
        k.key = path
        k.set_contents_from_filename(path)
        k.make_public()
