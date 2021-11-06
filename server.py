import sys
import time
import socket

status = True
message = b''


def run():
    global status
    global message
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('0.0.0.0', 4545))
    sock.listen(50)  # Сколько соединения
    while status:
        if status == False:
            print('Server stop')
            break
        try:
            client, addr = sock.accept()
        except KeyboardInterrupt as err:
            sock.close()
            print('err')
            break
        else:
            message = client.recv(1024)
            client.close()
            print(f'IP: {addr}')
            print('Message: ', message.decode('utf-8'))


def stop():
    global status
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('127.0.0.1', 4545))

    sock.send('Server down'.encode('utf-8'))  # send byte 'localhost' or '127.0.0.1'

    sock.close()
    status = False
    sys.exit()
