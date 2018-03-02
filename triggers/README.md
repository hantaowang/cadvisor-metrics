### How to use
1) Make sure you have redis running. Default at `localhost:12345`, but this can be changed.
2) Run `python server.py` which servers at `localhost:5000`.
3) Start cAdvisor on the machines you want to track.
4) For each machine, get that machine's ip. Then visit `localhost:5000/newmachine?machineip=<machine_ip>&machineport=8000`.
5) Now cmetrics is tracking that machine. For stats on a container, visit `localhost:5000/getdatapoints?containerid=<container_id>&period=<time_in_secs>`
6) That returns a json with the last `<time_in_secs>`/5 in 5 second intervals data points for `<container_id>`.

The return value will be an json string that is a array of nested dictionaries. It will look like:

`[{Data point 1}, {Data point 2}, ...]`

Each data point will look like:

    {
        name: <container id>,
        start: <start of interval in seconds since epoch>,
        end: <end of interval in seconds since epoch>,
        cpu: {
            usage: float,
            load: {
                ave: float,
                min: float,
                max: float,
            }
        },
        memory: {
            ave: float,
            min: float,
            max: float,
        },
        network: {
            tx_kb: float,
            rx_kb: float,
            tx_packets: int,
            rx_packets: int,
            tx_errors: float,
            rx_errors: float,
            tx_drops: int,
            rx_drops: int,
        },
        diskio: {
            async: float,
            sync: float,
            read: float,
            write: float,
        }
    }
   
I am actually unsure of / forgot the units of diskio (b or kb), memory (b or kb), and cpu (???).
Will update later when I find out.


### How to Deploy

Have your Kubernetes cluster up and running. In `cadvisor-metrics/triggers/deployment` run

```
kubectl create -f cmetrics.yaml
```

To obtain the URL of the python server, run

```
kubectl describe services cmetrics-server
```
The url is under LoadBalancer Ingress. Access the server through port 5000.