from flask import Flask, jsonify, request
import threading
import random
import requests
import sys

# creating a Flask app
app = Flask(__name__)
  
# on the terminal type: curl http://127.0.0.1:5000/
# returns hello world when we use GET.
# returns the data that we send when we use POST.

# body = {
#     "counter": [1, 1, 3]
# }



@app.route('/', methods = ['POST'])
def home():
    if(request.method == 'POST'):
        receive_message(request.json)
        return jsonify({'result': 'success'})


def receive_message(request):
    print(f"[{name}] counter before receiving: {counter}" )
    counter[server_number] += 1
    for x in range(len(counter)):
        if request["counter"][x] > counter[x]:
            counter[x] = request["counter"][x]
    print(f"[{name}] counter after receiving: {counter}")

def send_message(server_port):
    try:
        if (server_port != port):
            print(f"[{name}] counter before send: {counter}")
            url = 'http://localhost:' + str(server_port)
            body = {
                "counter": counter
            }
            requests.post(url, json=body)
            counter[server_number] += 1
            print(f"[{name}] counter after send: {counter}")
    except:
        pass

def do_event():
    print(f"[{name}] counter before event: {counter}")
    counter[server_number] += 1
    print(f"[{name}] counter after event: {counter}")

def generate_name_port():
    port = 8080 + server_number
    name = "server_" + str(port)
    return name, port

def run_events_randomly():
    threading.Timer(15, run_events_randomly).start()
    do_event()

def run_sends_randomly():
    threading.Timer(15, run_sends_randomly).start()
    send_message(8080 + random.randint(0,2))

if __name__ == '__main__':
    if len(sys.argv) == 2:
        global name
        global port
        global server_number
        global counter
        server_number = int(sys.argv[1])
        name, port = generate_name_port()
        counter = [0, 0, 0]
        threading.Thread(target=lambda: app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)).start()
        run_events_randomly()
        run_sends_randomly()
    else: 
        print("bad arguments, check readme")