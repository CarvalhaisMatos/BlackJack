#encoding: utf8
__author__ = 'Diogo Gomes'
__email__ = 'dgomes@ua.pt'
__license__ = "GPL"
__version__ = "0.1"
import json 
import zmq
from player import Player
from student import StudentPlayer
from json_utils import object_to_dict
from json_utils import dict_to_object
from game import Game

context = zmq.Context()

#  Socket to talk to server
print("Connecting to Casino…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

p = Player("Human", 100)

print("Sending request …")
socket.send("HELLO" + str(p))

#  Get the reply.
message = socket.recv()
print("Received reply [{}]".format(message))
socket.send("OK" + str(p))
while True:
    msg = json.loads(socket.recv(), object_hook=dict_to_object)

    if msg['cmd'] == 'SHOW':
        p.show(msg['players'])
        socket.send("OK")
    elif msg['cmd'] == 'WANT_TO_PLAY':
        socket.send(json.dumps(p.want_to_play(msg['rules'])))
    elif msg['cmd'] == 'PAYBACK':
        p.payback(msg['prize'])
        socket.send("OK")
    elif msg['cmd'] == 'PLAY':
        socket.send(json.dumps(p.play(msg['dealer'], msg['players'])))
    elif msg['cmd'] == 'BET':
        socket.send(json.dumps(p.bet(msg['dealer'], msg['players'])))
    else:
        print("ERROR UNKNOWN MESSAGE:")
        print msg
        socket.send("ERROR")
