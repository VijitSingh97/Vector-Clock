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
# returns the success when we send valid update vector_clock message
# example body:
#   body = {
#       "vector_clock": [1, 1, 3]
#   }
@app.route('/', methods = ['POST'])
def home():
    receive_message(request.json)
    return jsonify({'result': 'success'})

# method that handles incoming message 
def receive_message(request):
    lock.acquire()
    try:
        print(f"[{name}] vector_clock before receiving: {vector_clock}" )
        for x in range(len(vector_clock)):
            if request["vector_clock"][x] > vector_clock[x]:
                vector_clock[x] = request["vector_clock"][x]
        vector_clock[server_number] += 1
        print(f"[{name}] vector_clock after receiving: {vector_clock}")
    finally:
        lock.release()

# method that sends message to other servers in network
def send_message(server_port):
    lock.acquire()
    try:
        try:
            if (server_port != port):
                url = 'http://localhost:' + str(server_port)
                body = {
                    "vector_clock": vector_clock
                }
                post(url, json=body, timeout=20)
                print(f"[{name}] vector_clock before send: {vector_clock}")
                vector_clock[server_number] += 1
                print(f"[{name}] vector_clock after send: {vector_clock}")
        except Exception as e:
            # pass
            print(f"[{name}] send failed: {vector_clock}")
    finally:
        lock.release()

# method that performs arbitrary event 
def do_event():
    lock.acquire()
    try:
        print(f"[{name}] vector_clock before event: {vector_clock}")
        sleep(1)
        vector_clock[server_number] += 1
        print(f"[{name}] vector_clock after event: {vector_clock}")
    finally:
        lock.release()
# generate name and port from server_number input argument 
def generate_name_port():
    port = 8080 + server_number
    name = "server_" + str(port)
    return name, port

# run event on a random interval
def run_events_interval():
    Timer(randint(0,5), run_events_interval).start()
    do_event()

# run send on a random interval
def run_sends_randomly():
    Timer(randint(0,30), run_sends_randomly).start()
    send_message(8080 + randint(0,2))

# main method
if __name__ == '__main__':
    # check we have argument
    if len(argv) == 2:
        # create global vars for lock, server name, port, server number and vector clock ()
        global lock
        global name
        global port
        global server_number
        global vector_clock
        # assign global vars
        lock = Lock()
        server_number = int(argv[1])
        name, port = generate_name_port()
        vector_clock = [0, 0, 0]
        # mute flask logger
        log = getLogger('werkzeug')
        log.setLevel(ERROR)
        # start receiving incoming vector clocks
        Thread(target=lambda: app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)).start()
        # sleep to avoid mixing with flask start up logs
        sleep(2)
        # start event and send threads
        # run_events_interval()
        run_sends_randomly()
    else: 
        print("bad arguments, check readme")