import json
with open("country_name.txt", "r") as file:
    country_name_list = file.read().splitlines()
# Load data from file
with open('temp_json.json', 'r') as file:
    data = json.load(file)

def modify_provider_name(name):
    # Example modification: Replace numbers with the word 'Num'
    print(f"Modifying name: {name}")
    print(f"Do you want to modify this name? (y/n)")
    response = input()
    if response.lower() == 'y':
        modified_name = input("Enter the modified name: ")
    else:
        modified_name = name
    return modified_name

def generate_network_inserts(country_name, contry_code):
      
    # Ensure the country exists in the data
    if country_name in data['responseData']:
        providers = data['responseData'][country_name]
        
        for provider in providers:
            name = provider['providerName']
            
            # Modify name if it contains numbers
            if any(char.isdigit() for char in name):
                name = modify_provider_name(name)
            
            mmc = provider['countryID']
            mnc = provider['providerID']
            
            list_of_networks.append(
                f'INSERT INTO mmcmnc_cellmapper (country_code, network_name, mmc, mnc) VALUES ("{country_code}", "{name}", {mmc}, {mnc});'
            )
    else:
        print(f"No data available for country: {country_name}")
        no_data.append(country_name)
    
    return list_of_networks

# Example usage
no_data = []
list_of_networks = []
for i in range(len(country_name_list)):
    print(f"Processing country: {country_name_list[i].split(".")[0]}")
    country_name = country_name_list[i].split(".")[0]  # Replace with the country you want to process
    country_code = country_name_list[i].split(".")[1].strip() # Replace with the country code
    network_inserts = generate_network_inserts(country_name, country_code)
# Print the results
for insert_statement in network_inserts:
    print(insert_statement)
input("Press Enter to exit...")
print(f"No data available for the following countries: {no_data}")