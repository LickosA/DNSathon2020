from flask import Flask, jsonify, request
import urllib.request
import sys
import dns.resolver
import socket
from cymruwhois import Client
import os
import re, socket, subprocess

app = Flask(__name__)
infos = {}

def checkSOA(host):
    try:
        answers = dns.resolver.resolve(host, 'SOA')
        soa = []
        soa_len = len(answers)
        for rdata in answers:
            soa.append(rdata.to_text())
        infos['INFO_SOA']['list'] = soa
        infos['INFO_SOA']['number'] = soa_len
    except Exception as e:
        infos['INFO_SOA'] = False
def checkMX(host):
    try:
        answers = dns.resolver.resolve(host,'MX')
        mx = []
        mx_len = len(answers)
        for rdata in answers:
           mx.append(rdata.to_text())

        infos['mx']['list'] = mx
        infos['mx']['number'] = mx_len
    except Exception as e:
        infos['mx'] = False

def check_ns(domain="gouv.bj"):
    result = dns.resolver.query(domain, 'NS')
    ns_len = len(result)
    ns = []
    for ipval in result:
        ns.append(ipval.to_text())
    infos['INFO_NS'] = {
        'list': ns,
        'number': ns_len,
    }
    if ns_len >= 2:
        asn = 0
        for name in ns:
            ip = socket.gethostbyname(name)
            c = Client()
            r = c.lookup(ip)

            if asn == 0:
                asn = r.asn
            elif asn != r.asn:
                infos['INFO_NS']['same_asn'] = False
            else:
                asn = r.asn
                infos['INFO_NS']['same_asn'] = True

# Define a function to resolver nameserver into ipv4.
def ns_resolver(ns: str) -> str:
    try:
        res = socket.getaddrinfo(ns, None, socket.AF_INET)[0][4][0]
    except Exception:
        res = 'Failed'
    return res

# Define a function to resolver nameserver into ipv6.
def ns_resolverV6(ns: str) -> str:
    try:
        res = socket.getaddrinfo(ns, None, socket.AF_INET6)[0][4][0]
    except Exception:
        res = 'Failed'
    return res

# Define the function to extract list of NS for each ccTLDs
def domain_ns_retrieval(domain: str) -> str:
    try:
        res = [ns.__str__() for ns in dns.resolver.query(domain + '.', 'NS')]
    except Exception:
        res = 'U'
    return res

# Define EDNS Tests list
edns_test_dict = {'dns_plain': ['dig', '+norec', '+noedns', 'soa'],
                  'edns_plain': ['dig', '+norec', '+edns=0', 'soa'],
                  'edns_dnssec': ['dig', '+norec', '+dnssec', 'soa'],
                  'edns_tcp': ['dig', '+norec', '+tcp', 'soa']}


# Define function to execute dig command
def run_dig_cmd(cmd: list, pkt_size=False, flag=False, aa_zone=None)  -> list:
    status = None
    edns_version = None
    pckt_size, flags, answer_section, rrsig = None, None, None, None
    result = subprocess.run(
        cmd, stdout=subprocess.PIPE).stdout.decode('utf-8').split(';;')
    for line in result:
        if re.search('RRSIG', line):
            rrsig = True
        if re.search('status:', line):
            status = line.split(',')[1].split(':')[1].strip()
        elif re.search('EDNS: version: 0', line):
            edns_version = 0
            if pkt_size:
                pckt_size = line.split('; ')[2].split(':')[1].replace(' ', '').replace('\n', '')  # Get the Maximum UDP packet size
            if flag:
                flags = line.split(';')[1].split(':')[3].replace('\n', '').split(' ')  # Get the flags
        elif aa_zone is not None and re.search('ANSWER SECTION', line):
            answer_section = True if re.search(aa_zone, line) else None  # Get the flags
    return status, edns_version, pckt_size, flags, answer_section, rrsig, result


