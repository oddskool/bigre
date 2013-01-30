#!/usr/bin/python

import logging
import sys, os
import boto
from boto.s3.key import Key

logging.getLogger('boto').setLevel(logging.INFO)
logging.getLogger().setLevel(logging.INFO)

bucket_name = 'odd-bigre'
conn = boto.connect_s3(*[ _.strip() for _ in open('deploy.keys').read().split('\n') ])
bucket = conn.get_bucket(bucket_name)

logging.info('removing old stuff...')
for key in bucket.list(prefix="/"):
    logging.info('DEL %s',key.key)
    key.delete()

logging.info('pushing new files...')
for (dirpath, dirnames, filenames) in os.walk("output"):
    for fn in filenames:
        path = os.path.join(dirpath, fn)
        k = Key(bucket)
        k.key = path.replace('output/','')
        k.set_contents_from_filename(path)
        k.make_public()
        logging.info('PUT %s',k.key)

logging.info('done')
