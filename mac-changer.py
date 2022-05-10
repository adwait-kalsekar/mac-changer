#!/usr/bin/python3

import subprocess
import argparse
import sys
import re #regex


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--interface", dest="interface", help="Interface to change the mac address")
    parser.add_argument("-m", "--mac", dest="new_mac", help="New Mac address to assign")
    options = parser.parse_args()
    if not options.interface:
        print("[-]Error. No interface specified. Use --help for more info")
        sys.exit()
    elif not options.new_mac:
        print("[-]Error. No mac address specified. Use --help for more info")
        sys.exit()
    return options


def get_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))
    if not mac_address:
        print("[-]Error. Could not read MAC address on interface '" + interface + "'")
    else:
        return mac_address.group(0)


def change_mac(interface, new_mac):
    print("[+]Changing MAC address for '" + interface + "' to " + new_mac)
    subprocess.call(["sudo", "ifconfig", interface, "down"])
    subprocess.call(["sudo", "ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["sudo", "ifconfig", interface, "up"])


options = get_arguments()
current_mac = get_mac(options.interface)
if current_mac:
    print("Current MAC: " + str(current_mac))
    change_mac(options.interface, options.new_mac)
    current_mac = get_mac(options.interface)
    if current_mac == options.new_mac:
        print("[+]MAC address successfully changed to " + current_mac)
    else:
        print("\n[-]MAC address could not be changed")
