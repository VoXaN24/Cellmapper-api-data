list_of_networks=[]
def add_new():
    try:
        country_code=input("Enter country code: ")
        name=input("Enter network name: ")
        mmc=int(input("Enter MMC: "))
        mnc=int(input("Enter MNC: "))
        list_of_networks.append(f'INSERT INTO mmcmnc_cellmapper (country_code, network_name, mmc, mnc) VALUES ("{country_code}", "{name}", {mmc}, {mnc});')
        add_new()
    except:
        print("Invalid input")
        for i in range(len(list_of_networks)):
            print(list_of_networks[i])

add_new()