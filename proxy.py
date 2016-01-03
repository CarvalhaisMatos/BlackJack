#encoding: utf8
__author__ = 'Diogo Gomes'
__email__ = 'dgomes@ua.pt'
__license__ = "GPL"
__version__ = "0.1"
import json 
from player import Player
from student import StudentPlayer
from game import Game
import sys
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer

def dict_to_object(d):
    if '__class__' in d:
        class_name = d.pop('__class__')
        module_name = d.pop('__module__')
        module = __import__(module_name)
#        print 'MODULE:', module
        if class_name in ['Rules', 'PlayerState']:
            class_base = getattr(module, "Game")
            class_ = getattr(class_base, class_name)
        elif class_name == 'ProxyPlayer':
            module = __import__('player')
            class_ = getattr(module, 'Player')
        else:
            class_ = getattr(module, class_name)

#        print 'CLASS:', class_
        args = dict( (key.encode('ascii'), value) for key, value in d.items())
#        print 'INSTANCE ARGS:', args
        inst = class_(**args)
    else:
        inst = d
    return inst

KEEP_RUNNING = True
p = None


class PlayerRequestHandler (BaseHTTPRequestHandler):
    def do_POST(self):
        global p
        self.data_string = self.rfile.read(int(self.headers['Content-Length']))

        msg = json.loads(self.data_string, object_hook=dict_to_object)
        ret = "FAIL"
        code = 200

        if msg['cmd'] == 'SHOW':
            p.show(msg['players'])
            ret = "OK"
        elif msg['cmd'] == 'WANT_TO_PLAY':
            ret = p.want_to_play(msg['rules'])
        elif msg['cmd'] == 'PAYBACK':
            p.payback(msg['prize'])
            ret = p.pocket
        elif msg['cmd'] == 'PLAY':
            ret = p.play(msg['dealer'], msg['players'])
        elif msg['cmd'] == 'BET':
            ret = p.bet(msg['dealer'], msg['players'])
        elif msg['cmd'] == 'BYE':
            ret = "BYE"
        elif msg['cmd'] == 'NEW':
            p = Player(msg['name'], msg['money'])
            ret = "READY"
        else:
            print("ERROR UNKNOWN MESSAGE:")
            print(msg)
            ret = "ERROR"
            code = 500

        self.send_response(code)
        self.end_headers()
        self.wfile.write(json.dumps(ret))
       
        if ret == "BYE":
            print "BYE"
            global KEEP_RUNNING
            KEEP_RUNNING = False
try:
    nmec = sys.argv[1]
    PORT_NUMBER = int(nmec)
    
    server = HTTPServer(('', PORT_NUMBER), PlayerRequestHandler)
    print 'Started httpserver on port ' , PORT_NUMBER
    
    #Wait forever for incoming htto requests
    while KEEP_RUNNING:
        server.handle_request()

except KeyboardInterrupt:
    print '^C received, shutting down the web server'
    server.socket.close()
