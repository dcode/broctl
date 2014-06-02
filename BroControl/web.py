from BroControl import version
from BroControl.broctld import Client
from BroControl.ser import dumps
import os
import bottle
import json

app = bottle.Bottle(autojson=False)
app.install(bottle.JSONPlugin(json_dumps=lambda s: json.dumps(s, default=dumps)))

@app.route('/start')
def start():
    i = app.daemon.call("start")
    return {"id": i} 

@app.route('/stop')
def start():
    i = app.daemon.call("stop")
    return {"id": i} 

@app.route('/restart')
def restart():
    i = app.daemon.call("restart")
    return {"id": i} 


@app.route('/nodes')
def nodes():
    s = app.daemon.sync_call("nodes")
    return {"result": s}

@app.route('/exec/:cmd')
def start(cmd):
    i = app.daemon.call("execute", cmd)
    return {"id": i} 

@app.route('/result/:id')
def result(id):
    id = int(id)
    return {"result": app.daemon.getresult(id)}

@app.route('/log/:id')
@app.route('/log/:id/:since')
def result(id, since=0):
    id = int(id)
    since = int(since)
    return {"log": app.daemon.getlog(id, since) or []}

@app.route('/:cmd')
def cmd(cmd):
    i = app.daemon.call(cmd)
    return {"id": i} 

def main():
    sockfile = os.path.join(version.BROBASE, "socket")
    app.daemon = Client('ipc://%s' % sockfile)
    bottle.run(app, host='localhost', port=8082)

if __name__ == "__main__":
    main()
