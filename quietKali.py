#! /bin/python
import sys
import os
import string
import random
from argparse import ArgumentParser

parser = ArgumentParser(description='Modify your Kali machine to look more like a normal machine on the network and keep from giving yourself away to the defenders.')
parser.add_argument('--on', action='store_true', help='Enable quietKali. This will modify your machine to keep from connecting to Kali servers.')
parser.add_argument('--off', action='store_true', help='Disable quietKali. This will remove settings set when turning on quietKali and allow you to connect to Kali servers again. quietKali must be off to run apt-get update and install.')
parser.add_argument('-m', '--mac', help='Change MAC address. Specify the interface you want to change the MAC address of. If using the --hostname (-n) option, the MAC address will be changed to match the type of host you are emulating.')
parser.add_argument('-n', '--hostname', help='Set hostname. Valid options are random, router, printer, workstation, server, or manual. Manual will request a string to use as the hostname, which will allow you to match to the customer environment better.')
parser.add_argument('--revert', action='store_true', help='Revert changes. Will turn off quietKali and restore settings for mac and hostname changes.')

args = parser.parse_args()
if not len(sys.argv) > 1:
        parser.print_help()
if (args.revert) > 2:
	print("Revert must be run without any other arguments.")
	exit()

def quietKali():
	if args.on == True:
		print("Turning on quietKali")
		quietKaliOn()
	elif args.off == True:
		print("Turning off quietKali")
		quietKaliOff()
	if args.revert == True:	
		revert()
	if args.mac:
		macChange()
	if args.hostname:
		hostnameChange()

def revert():
	print("Reverting machine...Please wait")
	print("Reverting MAC Address...")
        inter=raw_input("What interface should be reset?:")
	os.system("ifconfig " + inter + " down")
        os.system("macchanger -p " + inter)
        print("Your MAC address has been reset.")
        os.system("ifconfig " + inter + " up")


def macChange():
	print("Changing MAC Address...")
	os.system("ifconfig " + args.mac + " down")
	os.system("macchanger -r " + args.mac)
	print("Your MAC address has been changed.")
	os.system("ifconfig " + args.mac + " up")

def hostnameChange():
	hostnameLower=args.hostname.lower()
	hostnameNew=""
	if hostnameLower == "server":
		print("You selected a Server hostname. Generating....")
		number=id_generator()
		hostnameNew="Server-" + number
	elif hostnameLower == "workstation":
		print("You selected a Workstation hostname. Generating....")
		number=id_generator()
                hostnameNew="Workstation-" + number	
	elif hostnameLower == "printer":
		print("You selected a Printer hostname. Generating....")
		number=id_generator()
                hostnameNew="Printer-" + number
	elif hostnameLower == "router":
		print("You selected a Router hostname. Generating....")
		number=id_generator()
                hostnameNew="Router-" + number
	elif hostnameLower == "random":
		print("You selected a Random hostname. Generating....")
		number=id_generator()
                hostnameNew="Random-" + number
	elif hostnameLower == "manual":
		hostnameNew=raw_input("Please enter the hostname you would like to use: ")
	else:
		print("I am unsure what you are requesting, so I am generating a random hostname....")	
		number=id_generator()
                hostnameNew="Random-" + number
	# Backup original hostname
	os.system("cp /etc/hostname /etc/hostname.orig")
	os.system("echo " + hostnameNew + " > /etc/hostname")
	os.system("service hostname.sh")
	print("Hostname has been changed to: " + hostnameNew)

def id_generator(size=4, chars=string.digits):
                return ''.join(random.choice(chars) for _ in range(size))

#def serverBaseName():
#	return random.choice(open("servers.txt").readlines())	

quietKali()
