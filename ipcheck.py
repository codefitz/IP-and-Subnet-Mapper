#!/usr/bin/python3

# Copyright 2019-2021 Wes Moskal-Fitzpatrick
# Licensed under Apache Version 2.0

import ipaddress
import csv
import argparse
from argparse import RawTextHelpFormatter
from cidrize import cidrize
import sys

parser = argparse.ArgumentParser(description='IP Subnet Checker',formatter_class=RawTextHelpFormatter)
parser.add_argument('-s', '--subnet', dest='subnet',  type=str, required=False, help='A subnet to check against.\n\n', metavar='<subnet>')
parser.add_argument('-S', '--subnets_file', dest='subnets_file',  type=str, required=False, help='CSV file containing a list of subnets to check against.\n\nFormat - IPAddress, Name\n\n', metavar='<filename>')
parser.add_argument('-i', '--ip_address', dest='ip_address',  type=str, required=False, help='IP address to check in subnet.\n\n', metavar='<ip address>')
parser.add_argument('-I', '--ip_file', dest='ip_file',  type=str, required=False, help='CSV file containing IP addresses to check in subnet.\n\nFormat - Subnet, Name\n\n', metavar='<filename>')
parser.add_argument('-o', '--output_file', dest='output_file',  type=str, required=False, help='Specify a CSV output_file file.\n\n', metavar='<filename>')

args = parser.parse_args()
subnet = args.subnet
subnets_file = args.subnets_file
ip_addr = args.ip_address
ip_file = args.ip_file
output_file = args.output_file
subnets_list = []
if subnets_file:
    with open(subnets_file) as file:
        subnets_list = list(csv.reader(file))

if not ip_addr and not ip_file:
    parser.print_help()
    sys.exit(1)

def range_to_ips(iprange):
    list_of_ips = []
    if iprange:
        try:
            ipaddr = ipaddress.ip_address(iprange)
            list_of_ips.append(ipaddr)
        except:
            try:
                ipaddrs = ipaddress.ip_network(iprange)
                for ipaddr in ipaddrs:
                    list_of_ips.append(ipaddr)
            except:
                try:
                    ipaddrs = ipaddress.ip_network(iprange,strict=False)
                    msg = 'Address %s is not valid CIDR syntax, using recommended CIDR: %s' % (iprange, ipaddrs)
                    print(msg)
                    for ipaddr in ipaddrs:
                        list_of_ips.append(ipaddr)
                except:
                    try:
                        cidrip = cidrize(iprange)
                        for cidr in cidrip:
                            ipaddrs = ipaddress.ip_network(cidr)
                            for ipaddr in ipaddrs:
                                list_of_ips.append(ipaddr)
                    except:
                        msg = 'Address %s is not valid CIDR syntax, cannot process!' % (iprange)
                        print(msg)
    return list_of_ips

def validate_subnet(subnet):
    if subnet:
        try:
            ip = ipaddress.ip_address(subnet)
            subbed = ipaddress.ip_network(ip)
            return subbed
        except:
            try:
                subbed = ipaddress.ip_network(subnet)
                return subbed
            except:
                try:
                    subbed = ipaddress.ip_network(subnet,strict=False)
                    msg = 'Address %s is not valid CIDR syntax, using recommended CIDR: %s' % (subnet, subbed)
                    print(msg)
                    return subbed
                except:
                    try:
                        cidrip = cidrize(subnet)
                        if cidrip:
                            for cidr in cidrip:
                                subbed = ipaddress.ip_network(str(cidr))
                                return subbed
                        else:
                            raise ValueError('cidrize returned no results')
                    except:
                        msg = 'Subnet %s is not valid CIDR syntax, cannot process!' % (subnet)
                        print(msg)

def output(ip,ip_name,valid_subnet,subnet,sub_name):
    if valid_subnet:
        if ip in valid_subnet:
            values = [str(ip),ip_name,str(valid_subnet),sub_name,True,ip_addr,subnet]
            msg = ("IP Address",values[0],"found in",values[2],"( Inputted Address:",values[5],"Inputted Subnet:",values[6],")")
        else:
            values = [str(ip),ip_name,str(valid_subnet),sub_name,False,ip_addr,subnet]
            msg = ("IP Address",values[0],"NOT in",values[2],"( Inputted Address:",values[5],"Inputted Subnet:",values[6],")")
        if output_file:
            mapped.append(values)
        else:
            print(' '.join(str(s) for s in msg))
            mapped.append(values)
    return mapped

def checkIPs(ip_addr, ip_name=None, subnets=None):
    count = 0
    ip_list = range_to_ips(ip_addr)
    for ip in ip_list:
        count += 1
        if subnet:
            validated = validate_subnet(subnet)
            mapped = output(ip, ip_name, validated, subnet, None)
        elif subnets:
            for line in subnets:
                subnet_ip = line[0]
                sub_name = line[1] if len(line) > 1 else None
                validated = validate_subnet(subnet_ip)
                mapped = output(ip, ip_name, validated, subnet_ip, sub_name)
    mapped.sort( key = lambda k: ipaddress.ip_address(k[0]) )
    return mapped

mapped = []

if ip_addr:
    mapped = checkIPs(ip_addr, subnets=subnets_list)
    mapped.insert(0, [ "IP Address", "IP Name", "Subnet", "Subnet Name", "In Subnet", "Inputted Address", "Inputted Subnet" ])
elif ip_file:
    with open(ip_file) as file:
        reader = csv.reader(file)
        count = 0
        for line in reader:
            ip_addr = line[0]
            ip_name = line[1]
            mapped = checkIPs(ip_addr, ip_name, subnets=subnets_list)
        mapped.insert(0, [ "IP Address", "IP Name", "Subnet", "Subnet Name", "In Subnet", "Inputted Address", "Inputted Subnet" ])

processed_count = len(mapped) - 1
if processed_count < 0:
    processed_count = 0
print (processed_count,"IP addresses processed.\n")

if output_file:
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(mapped)
    print("Results saved to",output_file,"\n")
