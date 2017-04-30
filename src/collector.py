import redis
import time
from datetime import datetime
import json
from threading import Thread
from sender import poll
import os

REDIS_HOST=os.getenv('COLLECTOR_REDIS_HOST', '127.0.0.1')
REDIS_PORT=int(os.getenv('COLLECTOR_REDIS_PORT', '6379'))
STATS_LEN=int(os.getenv('STATS_LEN', '1440'))
IP_LIST = os.getenv('CADVISOR_IPS', '0.0.0.0').strip().split(",")
IP_LIST = ["54.193.79.14", "52.53.231.12", "54.219.176.151"]
r = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
lastTime = 0
def postToRedis(ip):
    results = poll(ip)
    print(datetime.now().strftime('%H:%M:%S.%f') + " polled " + ip)
    for re in results["stats"]:
        r.sadd("names", re["name"])
        r.lpush(re["name"], json.dumps(re))
        r.ltrim(re["name"], 0, STATS_LEN - 1)


def collect():
    for ip in IP_LIST:
        Thread(target = postToRedis, args=(ip,)).start()


while True:
    starttime = time.time()
    collect()
    time.sleep(5.0 - ((time.time() - starttime)))
