import redis, time, json, datetime
import dateutil.parser
from threading import Thread
from sender import poll

REDIS_HOST = "localhost"
REDIS_PORT = "6379"
STATS_LEN = 1024


class Recorder:

    def __init__(self):
        self.ip = []
        self.client = None

    # adds a new machine to start watching
    def new_machine(self, new_ip, port):
        self.ip.append((new_ip, port))
        print self.ip

    # gets data from source and puts it in redis
    def post_to_redis(self, ip):
        print "post_to_redis " + str(ip)
        results = poll(ip[0], ip[1])
        print results
        for re in results["stats"]:
            container_id = re["name"]
            self.client.lpush(container_id, json.dumps(re))
            self.client.ltrim(container_id, 0, STATS_LEN - 1)

    # collects info for all IPs in self.ip
    def collect(self):
        while True:
            start_time = time.time()
            for ip in self.ip:
                Thread(target=self.post_to_redis, args=(ip,)).start()
            time.sleep(5.0 - time.time() + start_time)

    # Collects every 5 seconds, runs forever
    def run(self):
        self.client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
        while True:
            try:
                self.client.ping()
                break
            except redis.exceptions.ConnectionError:
                continue

        Thread(target=self.collect).start()
 
    # Retrieves data from redis, returns it
    def retrieve(self, container_id, delta):
        results = []
        now = datetime.datetime.now()
        dt = datetime.timedelta(seconds=int(delta))
        all_results = self.client.lrange(container_id, 0, -1)
        for r in all_results:
            parsed = json.loads(r)
            if now - dateutil.parser.parse(parsed["end"]) < dt:
                results.append(r)
        return json.dumps(results)
