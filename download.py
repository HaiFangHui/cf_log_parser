#!/usr/bin/env python

from datetime import datetime
import logging
from boto.s3.connection import S3Connection
import zlib
from models import parse_log_data, LogFile, session, Base, engine
from config import config
from datetime import timedelta


def parse_all_files_for_day(distribution_id, date, bucket):
    prefix = "%s.%s" % (distribution_id, date.strftime("%Y-%m-%d"),)
    for k in bucket.list(prefix=prefix):
        if session.query(LogFile).filter(LogFile.filename==k.name).count() > 0:
            pass
        else:
            logging.debug("Processing: %s" % (str(k),))
            log_file = LogFile()
            log_file.filename = k.name
            session.add(log_file)
            content = zlib.decompress(k.get_contents_as_string(), 16+zlib.MAX_WBITS)
            parse_log_data(content)
            session.commit()


if __name__ == '__main__':
    s3conn = S3Connection(
        config.get('AWS', 'AWS_ACCESS_KEY_ID'),
        config.get('AWS', 'AWS_SECRET_ACCESS_KEY')
    )
    bucket = s3conn.get_bucket(config.get('CF_LOG', 'S3BUCKET'), validate=False)

    Base.metadata.create_all(engine)

    day = datetime.now()
    for d in xrange(0, config.getint('CF_LOG', 'BACKFILL_DAYS')):
        day = day - timedelta(days=1)
        parse_all_files_for_day(config.get('CF_LOG', 'DISTRIBUTION_ID'),
                                day, bucket)

    
