#!/usr/bin/env python3

import os
import sys
import time
import signal

def logo(): #Used asci art font - ANSI Shadow
    os.system("clear")
    print("""\033[1;91m
    
██████╗ ██████╗ ████████╗██████╗  ██████╗████████╗ ██████╗ ██████╗ 
██╔══██╗╚════██╗╚══██╔══╝╚════██╗██╔════╝╚══██╔══╝██╔═══██╗██╔══██╗
██║  ██║ █████╔╝   ██║    █████╔╝██║        ██║   ██║   ██║██████╔╝
██║  ██║ ╚═══██╗   ██║    ╚═══██╗██║        ██║   ██║   ██║██╔══██╗
██████╔╝██████╔╝   ██║   ██████╔╝╚██████╗   ██║   ╚██████╔╝██║  ██║
╚═════╝ ╚═════╝    ╚═╝   ╚═════╝  ╚═════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝  \033[0;0m                                                           
                                            \033[1;96mCyberSec Detection Tool\033[0;0m
                       \033[0;37mDeveloped by Abshar | Nahar | Soban | Danyal\033[0;0m

\n\033[1;106;97m#### Disclaimer: This tool is for educational purposes only    ####\033[0;0m
\033[1;106;97m#### Use responsibly. The developers are not liable for misuse ####\033[0;0m

""")


def main_menu():
    print("\033[1;92m[1] Man-in-the-Middle (MitM) Attacks\033[0;0m")
    print("\033[1;92m[2] Network Attacks\033[0;0m")
    print("\033[1;92m[3] Network Spoofing Attacks\033[0;0m")
    print("\033[1;92m[4] Denial-of-Service (DoS) & Flooding Attacks\033[0;0m")
    print("\033[1;92m[5] Exploitation Attacks\033[0;0m")
    print("\033[1;92m[0] Exit\033[0;0m")

    while True:
        try:
            choice = int(input("\nOPTION: "))
            if 0 > choice > 5:
                print("\033[1;37mInvalid option! Try again.\033[0;0m")
            break
        except ValueError:
            print("\033[1;37mInvalid option! Try again.\033[0;0m")

    if choice == 1:
            run_mitm_attacks()
    elif choice == 0:
        print("\n\033[1;91mExiting...\033[0;0m")
        exit(0)

def run_mitm_attacks():
    print("\n\t\t\033[1;103;97m    Man-in-the-Middle (MitM) Attacks    \033[0;0m\n")
    print("\033[1;92m[1] ARP Spoofing Detection\033[0;0m")
    print("\033[1;92m[2] Rough Access Point Detection\033[0;0m")
    print("\033[1;92m[3] Back\033[0;0m")
    print("\033[1;92m[0] Exit\033[0;0m")

    while True:
        try:
            choice = int(input("\nOPTION: "))
            if 0 > choice > 3:
                print("\033[1;37mInvalid option! Try again.\033[0;0m")
            break
        except ValueError:
            print("\033[1;37mInvalid option! Try again.\033[0;0m")

    if choice == 1:
        run_arp_detection()
    elif choice == 2:
        os.system("python3 src/roughAP_detection.py")
        input("Press Enter to Continue....")
        os.system("clear")
        run_mitm_attacks()
    elif choice == 3:
        logo()
        main_menu()
    else:
        print("\n\033[1;91mExiting...\033[0;0m")
        exit(0)

def run_arp_detection():
    #os.system("clear")
    print("\n\t\t\033[1;103;97m    ARP SPOOFING DETECTION    \033[0;0m\n")
    print("\033[1;92m[1] Run ARP Spoofing Detection\033[0;0m")
    print("\033[1;92m[2] Print ARP Table\033[0;0m")
    print("\033[1;92m[3] Back\033[0;0m")
    print("\033[1;92m[0] Exit\033[0;0m")

    while True:
        try:
            choice = int(input("\nOPTION: "))
            if 0 > choice > 3:
                print("\033[1;37mInvalid option! Try again.\033[0;0m")
            break
        except ValueError:
            print("\033[1;37mInvalid option! Try again.\033[0;0m")

    if choice == 1:
        print("")
        for _ in range(5):
            sys.stdout.write("\r\033[1;93mRunning ARP Spoofing Detection......./")  # Print first state
            sys.stdout.flush()
            time.sleep(0.2)

            sys.stdout.write("\r\033[1;93mRunning ARP Spoofing Detection.......\\")  # Print second state
            sys.stdout.flush()
            time.sleep(0.2)
        print("")
        os.system("python3 src/arp_detect.py")
        input("Press Enter to Continue....")
        os.system("clear")
        run_arp_detection()

    elif choice == 3:
        run_mitm_attacks()

    elif choice == 0:
        print("\n\033[1;91mExiting...\033[0;0m")
        exit(0)


# setting up the signal handler to exit (Ctrl+C)
signal.signal(signal.SIGINT, lambda sig, frame: (print("\n\033[1;91mExiting...\033[0;0m"), exit(0)))

logo()
main_menu()
