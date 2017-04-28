import os
import subprocess
import threading
import time

ipList = os.getenv('CADVISOR_IPS', '0.0.0.0').strip().split()

time.sleep(60)

print("Starting senders")
print(ipList)

# for ip in ipList:
#     print("Running sender for " + ip)
#     os.system("python sender.py " + ip)

while True:
    t1 = time.clock()
    for ip in ipList:
        t1 = time.clock()
        print("Running sender for " + ip)
        os.system("python sender.py " + ip)
    time.sleep(60 - time.clock() + t1)
