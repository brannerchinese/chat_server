#!/usr/bin/env python
# Rhodes and Goerzen, Foundations of Python Network Programming - Chapter 4
# dns_basic.py
# Basic DNS query
# Converted to Python3 by David Branner, 20140706, works.

import sys, DNS

if len(sys.argv) != 2:
    sys.stderr.write('usage: dns_basic.py <hostname>')
    sys.exit(2)
DNS.DiscoverNameServers()
request = DNS.Request()
for qt in DNS.Type.A, DNS.Type.AAAA, DNS.Type.CNAME, DNS.Type.MX, DNS.Type.NS:
    reply = request.req(name=sys.argv[1], qtype=qt)
    for answer in reply.answers:
        print(answer['name'], answer['classstr'], answer['typename'], 
            repr(answer['data']))