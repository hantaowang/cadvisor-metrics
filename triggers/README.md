### How to use
1) Make sure you have redis running. Default at `localhost:12345`, but this can be changed.
2) Run `python server.py` which servers at `localhost:5000`.
3) Start cAdvisor on the machines you want to track.
4) For each machine, get that machine's ip. Then visit `localhost:5000/newmachine?machineip=<machine_ip>&machineport=8000`.
5) Now cmetrics is tracking that machine. For stats on a container, visit `localhost:5000/getdatapoints?containerid=<container_id>&period=<time_in_secs>`
6) That returns a json with the last `<time_in_secs>`/5 in 5 second intervals data points for `<container_id>`.