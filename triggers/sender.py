"""
This script is to be called by collector.py. It parses the
last 5 stats for each container.

Usage:

    results = poll(0.0.0.0)

"""
from datetime import datetime
import requests
import dateutil.parser

blacklist = ["ovs-vswitchd", "minion", "ovn-controller", "cadvisor", "ovsdb-server"]
interval = 5 # Number of seconds of data that we are getting back from cadvisor per container

def total_min_max(stat, s_total, s_min, s_max):
    """
    Given a value (stat), add it to the total and check if it is the new
    min value or max value compared to s_min and s_max.
    """
    result_min = s_min
    result_max = s_max
    s_total += stat
    if s_min == None or stat < s_min:
        result_min = stat
    if s_max == None or stat > s_max:
        result_max = stat
    return s_total, result_min, result_max

def process_diskio(diskio, field):
    """
    Sum up all the disk IO bytes for a given field (Sync, Async, Read, Write).

    Only considering io_service_bytes stats right now (io_serviced is ignored).
    """

    total = 0
    try:
        io_stats = diskio['io_service_bytes']
    except KeyError:
        io_stats = {}
    for entry in io_stats:
        total += entry['stats'][field]

    return total


def getStats(ip, port):
    cadvisor_url = "http://" + ip + ":" + port + "/api/v1.2/docker"
    # Connect to cadvisor and get the 5 last stats
    r = requests.get(cadvisor_url)
    entries = []
    for key, value in r.json().items():
        print key
        # Determine if one of the aliases matches (is something we want to collect metrics for)
        if value['aliases'][0] in blacklist:
            container_name = "ERROR " + value['aliases'][0]
            continue
        else:
            container_name = "docker://" + value['id']

        # Compute the timestamp, using the first second in this series
        # Run through all the stat entries for this container
        stats = value['stats'][-5:]
        ts = dateutil.parser.parse(stats[0]['timestamp']).ctime()
        ts2 = dateutil.parser.parse(stats[-1]['timestamp']).ctime()
        stats_len = 5

        # Initialize min/max/total variables for memory, cpu
        total_memory = 0
        min_memory = None
        max_memory = None
        total_load = 0
        min_load = None
        max_load = None
        records = 0

        # Compute min, max and average for all non-cumulative stats
        for stat in stats:
            records += 1

            # Grab the memory usage stats
            memory = stat['memory']
            memory_kb = memory['usage']/1024.0
            total_memory, min_memory, max_memory = total_min_max(memory_kb, total_memory, min_memory, max_memory)

            # Get the CPU load. The load value is always 0?
            cpu = stat['cpu']['usage']
            cpu_load = cpu['total']
            total_load, min_load, max_load = total_min_max(cpu_load, total_load, min_load, max_load)

        # Initialize the entry for this container
        entry = {'name': container_name, 'start' : ts, 'end' : ts2}
        entry['cpu'] = {}
        entry['memory'] = {}
        entry['network'] = {}
        entry['diskio'] = {}

        # Compute first/last values of cumulative counters
        first = stats[0] # First item in this series
        last = stats[stats_len - 1] # Last item in this series

        # Compute CPU usage delta
        start_cpu_usage = first['cpu']['usage']['total']
        end_cpu_usage = last['cpu']['usage']['total']

        # Network stats deltas
        start_tx_bytes = first['network']['tx_bytes']
        end_tx_bytes = last['network']['tx_bytes']
        start_rx_bytes = first['network']['rx_bytes']
        end_rx_bytes = last['network']['rx_bytes']
        start_tx_packets = first['network']['tx_packets']
        end_tx_packets = last['network']['tx_packets']
        start_rx_packets = first['network']['rx_packets']
        end_rx_packets = last['network']['rx_packets']
        start_tx_errors = first['network']['tx_errors']
        end_tx_errors = last['network']['tx_errors']
        start_rx_errors = first['network']['rx_errors']
        end_rx_errors = last['network']['rx_errors']
        start_tx_drops = first['network']['tx_dropped']
        end_tx_drops = last['network']['tx_dropped']
        start_rx_drops = first['network']['rx_dropped']
        end_rx_drops = last['network']['rx_dropped']

        # Compute Disk IO deltas
        start_async_bytes = process_diskio(first['diskio'], 'Async')
        end_async_bytes = process_diskio(last['diskio'], 'Async')
        start_sync_bytes = process_diskio(first['diskio'], 'Sync')
        end_sync_bytes = process_diskio(last['diskio'], 'Sync')
        start_read_bytes = process_diskio(first['diskio'], 'Read')
        end_read_bytes = process_diskio(last['diskio'], 'Read')
        start_write_bytes = process_diskio(first['diskio'], 'Write')
        end_write_bytes = process_diskio(last['diskio'], 'Write')

        # Add CPU stats
        entry['cpu']['usage'] = end_cpu_usage - start_cpu_usage
        entry['cpu']['load'] = {}
        entry['cpu']['load']['ave'] = total_load/stats_len
        entry['cpu']['load']['min'] = min_load
        entry['cpu']['load']['max'] = max_load

        # Add memory stats
        entry['memory']['ave'] = total_memory/stats_len
        entry['memory']['min'] = min_memory
        entry['memory']['max'] = max_memory

        # Add network stats
        entry['network']['tx_kb'] = (end_tx_bytes - start_tx_bytes)/1024.0
        entry['network']['rx_kb'] = (end_rx_bytes - start_rx_bytes)/1024.0
        entry['network']['tx_packets'] = end_tx_packets - start_tx_packets
        entry['network']['rx_packets'] = end_rx_packets - start_rx_packets
        entry['network']['tx_errors'] = end_tx_errors - start_tx_errors
        entry['network']['rx_errors'] = end_rx_errors - start_rx_errors
        entry['network']['tx_drops'] = end_tx_drops - start_tx_drops
        entry['network']['rx_drops'] = end_rx_drops - start_rx_drops

        # Add disk IO stats
        # These stats are currently aggregated across all volumes. May not be desirable.
        entry['diskio']['async'] = end_async_bytes - start_async_bytes
        entry['diskio']['sync'] = end_sync_bytes - start_sync_bytes
        entry['diskio']['read'] = end_read_bytes - start_read_bytes
        entry['diskio']['write'] = end_write_bytes - start_write_bytes
        # Note that io_serviced stats are not being included here. Easy to add if needed.
        entries.append(entry)

    return entries

def poll(ip, port="8000"):
    # Create the final result to send to the collector
    stats_result = {}
    stats_result['timestamp'] = datetime.now().strftime("%X") # Epoch time for when this entry was computed (in seconds)
    stats_result['stats'] = getStats(ip, port)
    stats_result['interval'] = interval # The duration of this stat entry in seconds
    stats_result[ip] = ip
    return stats_result
