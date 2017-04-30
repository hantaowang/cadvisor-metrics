import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import redis
from datetime import datetime
import json
import os
import sys
HOST=os.getenv('REDIS_HOST', '127.0.0.1')
PORT=int(os.getenv('REDIS_PORT', '6379'))
LIMIT=int(os.getenv('LIMIT', '20'))


name = sys.argv[1]
stat = sys.argv[2]

style.use("ggplot")
r = redis.StrictRedis(host=HOST, port=PORT)

def append(arr, item):
    if len(arr) >= LIMIT:
        arr.pop(0)
    arr.append(item)

def updateEach(name, jsn):
    if len(name["timestamp"]) > 0 and jsn["ts"] == name["timestamp"][-1].strftime("%X"):
        return
    append(name["cpu_load"], jsn["cpu"]["load"]["ave"])
    append(name["cpu_usage"], jsn["cpu"]["usage"])
    append(name["network_rx"], jsn["network"]["rx_kb"])
    append(name["network_tx"], jsn["network"]["tx_kb"])
    append(name["memory"], jsn["memory"]["ave"])
    append(name["disk_read"], jsn["diskio"]["read"])
    append(name["disk_write"], jsn["diskio"]["write"])
    print jsn["ts"]
    append(name["timestamp"], datetime.strptime(jsn["ts"], "%X"))

stat_names = {"timestamp": "Time", "cpu_load": "CPU Load", "cpu_usage": "CPU Usage", "network_rx": "RX Bytes", "network_tx": "TX Bytes", "memory": "Memory Usage", "disk_read": "Read KB", "disk_write": "Write KB"}
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
entries = {}
for sn in stat_names.keys():
    entries[sn] = []
last20 = r.lrange(name, 0, 19)
# for e in last20:
#     updateEach(entries, json.loads(e))

def animate(i):
    updateEach(entries, json.loads(r.lindex(name, 0)))
    ax.clear()
    ax.set_title(name)
    ax.set_xlabel("Time")
    ax.set_ylabel(stat_names[stat])
    ax.plot(entries["timestamp"], entries[stat], color='r')

ani = animation.FuncAnimation(fig, animate, interval=1000)

plt.show()
