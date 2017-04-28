import os
import time
import sys
import subprocess
import ipaddress

def senderCommand(ip):
    command = ("sudo docker run -d"
    "  -e 'COLLECTOR_URL=http://0.0.0.0:8787/cadvisor/metrics/'"
    "  -e 'CADVISOR_URL=http://" + ip + ":8080/api/v1.2'"
    " --restart on-failure:5 --net=host"
    " --name=sender" + ip + ""
    " hantaowang/sender:stable")
    os.system(command)

def collectorCommand(ip="0.0.0.0"):
    command = ("sudo docker run"
    "  -e 'COLLECTOR_REDIS_HOST=" + ip + "'"
    "  -e 'COLLECTOR_REDIS_PORT=6379'"
    "  -e 'COLLECTOR_PORT=8787'"
    "  --restart on-failure:5"
    "  --name=collector"
    "  -p 8787:8787 -d --name=collector"
    "  --net=host"
    "  hantaowang/collector:stable")
    os.system(command)

def getIP():
    ips = []
    disconnected = 0
    total = 0
    results = subprocess.check_output("quilt ps", shell=True).decode("utf-8")
    os.system('clear')
    print(results)
    results = results.split()
    for line in results:
        line = line.strip()
        if "disconnected" == line:
            disconnected += 1
        elif ("Worker" == line) or ("Master" == line):
            total += 1;
        try:
            ipaddress.ip_address(line)
            ips.append(line)
        except ValueError:
            next
    if (disconnected == 0 and total != 0):
        return ips
    return disconnected

ips = getIP()

while (isinstance(ips, int)):
    time.sleep(5)
    ips = getIP()

os.system("sudo docker kill $(docker ps -aq)")
os.system("sudo docker rm $(docker ps -aq)")
os.system("sudo redis-cli shutdown")
os.system("sudo docker run --name=redis -p 6379:6379 -d redis")
collectorCommand()
for ip in ips:
    senderCommand(ip)
