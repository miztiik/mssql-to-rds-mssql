#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import logging
import os
import random
import string
import datetime
import time
import redis


class GlobalArgs:
    """ Global statics """
    OWNER = "Mystique"
    ENVIRONMENT = "production"
    MODULE_NAME = "insert_records_to_mysql"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
    LOG_FILE_NAME = "/var/log/miztiik-automation-redis-ingestor.log"
    DURATION = 3
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
    RECORD_COUNT = 200
    SRC_REDIS_HOST = "10.10.0.67"
    TGT_REDIS_HOST = "es.1uiafm.ng.0001.use1.cache.amazonaws.com"


def clear_redis(host, port):
    r = redis.StrictRedis(host, port, charset="utf-8", decode_responses=True)
    r.flushall
    logger.info(f'"host":{host},"db_wiped_clean":True')


def random_str_generator(size=40, chars=string.ascii_uppercase + string.digits):
    ''' Generate Random String for given string length '''
    return ''.join(random.choice(chars) for _ in range(size))


def ingest_to_redis(host, port):
    r = redis.StrictRedis(host, port, charset="utf-8", decode_responses=True)
    logger.info(f'{{"ingesting_to_host":"{host}"}}')
    print(f'{{"ingesting_to_host":"{host}"}}')
    # Load data into S3 & Redis
    i = 0
    while i < int(GlobalArgs.RECORD_COUNT):
        random_str = random_str_generator(random.randrange(200, 400))
        # r.set([KEY], [VALUE],[TTL])
        r.set(random.randint(1, 1000), random_str, int(time.time()) + 172800)
        i += 1
    print(
        f'{{"host":"{host}","total_records_ingested":{i},"data_ingest_completed":True}}')
    logger.info(
        f'{{"host":"{host}","total_records_ingested":{i},"data_ingest_completed":True}}')


def read_from_redis(host, port):
    print(f'{{"reading_from_host":"{host}"}}')
    logger.info(f'{{"reading_from_host":"{host}"}}')
    r = redis.StrictRedis(host, port, charset="utf-8", decode_responses=True)
    begin_time = datetime.datetime.now()
    new_time = begin_time
    i = 1
    while (new_time - begin_time).total_seconds() < GlobalArgs.DURATION:
        _resp = r.get(random.randint(1, 1000))
        # Count only if we found a key
        if _resp:
            i += 1
        new_time = datetime.datetime.now()
        if i % 10000 == 0:
            print(f'{{"records_retrieval_attempts":{i}}}')
    i -= 1
    print(f'{{"tot_of_records_retrieved":{i}}}')
    logging.info(f'{{"tot_of_records_retrieved":{i}}}')


logger = logging.getLogger()
logging.basicConfig(
    filename=f"{GlobalArgs.LOG_FILE_NAME}",
    filemode='a',
    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
    datefmt='%H:%M:%S',
    level=GlobalArgs.LOG_LEVEL
)

if not (GlobalArgs.SRC_REDIS_HOST or GlobalArgs.TGT_REDIS_HOST):
    logger.info(f"Check global args for SRC and TGT host. Should not be none")
    print(f"Check global args for SRC and TGT host. Should not be none")
    exit


ingest_to_redis(GlobalArgs.SRC_REDIS_HOST, GlobalArgs.REDIS_PORT)
read_from_redis(GlobalArgs.SRC_REDIS_HOST, GlobalArgs.REDIS_PORT)
read_from_redis(GlobalArgs.TGT_REDIS_HOST, GlobalArgs.REDIS_PORT)


# r = redis.StrictRedis(GlobalArgs.TGT_REDIS_HOST, GlobalArgs.REDIS_PORT, charset="utf-8", decode_responses=True)


# To delete ALL Redis KEYS
# clear_redis(GlobalArgs.TGT_REDIS_HOST, GlobalArgs.REDIS_PORT)
