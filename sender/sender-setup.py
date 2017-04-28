import sys
import os
import threading

cadvisor_base = os.getenv('CADVISOR_IPS', '0.0.0.0').split(" ")
ipList = list(map(lambda x: x.strip(), cadvisor_base))

print("Starting senders")
print(ipList)

def runSenders():
    threading.Timer(60, runSenders).start()
    for ip in ipList:
        try:
            print("running sender for " + ip)
            os.spawnl(os.P_DETACH, "python sender.py " + ip)
            print("ran sender for " + ip)
        except Error as err:
            print err
            next

# start calling f now and every 60 sec thereafter
runSenders()
