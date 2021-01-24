R = '\033[31m'  # red
G = '\033[32m'  # green
C = '\033[36m'  # cyan
W = '\033[0m'  # white
B = '\033[1m'
I = "\033[3m"

import os
import csv
import sys
import time
import json
import argparse
import requests
import subprocess as subp
from pyngrok import ngrok


print(f'''{R}
⠀⣀⣀⣀⣀⡀⠀⠀⣀⣀⣀⣀⠀⠀⠀⠀⠀⠀⣀⡀⠀⠀⠀⠀⠀⠀⣀⣀⣀⣀⣀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⡀⠀⠀⠀⠀⠀
⠀⠉⣿⣿⠉⠁⠀⢀⣽⡿⠟⠉⠀⠀⠀⠀⠀⣰⣿⣿⣄⠀⠀⠀⠀⠀⠉⢹⣿⡏⠉⠉⠻⣿⣶⡆⠀⠀⠀⠀⠀⢀⣾⣿⣷⡀⠀⠀⠀⠀
⠀⠀⣿⣿⢀⣤⡾⠟⠁⠀⠀⠀⠀⠀⠀⠀⣾⡟⠈⢻⣿⣄⠀⠀⠀⠀⠀⢸⣿⡇⠀⠀⣠⣿⡿⠃⠀⠀⠀⠀⢠⣿⠃⠘⣿⣿⡀⠀⠀⠀
⠀⠀⣿⣿⠙⠿⣿⣧⣀⠀⠀⠀⠀⠀⢠⣼⠿⠶⠶⠾⢿⣿⣆⠀⠀⠀⠀⢸⣿⡟⠛⢿⣿⣥⡀⠀⠀⠀⠀⣰⡿⠷⠶⠶⠾⣿⣿⡄⠀⠀
⠀⠀⣿⣿⡄⠀⠈⠻⣿⣷⣄⡀⠀⣰⣾⠏⠀⠀⠀⠀⠀⢿⣿⣇⡀⠀⠀⢸⣿⣇⠀⠀⠹⣿⣷⣄⡀⠀⣼⡿⠃⠀⠀⠀⠀⠉⣿⣷⣆⠀
⠀⠉⠉⠉⠉⠁⠀⠀⠀⠉⠉⠉⠛⠉⠉⠙⠀⠀⠀⠀⠘⠉⠉⠉⠉⠁⠉⠉⠉⠉⠃⠀⠀⠀⠉⠙⠛⠉⠉⠉⠉⠀⠀⠀⠀⠋⠉⠉⠉⠉
⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣠⣤⣤⣄⣀⣀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣀⣀⣀⣀⣀⣀⣀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣠⣶⠿⠋⠉⠉⠉⢹⣿⠀⠀⠀⠀⢀⣠⣶⡿⠿⠟⢛⣛⣛⡛⠿⠿⣿⣦⣄⠀⠀⠀⠸⣿⠉⠉⠉⠉⣉⣿⣿⠟⠀⠀⠀⠀⠀
⠀⠀⠀⣿⣿⠃⠀⠀⠀⠀⠀⠈⠁⠀⠀⠀⣤⠟⠋⠀⠀⠀⣾⣿⣿⣿⣿⣧⠀⠀⠈⠙⢳⣄⠀⠀⠀⠀⠀⢀⣴⣿⡟⠃⠀⠀⠀⠀⠀⠀
⠀⠀⢸⣿⣿⠀⠀⠀⠀⢠⣤⣤⣤⣤⠀⠈⣁⠀⠀⠀⠀⠸⣿⣯⡀⣀⣿⣿⠀⠀⠀⠀⠀⣉⠀⠀⠀⠀⣰⣿⡿⠉⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⢿⣿⣆⠀⠀⠀⠀⠀⣿⣿⠀⠀⠀⠙⢷⣦⣄⠀⠀⠻⣿⣿⣿⡿⠏⠀⠀⣠⣴⡞⠁⠀⠀⢠⣾⣿⠋⠁⠀⠀⠀⣴⡆⠀⠀⠀⠀
⠀⠀⠀⠀⠙⠻⢿⣦⣤⣤⣤⣿⣿⠀⠀⠀⠀⠀⠘⠛⢿⣿⣶⣶⣶⣶⣶⣾⣿⠿⠛⠁⠀⠀⠀⠸⠿⠿⠷⠶⠶⠶⠶⠾⠿⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀   ''' + W)
print(f"""{B}{C}{I}                           
                 Coded by team Terminal World{W}
""")

print (f'{B}{R}[1]{C}-Photo{W}')
print (f'{B}{R}[2]{C}-Audio{W}')
print (f'{B}{R}[3]{C}-Geolocation{W}')
sel=input(f'{G}Select number: {W}')

if sel=='1':
	os.system("chmod +x ph.sh && ./ph.sh")
elif sel=='2':
	os.system("chmod +x au/au.sh && ./au/au.sh")
elif sel=='3':
	os.system("python3 ge.py")
else:
	print("Invalid number")
	


