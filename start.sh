#!/bin/bash

# Navigheaza in directorul in care se afla scriptul
cd "$(dirname "$0")" || exit

# Pornim serverul
gnome-terminal -- bash -c "echo -e '\033]0;Server UDP\007'; python3 server.py; exec bash" &

# Asteptam 1 secunda
sleep 1

# Pornim clientii
gnome-terminal -- bash -c "echo -e '\033]0;Client 1\007'; python3 client.py; exec bash" &
gnome-terminal -- bash -c "echo -e '\033]0;Client 2\007'; python3 client.py; exec bash" &
gnome-terminal -- bash -c "echo -e '\033]0;Client 3\007'; python3 client.py; exec bash" &