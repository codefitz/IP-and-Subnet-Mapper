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
    if not iprange:
        return list_of_ips

    try:
        ipaddr = ipaddress.ip_address(iprange)
        list_of_ips.append(ipaddr)
        return list_of_ips
    except ValueError:
        pass

    try:
        ipaddrs = ipaddress.ip_network(iprange)
        list_of_ips.extend(ipaddrs)
        return list_of_ips
    except ValueError:
        pass

    try:
        ipaddrs = ipaddress.ip_network(iprange, strict=False)
        print('Address %s is not valid CIDR syntax, using recommended CIDR: %s' % (iprange, ipaddrs))
        list_of_ips.extend(ipaddrs)
        return list_of_ips
    except ValueError:
        pass

    try:
        cidrip = cidrize(iprange)
        for cidr in cidrip:
            for ipaddr in ipaddress.ip_network(cidr):
                list_of_ips.append(ipaddr)
    except Exception:
        print('Address %s is not valid CIDR syntax, cannot process!' % (iprange))

    return list_of_ips

def validate_subnet(subnet):
    if not subnet:
        return None

    try:
        ip = ipaddress.ip_address(subnet)
        return ipaddress.ip_network(ip)
    except ValueError:
        pass

    try:
        return ipaddress.ip_network(subnet)
    except ValueError:
        pass

    try:
        subbed = ipaddress.ip_network(subnet, strict=False)
        print('Address %s is not valid CIDR syntax, using recommended CIDR: %s' % (subnet, subbed))
        return subbed
    except ValueError:
        pass

    try:
        cidrip = cidrize(subnet)
        return ipaddress.ip_network(cidrip)
    except Exception:
        print('Subnet %s is not valid CIDR syntax, cannot process!' % (subnet))

def output(ip, ip_name, valid_subnet, subnet, sub_name):
    if not valid_subnet:
        return mapped

    in_net = ip in valid_subnet
    values = [str(ip), ip_name, str(valid_subnet), sub_name, in_net, ip_addr, subnet]
    status = "found in" if in_net else "NOT in"
    msg = ("IP Address", values[0], status, values[2], "( Inputted Address:", values[5], "Inputted Subnet:", values[6], ")")

    if not output_file:
        print(' '.join(str(s) for s in msg))
    mapped.append(values)
    return mapped

def checkIPs(ip_addr, ip_name=None):
    ip_list = range_to_ips(ip_addr)
    for ip in ip_list:
        if subnet:
            validated = validate_subnet(subnet)
            output(ip, ip_name, validated, subnet, None)
        elif subnets_file:
            with open(subnets_file) as file:
                reader = csv.reader(file)
                for line in reader:
                    subnet_ip = line[0]
                    sub_name = line[1]
                    validated = validate_subnet(subnet_ip)
                    output(ip, ip_name, validated, subnet_ip, sub_name)
    mapped.sort(key=lambda k: ipaddress.ip_address(k[0]))
    return mapped

def main():
    mapped = []

    if ip_addr:
        mapped = checkIPs(ip_addr, mapped)
        mapped.insert(0, [
            "IP Address",
            "IP Name",
            "Subnet",
            "Subnet Name",
            "In Subnet",
            "Inputted Address",
            "Inputted Subnet",
        ])
    elif ip_file:
        with open(ip_file) as file:
            reader = csv.reader(file)
            count = 0
            for line in reader:
                ip_item = line[0]
                ip_name = line[1]
                mapped = checkIPs(ip_item, mapped, ip_name)
        mapped.insert(0, [
            "IP Address",
            "IP Name",
            "Subnet",
            "Subnet Name",
            "In Subnet",
            "Inputted Address",
            "Inputted Subnet",
        ])

    print(len(mapped) - 1, "IP addresses processed.\n")

    if output_file:
        with open(output_file, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(mapped)
        print("Results saved to", output_file, "\n")


if __name__ == "__main__":
    main()
