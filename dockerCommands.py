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
        stopContainer("redis")
        stopContainer("cmetrics")

    # Starts the docker cmetrics container
    @staticmethod
    def cmetrics(ips=["0.0.0.0"]):
        ip_string = ""
        for ip in ips:
            ip_string += ip + ","
        command = ("sudo docker run"
            "  -e 'CADVISOR_IPS=" + ip_string[:-1] + "'"
            "  --restart on-failure:5"
            "  --name=cmetrics"
            "  -d --net=host"
            "  hantaowang/cmetrics")
        os.system(command)

    # Starts the docker redis container
    @staticmethod
    def redis():
        os.system("sudo redis-cli shutdown")
        os.system("sudo docker run --name=redis -p 6379:6379 -d redis")
