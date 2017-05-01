# cAdvisor Metrics

This repo is a fork of the cadvisor-metrics (cmetrics) tool published by Catalyze. You can read the original full length ReadMe in their [repo](https://github.com/catalyzeio/cadvisor-metrics). The topics here focus on the changes made on this fork.

### Overview
The purpose of this fork is to integrate cAdvisor with [Quilt](https://github.com/quilt/) in order to monitor and analyze cpu, memory, disk, and network data across a distributed system. It is intended as a dependency for the [ThrottleBot](https://github.com/mchang6137/throttlebot), which aims to find resource bottlenecks in a distributed containerized application.

### Changes
cmetrics.py acts as the main tool to automate the setup and take down of cMetrics. It parses Quilt output and sets up cmetrics to conncet to the appropriate cAdvisor instances. The original sender.py file was used as a base for the new collection system. The server in collector.py has been removed, and it instead calls the poll function in sender. This is better suited for the purposes of quilt. Changes were also made to provide better integration with Redis and bug fixes were made to sender.py, fixing some of the outstanding bugs noted in the original docs.

### Running
After booting up quilt by using `quilt run`, simply run `python cmetrics.py start` to boot up cmetrics. One cmetrics is booted up, there is a jupyter notebook that can visualize live data results. Make sure you have jupyter installed and run `jupyter notebook`. In the browser, open up visualizer.ipnyb to see the plots.
Close down cmetrics by running `python cmetrics.py stop`
