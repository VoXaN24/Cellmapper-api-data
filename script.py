import re
import subprocess
import requests
import math

proxy=[]
#Utilisation de MullVad comme Proxy (Nécéssite un abonement + être connecter au VPN)
def ping_ip(ip):
    try:
        result = subprocess.run(['ping', "-c", "1", "-W", "1", ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.returncode == 0
    except Exception as e:
        return False
def download_proxy(url):
    response=requests.get(url)
    return response.text.splitlines()

def get_mullvad_proxy():
    lines=download_proxy("https://raw.githubusercontent.com/maximko/mullvad-socks-list/list/socks-ipv4_in-list.txt")
    print(f"Récupération des Proxy MullVad")
    print(f"Nombre de Proxy MullVad trouvé: {len(lines)}")
    print(f"Vérification de la disponibilité des Proxy MullVad")
    ip_pattern=re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')
    ips=[]
    for line in lines:
        match = ip_pattern.search(line)
        if match:
            ip = match.group()
            print(f"Vérification de {ip}")
            if ping_ip(ip):
                ips.append(ip+":1080")
    print(f"Proxy MullVad trouvé: {ips}")
    return ips

def get_perso_proxy():
    print(f"Le fichiers doit contenir 1 IP par ligne, et doit être accésible directement via une URL (Vous pouvez utiliser https://litterbox.catbox.moe/ pour heberger temporairement la liste)\n UNIQUEMENT DES SOCKS5 PROXY")
    lines=download_proxy(input("URL du fichier\n"))
    print(f"Vérification de la disponibilité des Proxy Personnalisé")
    ips=[]
    for line in lines:
        if ping_ip(line.split(":")[0]):
            ips.append(line)
    print(f"Proxy Personnalisé trouvé: {ips}")
    return ips

def get_public_proxy():
    lines=download_proxy("https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks5.txt")
    lines2=download_proxy("https://github.com/monosans/proxy-list/raw/main/proxies/socks5.txt")
    print(f"Récupération des Proxy Publique")
    print(f"Nombre de Proxy Publique trouvé: {len(lines)+len(lines2)}")
    for proxy in lines2:
        if proxy not in lines:
            lines.append(proxy)
    print(f"Vérification de la disponibilité des Proxy Publique")
    ips=[]
    for line in lines:
        if ping_ip(line.split(":")[0]):
            ips.append(line)
    print(f"Proxy Publique trouvé: {ips}")
    return ips

def menu_choose_proxy():
    print("|"+"-"*22+"|")
    print(f"|1 - Proxy MullVad     |")
    print(f"|2 - Proxy Publique    |")
    print(f"|3 - Proxy Personnalisé |")
    print("|"+"-"*22+"|")

def choose_proxy():
    choix=0
    while choix != "1" and choix != "2" and choix != "3":
        print(menu_choose_proxy())
        choix=input("\n")
    if choix == "1":
        return get_mullvad_proxy()
    elif choix == "2":
        return get_public_proxy()
    elif choix == "3": 
        return get_perso_proxy()

def get_proxy():
    return choose_proxy()

def get_coordonates():
    latNE=input("Latitude NE: ")
    longNE=input("Longitude NE: ")
    latSW=input("Latitude SW: ")
    longSW=input("Longitude SW: ")
    return latNE,longNE,latSW,longSW

def get_network_data():
    mmc=input("MMC: ")
    mnc=input("MNC: ")
    print("Type de réseau: ")
    print("0 - GSM")
    print("1 - 3G/UMTS/HSPA")
    print("2 - LTE")
    print("3 - NR")
    network_type=input()
    return mmc,mnc,network_type

def get_data(latNE,longNE,latSW,longSW,mmc,mnc,network_type):
    if network_type == "0":
        nt="GSM"
    elif network_type == "1":
        nt="UMTS"
    elif network_type == "2":
        nt="LTE"
    elif network_type == "3":
        nt="NR"
    url=f"https://api.cellmapper.net/v6/getTowers?MCC={mmc}&MNC={mnc}&RAT={nt}&boundsNELatitude={latNE}&boundsNELongitude={longNE}&boundsSWLatitude={latSW}&boundsSWLongitude={longSW}&filterFrequency=false&showOnlyMine=false&showUnverifiedOnly=false&showENDCOnly=false"
    prox=proxy[math.random(0,len(proxy))]
    response=requests.get(url,proxies={"https":prox})
    return response.text
    
    

def main():
    print("Choix du Proxy")
    proxy=choose_proxy()
    print("Choix des coordonnées")
    latNE,longNE,latSW,longSW=get_coordonates()
    print("Choix du réseau + Type de réseau")

if __name__ == "__main__":
    main()