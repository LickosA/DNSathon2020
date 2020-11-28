from flask import Flask, jsonify, request
from api import *

app = Flask(__name__)



@app.route('/api/audit/<domain>', methods=['GET'])
def audit(domain):

    if check_if_dns_exist(domain):
        check_ns(domain)
        check_soa(domain)
        check_mx(domain)
        check_ipv6(domain)

        check_dnssec(domain)
        check_ssl(domain)

        edns_tests_full(domain)
        get_performance(domain)

        return jsonify(infos)
    else:
        return jsonify({
            'EXIST': False
        })





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
    app.run(debug=True,  port=5555)