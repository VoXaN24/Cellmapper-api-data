list_of_networks=[]
def add_new():
    try:
        country_code=input("Enter country code: ")
        name=input("Enter network name: ")
        mnc=int(input("Enter MNC: "))
        mmc=int(input("Enter MMC: "))
        list_of_networks.append(f'INSERT INTO mmcmnc_cellmapper (country_code, network_name, mnc, mmc) VALUES ("{country_code}", "{name}", {mnc}, {mmc});')
        add_new()
    except:
        print("Invalid input")
        for i in range(len(list_of_networks)):
            print(list_of_networks[i])

add_new()