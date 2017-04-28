import os
import time
import sys
import subprocess
import socket
from dockerCommands import Commands

# Parses the command arguments
if len(sys.argv) == 1:
    command = None
else:
    command = sys.argv[1]
if command == "stop":
    Commands.stopAllContainers()
    sys.exit()
if command != None and command != "start":
    print command + "is not a valid commnad"
if command != "start":
    print ("Here is a list of valid commands\n"
    "  start    sets up and starts the cMetrics docker container\n"
    "  stop     stops and removes the cMetrics docker containers")
    sys.exit()
Commands.stopAllContainers()

# Parses the "quilt ps" output to retrieve all machine IPs.
# Only returns IPs if all machines are connected
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
            socket.inet_aton(line)
            ips.append(line)
        except socket.error:
            next
    if (disconnected == 0 and total != 0):
        return ips
    return disconnected

# Waits until all machines are conncted and then parses IPs
ips = getIP()
while (isinstance(ips, int)):
    time.sleep(5)
    ips = getIP()

# Sets up a docker containers
Commands.redis()
Commands.collector()
Commands.sender(ips)
