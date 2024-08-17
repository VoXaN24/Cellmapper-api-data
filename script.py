import re
import subprocess
import requests

#Utilisation de MullVad comme Proxy (Nécéssite un abonement + être connecter au VPN)
def ping_ip(ip):
    try:
        result = subprocess.run(['ping', "-c", "1", "-W", "1", ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.returncode == 0
    except Exception as e:
        return False

def get_mullvad_proxy():
    url="https://raw.githubusercontent.com/maximko/mullvad-socks-list/list/socks-ipv4_in-list.txt"
    response=requests.get(url)
    lines=response.text.splitlines()
    ip_pattern=re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')
    ips=[]
    for line in lines:
        match = ip_pattern.search(line)
        if match:
            ip = match.group()
            if ping_ip(ip):
                ips.append(ip)

    return ips

print(get_mullvad_proxy())

