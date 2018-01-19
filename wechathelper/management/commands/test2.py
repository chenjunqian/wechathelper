from multiprocessing.connection import Client
import time
import zmq
from multiprocessing import Process
import os


def foo(name):
    
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect('tcp://127.0.0.1:6000')
    socket.send_string('Hello'+name)
    message = socket.recv()
    print("Received request: %s" % message)
    


if __name__ == '__main__':
    n = 10
    while n >=0:
        n = n-1
        p = Process(target=foo, args=(str(n),))
        p.start()
        p.join()
