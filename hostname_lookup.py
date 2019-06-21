#!/usr/bin/python3

# Copyright 2019 Wes Moskal-Fitzpatrick
# Licensed under Apache Version 2.0

queryStart = "search Host where name matches regex '(?i)^("
queryEnd = ")$'"

with open('hosts.txt') as file:
    for line in file:
        queryStart += line.strip("\n") + "|"

queryStart = queryStart[:-1]
print ("\n" + queryStart + queryEnd + "\n")
