#!/usr/bin/python3

# Copyright 2009 Wes Moskal-Fitzpatrick
# Licensed under Apache Version 2.0

import ipaddress
import csv

ipsub = {}

with open('subnets.csv') as subfile:
    reader = csv.reader(subfile)
    for line in reader:
        ipsub[line[0]] = line[1]

iplist = []
count = 0

with open('ips.csv') as ipfile:
    reader = csv.reader(ipfile)
    for line in reader:
        count += 1
        iplist.append(line[0])

mapped = []
exists = []


for sub in ipsub:
    for ip in iplist:
        if ipaddress.ip_address(ip) in ipaddress.ip_network(sub, False):
            mapped.append([ip,sub,ipsub[sub]])
            exists.append(ip)

for ip in iplist:
    if ip not in exists:
        mapped.append([ip,"None","None"])

mapped.sort()
with open('ips_mapped.csv', 'w') as file:
    file.writelines(','.join(i) + '\n' for i in mapped)

print ( "Done. " + str(count) + " IP addresses processed.")
