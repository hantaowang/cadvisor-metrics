import redis
import time
from datetime import datetime
import json
from threading import Thread
from sender import poll
import os

# Sets up environemnt variables
REDIS_HOST=os.getenv('COLLECTOR_REDIS_HOST', '127.0.0.1')
REDIS_PORT=int(os.getenv('COLLECTOR_REDIS_PORT', '6379'))
STATS_LEN=int(os.getenv('STATS_LEN', '1440'))
IP_LIST = os.getenv('CADVISOR_IPS', '0.0.0.0').strip().split(",")

# Sets up redis interface
r = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)

# Retrieves data from IP and posts to redis server
def postToRedis(ip):
    results = poll(ip.strip())
    print("polled " + ip + " for data from " + results["stats"][0]["ts2"] + " to " + results["stats"][0]["ts"])
    for re in results["stats"]:
        r.sadd("names", re["name"])
        r.lpush(re["name"], json.dumps(re))
        r.ltrim(re["name"], 0, STATS_LEN - 1)

# Posts to redis for all IPS in IP_LIST using multithreading
def collect():
    for ip in IP_LIST:
        Thread(target = postToRedis, args=(ip,)).start()

# Collects data every 5 seconds 
while True:
    starttime = time.time()
    collect()
    time.sleep(5.0 - ((time.time() - starttime)))
