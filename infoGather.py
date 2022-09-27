#!/usr/bin/env python3
# this is my Information Gathering miniProject
#
import socket
import requests
import sys , os
import urllib.request 
import json


try:
	os.system("figlet infoGather") #created  in exception for some users where figlet isnot present
except:
	pass
print(f"\nversion: v1.2")
try:
	domain = str(sys.argv[1])
	port = int(sys.argv[2])

except (IndexError , ValueError):
	print(f"\033[33mMust pass an argument!!!\033[37m")
	sys.exit(2)

try:
	sock = socket.create_connection((domain,port))
	sock.settimeout(50) #50secs , socket will wait 50 sec to try connecting with the  server
 
except:
	print(f"\033[33mHost  Unreachable!!!");
	sys.exit(2)

req = None #no requests

if sock.fileno() != -1: # if domain is up  , then analyse further
	print(f"\033[32mDomain {socket.gethostbyname(domain)} is Up... \033[37m")
	if port == 443:
		req = requests.get(f"https://{domain}",verify=False)
		print(f"Status Code : {req.status_code}")
		print(f"Service by port : {socket.getservbyport(port)}")

	if port == 80:
		req = requests.get(f"http://{domain}:{port}",verify=False)
		print(f"Status Code : {req.status_code}")
		print(f"Service by port : {socket.getservbyport(port)}")

print(f"Service by : {req.headers['Server']}")

# trying to look for only tcp ports and not "to check with bruteforcing"
f = open("../ports/ports.json")
data = json.load(f)
ports = []
for key,value in data.items():
	port = ''.join(key.split('/')[0])
	if int(port)<2049:
		ports.append(port)
	else:
		break

for i in set(ports):
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # only dicovers TCP ports i repeat only discovers TCP ports
	s.settimeout(0.2) 
	result = s.connect_ex((domain,int(i)))
	if result == 0:
		print(f"Discovered port {i}")

# request's  headers 
for i in req.headers:
	print(req.headers[i])

 


