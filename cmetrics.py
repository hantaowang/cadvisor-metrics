import os
import time
print(os.system("sudo apt-get install redis-server")))
print(os.system("sudo apt-get install python-pip"))
print(os.system("sudo pip install falcon"))
print(os.system("sudo pip install gunicorn"))
print(os.system("sudo pip install redis"))
print(os.system("sudo pip install requests"))
print(os.system("sudo pip install python-dateutil"))
print(os.sysetm("export COLLECTOR_REDIS_HOST=127.0.0.1"))
print(os.sysetm("export COLLECTOR_URL=http://0.0.0.0:8787/cadvisor/metrics/"))
print(os.system("export CADVISOR_URL=http://0.0.0.0:8080/api/v1.2"))
print(os.system("python3 ./collector/collector.py"))
while True:
    print(os.system("python3 ./sender/sender.py"))
    time.sleep(60)
