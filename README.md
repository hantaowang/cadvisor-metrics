# cAdvisor Metrics

This repo is a fork of the cadvisor-metrics (cmetrics) tool published by Catalyze. You can read the origina full length ReadMe in their [repo](https://github.com/catalyzeio/cadvisor-metrics). The topics here focus on the changes made on this fork.

### Overview
The purpose of this fork is to integrate cAdvisor with [Quilt](https://github.com/quilt/) in order to monitor and analyze cpu, memory, disk, and network data across a distributed system. It is intended as a dependency for the [ThrottleBot](https://github.com/mchang6137/throttlebot), which aims to find resource bottlenecks in a distributed containerized application.

### Changes
cmetrics.py acts as the main tool to automate the setup and take down of cMetrics. It parses Quilt output and sets up cmetrics to conncet to the appropriate cAdvisor instances. To begin, simply run `python cmetrics.py start.` Run `python cmetrics.py` to see a full list of commands and what each does. 

Changes were made to the the sender and collector docker images to provide better integration with Quilt and Redis. There were also some bug fixes to sender.py.  
