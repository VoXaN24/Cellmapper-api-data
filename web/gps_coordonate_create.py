list_gps = []
def create_list_gps_coordonates():
    try :
        country = input("Enter the country abv : ")
        latitude = float(input("Enter the latitude : "))
        longitude = float(input("Enter the longitude : "))
        list_gps.append(f'INSERT INTO "main"."gps" ("country", "lat", "long") VALUES ("{country}", {latitude}, {longitude});')
        create_list_gps_coordonates()
    except ValueError:
        print("Unvalid value")
        for i in list_gps:
            print(i)
create_list_gps_coordonates()