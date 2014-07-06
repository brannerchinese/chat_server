#!/usr/bin/env python
# Foundations of Python Network Programming - Chapter 4
# dns_mx.py
# Looking up a mail domain - the part of an email address after the `@`
# Converted to Python3 by David Branner, 20140706, works.

import sys, DNS

if len(sys.argv) != 2:
    sys.stderr.write('usage: dns_basic.py <hostname>')
    sys.exit(2)

def resolve_hostname(hostname, indent=0):
    """Print an A or AAAA record for `hostname`; follow CNAMEs if necessary."""
    indent = indent + 4
    istr='' * indent
    request = DNS.Request()
    reply = request.req(name=sys.argv[1], qtype=DNS.Type.A)
    if reply.answers:
        for answer in reply.answers:
            print('{} Hostname {} = A {}'.
                    format(istr, hostname, answer['data']))
        return
    reply = request.req(name=sys.argv[1], qtype=DNS.Type.AAAA)
    if reply.answers:
        for answer in reply.answers:
            print('{} Hostname {} = AAAA {}'.
                    format(istr, hostname, answer['data']))
        return
    reply = request.req(name=sys.argv[1], qtype=DNS.Type.CNAME)
    if reply.answers:
        cname = reply.answers[0]['data']
        print('{} Hostname {} is an alias for {}'.format(istr, hostname, cname))
        resolve_hostname(cname, indent)
        return
    print('{} ERROR: no records for {}'.format(istr, hostname))

def resolve_email_domain(domain):
    """Print mail server IP addresses for an email address @ `domain`."""
    request = DNS.Request()
    reply = request.req(name=sys.argv[1], qtype=DNS.Type.MX)
    if reply.answers:
        print('The domain {} has explicit MX records!'.format(domain))
        print('Try the servers in this order:')
        datalist = [answer['data'] for answer in reply.answers]
        datalist.sort() # lower-priority integers go first
        for data in datalist:
            priority = data[0]
            hostname = data[1]
            print('Priority: {} Hostname: {}'.format(priority, hostname))
            resolve_hostname(hostname)
    else:
        print('Drat, this domain has no explicit MX records')
        print('We will have to try resolving it as an A, AAAA, or CNAME')
        resolve_hostname(domain)

DNS.DiscoverNameServers()
resolve_email_domain(sys.argv[1])