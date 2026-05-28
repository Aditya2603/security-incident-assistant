malicious_ips = [
    "185.220.101.1"
]
def ip_reputation(ip):

    if ip in malicious_ips:
        return "malicious"

    return "clean"