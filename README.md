# IP and Subnet Mapper v0.1.2

Check for an IP address within a given Subnet.

## Input Files

| Flag | File | Format | Column 1 | Column 2 |
| :--: | ---- | ------ | -------- | -------- |
| -I   | IP Addresses | CSV | IP Address/CIDR Range | Network Name |
| -S   | Subnets      | CSV | Subnet CIDR           | Subnet Name  |

## Example Usage

### Help

```shell
$ python3 ipcheck.py -h
usage: ipcheck.py [-h] [-s <subnet>] [-S <filename>] [-i <ip address>] [-I <filename>] [-o <filename>]

IP Subnet Checker

optional arguments:
  -h, --help            show this help message and exit
  -s <subnet>, --subnet <subnet>
                        A subnet to check against.

  -S <filename>, --subnets_file <filename>
                        CSV file containing a list of subnets to check against.

                        Format - IPAddress, Name

  -i <ip address>, --ip_address <ip address>
                        IP address to check in subnet.

  -I <filename>, --ip_file <filename>
                        CSV file containing IP addresses to check in subnet.

                        Format - Subnet, Name

  -o <filename>, --output_file <filename>
                        Specify a CSV output_file file.
```

### Check a Single IP against a Single Subnet

```shell
$ python3 ipcheck.py -i 192.168.1.210 -s 192.168.1.0/24
IP Address 192.168.1.210 found in 192.168.1.0/24 ( Inputted Address: 192.168.1.210 Inputted Subnet: 192.168.1.0/24 )
1 IP addresses processed.
```

### Input a list of IPs

```console
$ cat input.csv
192.168.1.0,Test1
192.168.1.1,Test2
192.168.1.2,Test3
192.168.1.136,Test1
192.168.1.176,Test2

$ python3 ipcheck.py -I input.csv -s 192.168.1.128/25
IP Address 192.168.1.0 NOT in 192.168.1.128/25 ( Inputted Address: 192.168.1.0 Inputted Subnet: 192.168.1.128/25 )
IP Address 192.168.1.1 NOT in 192.168.1.128/25 ( Inputted Address: 192.168.1.1 Inputted Subnet: 192.168.1.128/25 )
IP Address 192.168.1.2 NOT in 192.168.1.128/25 ( Inputted Address: 192.168.1.2 Inputted Subnet: 192.168.1.128/25 )
IP Address 192.168.1.136 found in 192.168.1.128/25 ( Inputted Address: 192.168.1.136 Inputted Subnet: 192.168.1.128/25 )
IP Address 192.168.1.176 found in 192.168.1.128/25 ( Inputted Address: 192.168.1.176 Inputted Subnet: 192.168.1.128/25 )
5 IP addresses processed.
```

### Output to a CSV File

```console
$ cat subnets.csv
192.168.1.128/25,TestSub

$ python3 ipcheck.py -i 192.168.1.210 -S subnets.csv -o output.csv
1 IP addresses processed.

Results saved to output.csv

$ cat output.csv
IP Address,IP Name,Subnet,Subnet Name,Inputted Address,Inputted Subnet
192.168.1.210,,192.168.1.128/25,TestSub,192.168.1.210,192.168.1.128/25
```

### Works on a Single IP

```console
$ python3 ipcheck.py -i 192.168.1.210 -s 192.168.1.0
IP Address 192.168.1.210 NOT in 192.168.1.0/32 ( Inputted Address: 192.168.1.210 Inputted Subnet: 192.168.1.0 )
1 IP addresses processed.
```

### Works in Reverse

```console
$ python3 ipcheck.py -i 192.168.1.208/30 -s 192.168.1.210
IP Address 192.168.1.208 NOT in 192.168.1.210/32 ( Inputted Address: 192.168.1.208/30 Inputted Subnet: 192.168.1.210 )
IP Address 192.168.1.209 NOT in 192.168.1.210/32 ( Inputted Address: 192.168.1.208/30 Inputted Subnet: 192.168.1.210 )
IP Address 192.168.1.210 found in 192.168.1.210/32 ( Inputted Address: 192.168.1.208/30 Inputted Subnet: 192.168.1.210 )
IP Address 192.168.1.211 NOT in 192.168.1.210/32 ( Inputted Address: 192.168.1.208/30 Inputted Subnet: 192.168.1.210 )
4 IP addresses processed.
```