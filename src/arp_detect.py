# !/usr/bin/env python3
import time
import threading
import signal
import subprocess
from scapy.all import sniff
from scapy.layers.l2 import ARP

# Dictionary to store IP to MAC address mapping
arp_table = {}


def get_initial_arp_table():
    """Initialize ARP table with existing entries from system ARP cache"""
    try:
        # For Linux/Unix systems
        arp_output = subprocess.check_output(['arp', '-n']).decode('utf-8')

        # Skip header line and process each entry
        for line in arp_output.split('\n')[1:]:
            if line.strip():
                parts = line.split()
                if len(parts) >= 3:
                    ip = parts[0]
                    mac = parts[2]
                    if ":" in mac:  # Verify it's a valid MAC address
                        arp_table[ip] = mac
    except Exception as e:
        print(f"Error initializing ARP table: {e}")
        print("Continuing with empty ARP table...")


def process_packet(packet):
    if packet.haslayer(ARP):
        ip = packet[ARP].psrc
        mac = packet[ARP].hwsrc

        if ip in arp_table:
            if arp_table[ip] != mac:
                print("[ALERT!!!] ARP Spoofing Detected!")
                print("""\033[1;91m

                      .o.            ooooo             oooooooooooo      ooooooooo.        ooooooooooooo      .o. .o. .o.
                     .888.           `888'             `888'     `8      `888   `Y88.      8'   888   `8      888 888 888
                    .8"888.           888               888               888   .d88'           888           888 888 888
                   .8' `888.          888               888oooo8          888ooo88P'            888           Y8P Y8P Y8P
                  .88ooo8888.         888               888    "          888`88b.              888           `8' `8' `8'
                 .8'     `888.        888       o       888       o       888  `88b.            888           .o. .o. .o.
                o88o     o8888o      o888ooooood8      o888ooooood8      o888o  o888o          o888o          Y8P Y8P Y8P

                                \033[0;0m""")
                print(
                    f"IP {ip} was previously associated with MAC {arp_table[ip]}, now seen as\033[0;91m {mac}\033[0;0m")
        else:
            arp_table[ip] = mac


def print_arp_table():
    while True:
        print("\n\033[1;94mCurrent ARP Table:\033[0;0m")
        for ip, mac in arp_table.items():
            print(f"IP: {ip} --> MAC: {mac}")
        print("-" * 40)
        time.sleep(5)


def main():
    # Initialize ARP table from system cache
    get_initial_arp_table()

    # Set up signal handler for clean exit (Ctrl+C)
    signal.signal(signal.SIGINT, lambda sig, frame: (print("\n"), exit(0)))

    # Start ARP table printing in a separate thread
    threading.Thread(target=print_arp_table, daemon=True).start()

    sniff(filter="arp", prn=process_packet, store=0)



main()