# Define function to run tests on NS
def run_ednsComp_test(zone: str, ns: str):
    # Reset results vars
    dns_plain, edns_plain, edns_dnssec, edns_tcp = False, False, False, False
    packet_size = 0
    # Test DNS plain resolution first
    dns_plain = True if run_dig_cmd(edns_test_dict['dns_plain'] + [zone, '@' + ns], aa_zone=zone)[:-2] == ('NOERROR', None, None, None, True) else False
    if dns_plain:
        # Test EDNS plain resolution first
        edns_plain_test = run_dig_cmd(edns_test_dict['edns_plain'] + [zone, '@' + ns], pkt_size=True)[:-1]
        packet_size = edns_plain_test[2]
        edns_plain = True if edns_plain_test[:-1] == ('NOERROR', 0, packet_size, None, None) else False

        edns_dnssec_test = run_dig_cmd(edns_test_dict['edns_dnssec'] + [zone, '@' + ns], aa_zone=zone, flag=True)[:-1]
        try:
            if 'do' in edns_dnssec_test[3] and edns_dnssec_test[4] and edns_dnssec_test[5] and edns_dnssec_test[0:2] == ('NOERROR', 0):
                edns_dnssec = True
        except Exception:
            edns_dnssec = False

        edns_tcp = True if run_dig_cmd(edns_test_dict['edns_tcp'] + [zone, '@' + ns])[0:2] == ('NOERROR', 0) else False

    #t_results = [ns, dns_plain, edns_plain, edns_dnssec, edns_tcp, packet_size, zone]
    t_results = {'ZONE': zone, 'NAMESERVER': ns, 'DNS': dns_plain, 'EDNS': edns_plain,
                 'DNSSEC': edns_dnssec,'TCP': edns_tcp, 'PACKET_SIZE': packet_size,
                 'IPv4': ns_resolver(ns=ns), 'IPv6': ns_resolverV6(ns=ns)}
    return t_results


def edns_tests_full(domain: str, nameserver: str = None) -> list:
    all_results = []
    if nameserver is not None:
        results = run_ednsComp_test(zone=domain, ns=nameserver)
        all_results.append(results)
    else:
        nameservers = domain_ns_retrieval(domain=domain)
        for nameserver in nameservers:
            all_results.append(run_ednsComp_test(zone=domain, ns=nameserver))
    print(all_results)
    return all_results



@app.route('/api/audit/<domain>', methods=['GET'])
def test(domain):
    dnssec = os.popen(f"dig {domain} +dnssec @9.9.9.9|egrep -w '^flags|ad'|wc -l")
    dnssec = dnssec.read()

    if int(dnssec) == 0:
        infos['SEC_DNSSEC'] = False
    else:
        infos['SEC_DNSSEC'] = True

    ipv6 = os.popen(f"dig {domain} AAAA +short")
    ipv6 = ipv6.read()
    if ipv6 != " ":
        infos['INFO_IPV6'] = True
    else:
        infos['INFO_IPV6'] = False

    sys.stderr = open("/dev/null")
    result = sys.stderr = urllib.request.urlopen(f"http://www.{domain}").getcode()
    if result:
        infos['SEC_SSL'] = True
    else:
        infos['SEC_SSL'] = False


    check_ns(domain)
    #edns_tests_full(domain)
    # checkSOA(domain)
    # checkMX(domain)

    return jsonify(infos)





# def checkexistdnssec(domain):
#     val = os.popen(f"dig {domain} +dnssec|egrep -w '^flags|ad'|wc -l")
#     val = val.read()
#     if int(val) == 0:
#         return "DNSSEC Not EXIST"
#     else:
#         return "DNSSEC OK"
#
#
# def checkdnssecreccord(domain):
#     val = os.popen(f"dig DNSKEY {domain} +short|egrep -w '^flags|ad'|wc -l")
#     val = val.read()
#     if int(val) == 0:
#         return "No DNSKEY records found"
#     else:
#         return "DNSKEY reccord EXIST"


# def checktrustdnssec(domain):
#     val = os.popen(f"dig DS {domain} +trace|egrep -w '^flags|ad'|wc -l")
#     val = val.read()
#     if int(val) == 0:
#         return "No DS records found for {domain}"
#     else:
#         return "DS record found"


if __name__ == '__main__':
    app.run(debug=True, host="192.168.12.81", port=5555)