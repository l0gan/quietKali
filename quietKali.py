#! /bin/python
import sys
import os
import string
import random
from argparse import ArgumentParser

# quietKali is a script to make setting up your Kali instance for a red team engagement simpler.
# Ever been on an engagement and kali attempted to do an update, getting caught in web proxy logging?
# Ever been on an engagement and your kali box was named 'kali' or had the word kali in the name and it get caught by DHCP logging?
# quietKali will help quiet your computer to keep it from giving you away.
# quietKali also will allow you to randomize your hostname, and MAC address, so you are harder to detect.
# Coming soon! quietKali will attempt to match your MAC address to your hostname type. If you are using a printer hostname, 
# quietKali will set your MAC to match.

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
	macChanged=raw_input("Did you change your MAC address? (Y/N):")
	if macChanged.lower() == "y":
		print("Reverting MAC Address...")
        	inter=raw_input("What interface should be reset?:")
		os.system("ifconfig " + inter + " down")
        	os.system("macchanger -p " + inter)
        	print("Your MAC address has been reset.")
        	os.system("ifconfig " + inter + " up")
	hostnameChanged=raw_input("Did you change your hostname? (Y/N):")
	if hostnameChanged.lower() == "y":
		if os.path.isfile("/etc/hostname.orig"):
			os.system("mv /etc/hostname.orig /etc/hostname")
        		os.system("service hostname.sh")
        		print("Hostname has been changed back to your original name.")
		else:
			hostnameNew=raw_input("I did not find the backup file '/etc/hostname.orig'. Please enter the name you want to change the hostname to:")
			f=open("/etc/hostname","w")
			f.write(hostnameNew + "\n")
			f.close
			os.system("service hostname.sh") #Not sure why, but this isn't working like it should.... 
			print("Hostname has been set.")
	print("Turning off quietKali...")
	quietKaliOff()

def quietKaliOn():
	print("Backing up your hosts file...")
	os.system("cp /etc/hosts /etc/hosts.orig")
	os.system("echo '127.0.0.1    kali    kali.com    kali.org security.kali.org    http.kali.org    update.kali.org' >> /etc/hosts")
	os.system("iptables -A OUTPUT -d 192.124.249.10 -j DROP")
	os.system("iptables -A OUTPUT -d 192.99.200.113 -j DROP")


def quietKaliOff():
	print("Restoring your hosts file...")
	if os.path.isfile("/etc/hosts.orig"):
		os.system("mv /etc/hosts.orig /etc/hosts")
	else:
		print("The backup file '/etc/hosts.orig' is missing. Cannot revert hosts file. Please remove manually the line that says:\n127.0.0.1    kali    kali.com    kali.org security.kali.org    http.kali.org    update.kali.org")
	print("Reverting iptables rules...")
	os.system("iptables -D OUTPUT -d 192.124.249.10 -j DROP")
	os.system("iptables -D OUTPUT -d 192.99.200.113 -j DROP")

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
		servername=serverBaseName()
		hostnameNew=(servername.rstrip("\n") + "-" + number)
	elif hostnameLower == "workstation":
		print("You selected a Workstation hostname. Generating....")
		number=id_generator()
		workstationname=workstationBaseName()
                hostnameNew=(workstationname.rstrip("\n") + "-" + number)	
	elif hostnameLower == "printer":
		print("You selected a Printer hostname. Generating....")
		number=id_generator()
		printername=printerBaseName()
                hostnameNew=(printername.rstrip("\n") + "-" + number)
	elif hostnameLower == "router":
		print("You selected a Router hostname. Generating....")
		number=id_generator()
		routername=routerBaseName()
                hostnameNew=(routername.rstrip("\n") + "-" + number)
	elif hostnameLower == "random":
		print("You selected a Random hostname. Generating....")
		number=id_generator()
		randomname=randomBaseName()
                hostnameNew=(randomname.rstrip("\n") + "-" + number)
	elif hostnameLower == "manual":
		hostnameNew=raw_input("Please enter the hostname you would like to use: ")
	else:
		print("I am unsure what you are requesting, so I am generating a random hostname....")	
		number=id_generator()
                randomname=randomBaseName()
                hostnameNew=(randomname.rstrip("\n") + "-" + number)
	# Backup original hostname
	os.system("cp /etc/hostname /etc/hostname.orig")
	os.system("echo " + hostnameNew + " > /etc/hostname")
	os.system("service hostname.sh")
	print("Hostname has been changed to: " + hostnameNew)

def id_generator(size=4, chars=string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def serverBaseName():
	return random.choice(open("names/servers.txt").readlines())

def printerBaseName():
        return random.choice(open("names/printers.txt").readlines())

def workstationBaseName():
        return random.choice(open("names/workstations.txt").readlines())

def routerBaseName():
        return random.choice(open("names/routers.txt").readlines())

def randomBaseName():
	randomfile=random.choice(os.listdir("names/"))
        return random.choice(open("names/" + randomfile).readlines())

if __name__ == "__main__":
	quietKali()
