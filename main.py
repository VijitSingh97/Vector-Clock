from re import T
from flask import Flask, jsonify, request
from logging import ERROR, getLogger
from random import randint
from requests import post
from sys import argv
from threading import Lock, Thread, Timer
from time import sleep

# creating a Flask app
app = Flask(__name__)
  
# on the terminal type: curl http://localhost:808x/
# returns the success when we send valid update counter message
# example body:
#   body = {
#       "counter": [1, 1, 3]
#   }
@app.route('/', methods = ['POST'])
def home():
    if(request.method == 'POST'):
        receive_message(request.json)
        return jsonify({'result': 'success'})

# method that handles incoming message 
def receive_message(request):
    lock.acquire()
    try:
        print(f"[{name}] counter before receiving: {counter}" )
        counter[server_number] += 1
        for x in range(len(counter)):
            if request["counter"][x] > counter[x]:
                counter[x] = request["counter"][x]
        print(f"[{name}] counter after receiving: {counter}")
    finally:
        lock.release()

# method that sends message to other servers in network
def send_message(server_port):
    lock.acquire()
    try:
        try:
            if (server_port != port):
                print(f"[{name}] counter before send: {counter}")
                url = 'http://localhost:' + str(server_port)
                body = {
                    "counter": counter
                }
                post(url, json=body)
                counter[server_number] += 1
                print(f"[{name}] counter after send: {counter}")
        except:
            pass
    finally:
        lock.release()

# method that performs arbitrary event 
def do_event():
    lock.acquire()
    try:
        print(f"[{name}] counter before event: {counter}")
        sleep(randint(1,10))
        counter[server_number] += 1
        print(f"[{name}] counter after event: {counter}")
    finally:
        lock.release()

def generate_name_port():
    port = 8080 + server_number
    name = "server_" + str(port)
    return name, port

def run_events_interval():
    Timer(randint(1,60), run_events_interval).start()
    do_event()

def run_sends_randomly():
    Timer(randint(1,60), run_sends_randomly).start()
    send_message(8080 + randint(0,2))

if __name__ == '__main__':
    if len(argv) == 2:
        global lock
        global name
        global port
        global server_number
        global counter
        lock = Lock()
        server_number = int(argv[1])
        name, port = generate_name_port()
        counter = [0, 0, 0]
        log = getLogger('werkzeug')
        log.setLevel(ERROR)
        Thread(target=lambda: app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)).start()
        sleep(1)
        run_events_interval()
        run_sends_randomly()
    else: 
        print("bad arguments, check readme")