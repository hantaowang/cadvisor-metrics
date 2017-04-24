import os
import time
print("##### INSTALLING REDIS SERVER #####")
os.system("sudo apt-get -y install redis-server")
print("##### INSTALLING PYTHON PIP #####")
os.system("sudo apt-get -y install python-pip")
print("##### INSTALLING PIP FALCON #####")
os.system("sudo pip install falcon")
print("##### INSTALLING PIP GUNICORN #####")
os.system("sudo pip install gunicorn")
print("##### INSTALLING PIP REDIS #####")
os.system("sudo pip install redis")
print("##### INSTALLING PIP REQUESTS #####")
os.system("sudo pip install requests")
print("##### INSTALLING PIP DATEUTIL #####")
os.system("sudo pip install python-dateutil")
print("##### SETTING ENVIRONMENT VARIABLES #####")
os.system("export COLLECTOR_REDIS_HOST=127.0.0.1")
os.system("export COLLECTOR_URL=http://0.0.0.0:8787/cadvisor/metrics/")
os.system("export CADVISOR_URL=http://0.0.0.0:8080/api/v1.2")
print("##### RUNNING COLLECTOR #####")
os.system("python ./cadvisor-metrics/collector/collector.py &")
time.sleep(5)
print("##### RUNNING SCRIPT #####")
while True:
    os.system("python ./cadvisor-metrics/sender/sender.py")
    print("[", strftime("%Y-%m-%d %H:%M:%S", gmtime()), "]", "Ran Sender")
    time.sleep(60)
