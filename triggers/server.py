from flask import Flask, request
from recorder import Recorder

app = Flask(__name__)
rec = Recorder()


@app.route('/ping')
def ping():
    return 'pong'


@app.route('/newmachine')
def newmachine():
    ip = request.form.get('machineip', None)
    port = request.form.get('machineport', None)
    if ip is not None and port is not None:
        rec.new_machine(ip.strip(), port.strip())
        return 'success'
    return 'failure'


@app.route('/getdatapoints')
def newmachine():
    container_id = request.form.get('containerid', None)
    period = request.form.get('period', "30")
    if container_id is not None:
        return rec.retrieve(container_id.strip(), period.strip())
    return "{}"

if __name__ == '__main__':
    rec.run()
    app.run()
