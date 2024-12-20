import re
import subprocess
import requests
import math
import json

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

def get_adress(lat,lon):
    url = f'https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}' #Use OpenStreetMap API
    response = requests.get(url)
    data = response.json()
    adr=f""
    if 'house_number' in data['address']:
        adr+=data["address"]["house_number"]+', '
    if 'road' in data['address']:
        adr+=data["address"]["road"]+', '
    if 'isolated_dwelling' in data['address']:
        adr+=data["address"]["isolated_dwelling"]+', '
    if 'village' in data['address']:
        if 'city' in data['address']:
            if data['address']["city"] != data["address"]["village"]:
                adr+=data["address"]["village"]+', '
    if 'postcode' in data["address"]:
        adr+=data["address"]["postcode"]+' '
    if 'city' in data['address']:
        adr+=data['address']['city']+', '
    return adr
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
    return response.json()

def check_data_hasmore(data):
    if "hasmore" in data:
        return True
    else:
        return False

def band_converter_LTE(band_nb):
    band = {"-1": "Unk band","1": "2100Mhz B1","2": "1900Mhz B2","3": "1800Mhz B3","4": "1700Mhz B4","5": "850Mhz B5","7": "2600Mhz B7","8": "900Mhz B8","11": "1500Mhz B11","12": "700Mhz B12","13": "700Mhz B13","14": "700Mhz B14","17": "700Mhz B17","18": "850Mhz B18","19": "850Mhz B19","20": "800Mhz B20","21": "1500Mhz B21","24": "1600Mhz B24","25": "1900Mhz B25","26": "850Mhz B26","28": "700Mhz B28","29": "700Mhz B29","30": "2300Mhz B30","31": "450Mhz B31","32": "1500Mhz B32","34": "2000Mhz B34","37": "1900Mhz B37","38": "2600Mhz B38","39": "1900Mhz B39","40": "2300Mhz B40","41": "2500Mhz B41","42": "3500Mhz B42","43": "3700Mhz B43","46": "5200Mhz B46","47": "5900Mhz B47","48": "3500Mhz B48","50": "1500Mhz B50","51": "1500Mhz B51","53": "2400Mhz B53","54": "1600Mhz B54","65": "2100Mhz B65","66": "1700Mhz B66","67": "700Mhz B67","69": "2600Mhz B69","70": "1700Mhz B70","71": "600Mhz B71","72": "450Mhz B72","73": "450Mhz B73","74": "1500Mhz B74","75": "1500Mhz B75","76": "1500Mhz B76","85": "700Mhz B85","87": "410Mhz B87","88": "410Mhz B88","103": "700Mhz B103","106": "900Mhz B106","107": "600Mhz B107","108": "500Mhz B108",}
    return band.get(band_nb,"Unkown band")

def band_converter_UMTS(band_nb):
    band ={"-1": "Unk band","1": "2100Mhz B1","2": "1900Mhz B2","3": "1800Mhz B3","4": "1700Mhz B4","5": "850Mhz B5","6": "800Mhz B6","7": "2600Mhz B7","8": "900Mhz B8","9": "900Mhz B9","10": "1700Mhz B10","11": "1500Mhz B11","12": "700Mhz B12","13": "700Mhz B13","14": "700Mhz B14","19": "800Mhz B19","20": "800Mhz B20","21": "1500Mhz B21","22": "3500Mhz B22","25": "1900Mhz B25","26": "850Mhz B26","32": "1500Mhz B32",}
    return band.get(band_nb,"Unkown band")

def band_converter_GSM(band_nb):
    band={"-1": "Unk band", "380": "T-GSM-380","410": "T-GSM-410","450": "GSM-450","480": "GSM-480","710": "E-GSM-710","750": "E-GSM-750", "810": "R-GSM-810","850": "GSM-850","900": "GSM-900","875": "E-GSM-875","1800": "DCS-1800","1900": "GSM-1900",}
    return band.get(band_nb,"Unkown band")

def band_converter_NR(band_nb):
    band={"-1": "Unk band","1": "2100Mhz n1 FDD","2": "1900Mhz n2 FDD","3": "1800Mhz n3 FDD","5": "850Mhz n5 FDD","7": "2600Mhz n7 FDD","8": "900Mhz n8 FDD","12": "700Mhz n12 FDD","13": "700Mhz n13 FDD","14": "700Mhz n14 FDD","18": "850Mhz n18 FDD","20": "800Mhz n20 FDD","24": "1600Mhz n24 FDD","25": "1900Mhz n25 FDD","26": "850Mhz n26 FDD","28": "700Mhz n28 FDD","29": "700Mhz n29 SDL","30": "2300Mhz n30 FDD","31": "450Mhz n31 FDD","34": "2100Mhz n34 TDD","38": "2600Mhz n38 TDD","39": "1900Mhz n39 TDD","40": "2300Mhz n40 TDD","41": "2500Mhz n41 TDD","46": "5200Mhz n46 TDD","47": "5900Mhz n47 TDD","48": "3600Mhz n48 TDD","50": "1500Mhz n50 TDD","51": "1500Mhz n51 TDD","53": "2400Mhz n53 TDD","54": "1600Mhz n54 TDD","65": "2100Mhz n65 FDD","66": "1700Mhz/2100Mhz n66 FDD","67": "700Mhz n67 SDL","70": "1700Mhz n70 FDD","71": "600Mhz n71 FDD","72": "450Mhz n72 FDD","74": "1500Mhz n74 FDD","75": "1500Mhz n75 SDL","76": "1500Mhz n76 SDL","77": "3700Mhz n77 TDD","78": "3500Mhz n78 TDD","79": "4900Mhz n79 TDD","80": "1800Mhz n80 SUL","81": "900Mhz n81 SUL","82": "800Mhz n82 SUL","83": "700Mhz n83 SUL","84": "2100Mhz n84 SUL","85": "700Mhz n85 FDD","86": "1700Mhz n86 SUL", "89": "700Mhz n89 SUL","90": "2500Mhz n90 TDD","91": "800/1500Mhz n91 FDD","92": "800/1500Mhz n92 FDD","93": "900/1500Mhz n93 FDD","94": "900/1500Mhz n94 FDD","95": "2100Mhz n95 SUL","96": "6000Mhz n96 TDD","97": "2300Mhz n97 SUL","98": "1900Mhz n98 SUL","99": "1600Mhz n99 SUL","100": "900Mhz n100 FDD","101": "1900Mhz n101 FDD","102": "6200Mhz n102 FDD","104": "6700Mhz n104 FDD","105": "600Mhz n105 FDD","106": "900Mhz n106 FDD","109": "700/1500Mhz n109 FDD","257": "28Ghz n257 LMDS","258": "26Ghz n258 K-band","259": "41Ghz n259 V-band","260": "39Ghz n260 Ka-band", "261": "28Ghz n261 Ka-band", "262": "47Ghz n262 V-band","263": "60Ghz n263 V-band","254": "2400Mhz n254 FDD","255": "1600Mhz n255 FDD","256": "2100Mhz n256 FDD","510": "28Ghz n510 FDD","511": "28Ghz n511 FDD","512": "28Ghz n512 FDD",}
    return band.get(band_nb,"Unkown band")

def reduce_ratio(ratio):
    return ratio/2

def main():
    print("Choix du Proxy")
    proxy=choose_proxy()
    print("Choix des coordonnées")
    latNE,longNE,latSW,longSW=get_coordonates()
    print("Choix du réseau + Type de réseau")

if __name__ == "__main__":
    main()
