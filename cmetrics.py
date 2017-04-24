import os
import time
os.system("sudo apt-get -y install redis-server")
os.system("sudo apt-get -y install python-pip")
os.system("sudo pip install falcon")
os.system("sudo pip install gunicorn")
os.system("sudo pip install redis")
os.system("sudo pip install requests")
os.system("sudo pip install python-dateutil")
os.system("export COLLECTOR_REDIS_HOST=127.0.0.1")
os.system("export COLLECTOR_URL=http://0.0.0.0:8787/cadvisor/metrics/")
os.system("export CADVISOR_URL=http://0.0.0.0:8080/api/v1.2")
os.system("python3 ./collector/collector.py")
while True:
    print(os.system("python3 ./sender/sender.py")
    time.sleep(60)
