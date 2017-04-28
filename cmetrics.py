import os
import time
import sys
import subprocess
import re
from dockerCommands import Commands

commands = ["start", "stop", "kill-all"]

# Parses the command arguments
if len(sys.argv) == 1 or sys.argv[1] not in commands:
    if len(sys.argv) > 1:
        print str(sys.argv[1]) + " is not a valid command"
    print ("Here is a list of all valid commands\n"
    "  start      sets up and starts the cMetrics docker container\n"
    "  stop       stops and removes the cMetrics docker containers\n"
    "  kill-all   kills all running docker containers")
    sys.exit()

Commands.stopAllContainers(sys.argv[1] == "kill-all")
if sys.argv[1] != "start":
    sys.exit()


# Parses the "quilt ps" output to retrieve all machine IPs.
# Only returns IPs if all machines are connected
def getValues():
    values = {}
    ips = {}
    results = subprocess.check_output("quilt ps", shell=True).decode("utf-8")
    os.system('clear')
    print(results)
    results = results.split("\n")
    fourthItem = ["SIZE", "Worker", "Master", "STATUS"]
    for line in results:
        items = line.split()
        if "disconnected" in line:
            return -1
        elif "Worker" in line:
            getIP(line, ips)
        elif "LABELS" in line:
            labelIndex = line.index("LABEL")
            statusIndex = line.index("STATUS")
        elif "running" in line:
            getNames(line, values, ips, labelIndex, statusIndex)
        elif len(items) > 0 and items[1] not in fourthItem and items[4] not in fourthItem:
            print items
            return -1
    return (ips, values)

# Parses a line to retrieve the IP and its matching machine ID
def getIP(line, ips):
    line = line.split()
    ips[line[0]] = line[5].encode("utf-8")

# Parses a line to retrieve the IP and its matching containers. Currently unused.
def getNames(line, values, ips, a, b):
    name = line[a:b].strip()
    line = line.split()
    if ips[line[1]] not in values:
        values[ips[line[1]]] = []
    values[ips[line[1]]].append((line[0], name + "@" + ips[line[1]]))

# Waits until all machines are conncted and then parses IPs
values = getValues()
while (isinstance(values, int)):
    time.sleep(5)
    values = getValues()
ips = values[0].values()
names = values[1]
print "Found these IPs beloning to worker machines: " + str(ips)
#print names

# Sets up a docker containers
Commands.redis()
Commands.collector()
Commands.sender(ips)
