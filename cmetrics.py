import os
import time
os.system("sudo apt-get install redis-server")
os.system("sudo apt-get install python-pip")
os.system("sudo apt-get install python-pip")
os.system("sudo pip install falcon")
os.system("sudo pip install redis")
os.system("sudo pip install requests")
os.systems("sudo pip install python-dateutil")
os.sysetm("export COLLECTOR_REDIS_HOST=127.0.0.1")
os.sysetm("export COLLECTOR_URL=http://0.0.0.0:8787/cadvisor/metrics/")
os.system("export CADVISOR_URL=http://0.0.0.0:8080/api/v1.2")
os.system("python ./collector/collector.py")
while True:
    os.system("python ./sender/sender.py")
    time.sleep(60)
