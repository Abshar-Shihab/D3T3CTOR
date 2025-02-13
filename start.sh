#!/bin/bash

echo "[INFO] Checking for Python3..."
if ! command -v python3 &> /dev/null
then
    echo "[WARNING] Python3 is not installed! Installing now..."
    sudo apt install python3 -y
else
    echo "[OK] Python3 is already installed."
fi


echo "\n[INFO] Checking for Scapy..."
if ! python3 -c "import scapy" &> /dev/null; then
    echo "[WARNING] Scapy not found, installing via apt..."
    sudo apt install python3-scapy -y
else
    echo "[OK] Scapy is already installed."
fi



echo "\n[INFO] Starting ARP Detection..."
sudo python3 src/top-module.py
