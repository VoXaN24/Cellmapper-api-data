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

def get_perso_proxy():
    print(f"Le fichiers doit contenir 1 IP par ligne, et doit être accésible directement via une URL (Vous pouvez utiliser https://litterbox.catbox.moe/ pour heberger temporairement la liste)\n")
    url=input("URL du fichier\n")
    response^=requests.get(url)
    lines=response.text.splitlines()
    ips=[]
    for line in lines:
        if ping_ip(line):
            ips.append(line)
    return ips

def menu_choose_proxy():
    print("|"+"-"*22+"|")
    print(f"|1 - Proxy MullVad     |")
    print(f"|2 - Proxy Publique    |")
    print(f"|3- Proxy Personnalisé |")
    print("|"+"-"*22+"|")

def choose_proxy():
    choix=0
    while choix != "1" and choix != "2" and choix != "3":
        print(menu_choose_proxy())
        choix=input("\n")
    if choix == "1":
        return get_mullvad_proxy()
    elif choix == "2":
        return get_public_proxy() #Non implémentais
    elif choix == "3":
        return get_perso_proxy()
print(choose_proxy())