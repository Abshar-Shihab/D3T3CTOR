#!/usr/bin/env python3
import os
import signal
import sys
import time
from scapy.layers.dot11 import *
from scapy.sendrecv import sniff
from subprocess import getoutput

ALLOWED_SSIDS = {"MAS-Comp Dep", "MAS-MTS Dep"}


def check_interface_exists(interface):
    """Check if the wireless interface exists"""
    interfaces = getoutput("iwconfig 2>/dev/null | grep 'IEEE' | awk '{print $1}'").split()
    return interface in interfaces


def check_root():
    """Check if the script is running with root privileges"""
    if os.geteuid() != 0:
        print("\n\033[1;91m[!] This script requires root privileges\033[0;0m")
        sys.exit(1)


def change_mode():
    """Change the mode of the network interface using os.system with error handling"""
    try:
        if check_interface_exists("wlan0mon"):
            os.system("airmon-ng stop wlan0mon")
            time.sleep(2)  # Give system time to process
        os.system("systemctl restart NetworkManager")
        print("\n\033[1;93m[+] Successfully reverted to managed mode\033[0;0m")
    except Exception as e:
        print(f"\n\033[1;91m[!] Error changing mode: {e}\033[0;0m")


def packet_handler(pkt):
    """Handle captured packets with error handling"""
    try:
        if pkt.haslayer(Dot11Beacon) or pkt.haslayer(Dot11ProbeResp):
            if Dot11Elt in pkt and hasattr(pkt[Dot11Elt], 'info'):
                ssid = pkt[Dot11Elt].info.decode("utf-8", errors="ignore")
                bssid = pkt[Dot11].addr2  # MAC Address of the AP
                # Check if SSID starts with "MAS-" but is not in the allowed list
                if ssid.startswith("MAS-") and ssid not in ALLOWED_SSIDS:
                    print(f"\033[1;91m[ROGUE AP DETECTED] Unauthorized MAS Network Found! SSID: \033[1;101;97m{ssid}\033[0;0m\033[1;91m, BSSID: \033[1;101;97m{bssid}\033[0;0m")
    except Exception as e:
        print(f"\n\033[1;91m[!] Error processing packet: {e}\033[0;0m")


def setup_monitor_mode():
    """Setup monitor mode with error handling"""
    try:
        if not check_interface_exists("wlan0"):
            print("\n\033[1;91m[!] Wireless interface wlan0 not found\033[0;0m")
            return False

        print("\n\033[1;93m[*] Killing interfering processes...\033[0;0m")
        os.system("airmon-ng check kill")
        time.sleep(2)  # Give system time to process

        print("\033[1;93m[*] Changing into Monitor mode...\033[0;0m")
        result = os.system("airmon-ng start wlan0")
        time.sleep(2)  # Give system time to process

        if result != 0 or not check_interface_exists("wlan0mon"):
            print("\n\033[1;91m[!] Failed to enable monitor mode\033[0;0m")
            return False

        return True
    except Exception as e:
        print(f"\n\033[1;91m[!] Error setting up monitor mode: {e}\033[0;0m")
        return False


def main():
    """Main function with error handling and retries"""
    check_root()
    print("\n\033[1;93m[*] Starting WiFi monitoring script...\033[0;0m")

    if not setup_monitor_mode():
        print("\n\033[1;91m[!] Failed to setup monitor mode. Exiting...\033[0;0m")
        return

    # Start sniffing with retry mechanism
    max_retries = 3
    retry_count = 0

    while retry_count < max_retries:
        try:
            print("\n\033[1;93m[*] Monitoring for Rogue APs...\033[0;0m")
            sniff(iface="wlan0mon", prn=packet_handler, store=False, filter="type mgt subtype beacon or subtype probe-resp")
            break
        except OSError as e:
            if "Network is down" in str(e):
                retry_count += 1
                print(f"\n\033[1;91m[!] Network interface error. Attempt {retry_count} of {max_retries}\033[0;0m")
                time.sleep(5)  # Wait before retrying
                setup_monitor_mode()  # Try to reset the interface
            else:
                print(f"\n\033[1;91m[!] Error: {e}\033[0;0m")
                break
        except Exception as e:
            print(f"\n\033[1;91m[!] Unexpected error: {e}\033[0;0m")
            break


def cleanup(sig, frame):
    """Cleanup function for graceful exit"""
    print("\n\033[1;93m[+] Exiting... Reverting monitor to managed mode.\033[0;0m")
    change_mode()
    sys.exit(0)


signal.signal(signal.SIGINT, cleanup)
main()
