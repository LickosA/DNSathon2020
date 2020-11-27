from flask import Flask, jsonify, request
import dns.resolver
import socket
from cymruwhois import Client
import os

app = Flask(__name__)


@app.route('/api/audit/<domain>', methods=['GET'])
def test(domain):
    infos = {}
    dnssec = os.popen(f"dig {domain} +dnssec|egrep -w '^flags|ad'|wc -l")
    dnssec = dnssec.read()

    if int(dnssec) == 0:
        infos['DNSSEC'] = "NOT EXIST"
    else:
        infos['DNSSEC'] = "EXIST"

    ipv6 = os.popen(f"dig {domain} AAAA +short")
    ipv6 = ipv6.read()
    if ipv6 != " ":
        infos['IPV6'] = "FOUND"
    else:
        infos['IPV6'] = "NOT FOUND"

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
    app.run(debug=True)