#!/bin/bash

echo "Se opresc procesele Python..."
# Suprimam output-ul in caz ca nu exista procese de oprit
pkill -f "python.*server.py" >/dev/null 2>&1
pkill -f "python.*client.py" >/dev/null 2>&1

echo "Se inchid terminalele..."
# In Linux, oprirea procesului principal inchide automat si fereastra terminalului asociat
echo "Gata. Toate procesele au fost oprite."

# Echivalentul comenzii 'pause'
read -n 1 -s -r -p "Apasati orice tasta pentru a continua..."
echo ""