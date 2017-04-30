import os
import subprocess

def stopContainer(name):
    if len(subprocess.check_output("docker ps -aq -f status=running -f name=" + name, shell=True).decode("utf-8")) > 0:
        os.system("docker stop " + name)
    if len(subprocess.check_output("docker ps -aq -f name=" + name, shell=True).decode("utf-8")) > 0:
        os.system("docker rm " + name)

class Commands:

    # Stops and removes the containers if it is running
    @staticmethod
    def stopAllContainers(all=False):
        if all:
            if len(subprocess.check_output("docker ps -aq -f status=running", shell=True).decode("utf-8")) > 0:
                os.system("sudo docker kill $(docker ps -aq -f status=running)")
            if len(subprocess.check_output("docker ps -aq", shell=True).decode("utf-8")) > 0:
                os.system("sudo docker rm $(docker ps -aq)")
            return
        stopContainer("cmetrics-redis")
        stopContainer("cmetrics-sender")
        stopContainer("cmetrics-collector")

    # Starts the docker collector container
    @staticmethod
    def collector(ip="0.0.0.0"):
        command = ("sudo docker run"
            "  -e 'COLLECTOR_REDIS_HOST=" + ip + "'"
            "  -e 'COLLECTOR_REDIS_PORT=6379'"
            "  -e 'COLLECTOR_PORT=8787'"
            "  --restart on-failure:5"
            "  --name=cmetrics-collector"
            "  -p 8787:8787 -d"
            "  --net=host"
            "  hantaowang/collector:stable")
        os.system(command)

    # Starts the docker sender container
    @staticmethod
    def sender(ips):
        ipString = ""
        for ip in ips:
            ipString += ip + " "
        command = ("sudo docker run -d"
        " -e 'CADVISOR_IPS=" + ipString + "'"
        " --restart on-failure:5 --net=host"
        " --name=cmetrics-sender"
        " hantaowang/sender:latest")
        os.system(command)

    # Starts the docker redis container
    @staticmethod
    def redis():
        try:
            if subprocess.check_output("sudo redis-cli ping", shell=True,stderr=subprocess.STDOUT).decode("utf-8") == "PONG":
                os.system("sudo redis-cli shutdown")
        except subprocess.CalledProcessError:
            next
        os.system("sudo docker run --name=cmetrics-redis -p 6379:6379 -d redis")
