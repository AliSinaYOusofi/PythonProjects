import pytube
import argparse
import concurrent.futures
import os
import sys

def check_module():
    try:
        from pytube import YouTube
    except ModuleNotFoundError as ME:
        print(f'[-] Module Not Installed: {ME}')
        choice = str(input('[*] Do You Want To Install The Module: '))
        if choice == 'y' or choice == 'Y' or choice == 'yes' or choice == 'Yes':
            os.system('pip install pytube')
        else:
            print('[):] Exiting')
            sys.exit(1)

def check_python_version():
    current_version = sys.version_info[0]
    if current_version != 3:
        print('[*] python3.x required')
        opt = str(input('[*] Update Python(y, n): '))
        if opt == 'y' or opt == 'Y' or opt == 'yes' or opt == 'Yes':
            os.system('pip install python3')
        else:
            print('[):] Exiting')
            sys.exit(1)

def pytube_downloader(url):
    print("**********************************VIDEO DETAILS*****************************************")
    objekt = pytube.YouTube(url=url)
    # printing Video Description if verbose
    # print(f'[+] Video Description: {objekt.description}')
    print(f'[+] Video Title: {objekt.title}')
    print(f'[+] Video Caption: {objekt.title}')
    print(f'[+] Video Views: {objekt.views}')
    print(f'[+] Video ID:{objekt.video_id}')
    print(f'[+] Video Length: {objekt.length}')
    print(f'[+] Video Publish Date: {objekt.publish_date}')
    print(f'[+] Video Is Age Restricted: {objekt.age_restricted}')
    print(f'[+] Video Author: {objekt.author}')
    print(f'[+] Video JS url: {objekt.js_url}')
    # resolutions available

    print('*******************************1080p RESOLUTION*****************************')
    high1080_resolution = objekt.streams.get_by_itag(248)
    high1080 = high1080_resolution.resolution
    print(f'[+] Video Resolution: {high1080}')
    print(f'[+] Video Size : {high1080_resolution.filesize}KB')
    print(f'[+] Video Defualt Name: {high1080_resolution.default_filename}')
    print(f'[+] Video Expiration Date: {high1080_resolution.expiration}')

    print('************************720p RESOLUTION***********************')
    high720_resolution = objekt.streams.get_by_itag(22)
    high720 = high720_resolution.resolution
    print(f'[+] Video Resolution: {high720}')
    print(f'[+] Video Size : {high720_resolution.filesize}KB')
    print(f'[+] Video Defualt Name: {high720_resolution.default_filename}')
    print(f'[+] Video Expiration Date: {high720_resolution.expiration}')

    print('***********************360p RESOLUTION**************************')
    lowest_resolution = objekt.streams.get_by_itag(18)
    low = lowest_resolution.resolution
    print(f'[+] Video Resolution: {low}')
    print(f'[+] Video Size : {lowest_resolution.filesize}KB')
    print(f'[+] Video Defualt Name: {lowest_resolution.default_filename}')
    print(f'[+] Video Expiration Date: {lowest_resolution.expiration}')

    print('*****************************480p RESOLUTION******************************')
    lowest480_resolution = objekt.streams.get_by_itag(18)
    low480 = lowest480_resolution.resolution
    print(f'[+] Video Resolution: {low480}')
    print(f'[+] Video Size : {lowest480_resolution.filesize}KB')
    print(f'[+] Video Defualt Name: {lowest480_resolution.default_filename}')
    print(f'[+] Video Expiration Date: {lowest480_resolution.expiration}')

    print('*********************************240p RESOLUTION*********************')
    high1080_resolution = objekt.streams.get_by_itag(242)
    high1080 = high1080_resolution.resolution
    print(f'[+] Video Resolution: {high1080}')
    print(f'[+] Video Size : {high1080_resolution.filesize}KB')
    print(f'[+] Video Defualt Name: {high1080_resolution.default_filename}')
    print(f'[+] Video Expiration Date: {high1080_resolution.expiration}')

    print('******************************144p RESOLUTION***************************')
    low144_resolution = objekt.streams.get_by_itag(160)
    low144 = low144_resolution.resolution
    print(f'[+] Video Resolution: {low144}')
    print(f'[+] Video Size : {low144_resolution.filesize}KB')
    print(f'[+] Video Defualt Name: {low144_resolution.default_filename}')
    print(f'[+] Video Expiration Date: {low144_resolution.expiration}')
    

if __name__ == '__main__':
    check_module()
    check_python_version()
    pytube_downloader('https://youtu.be/mS60nG6bJwo')
   

