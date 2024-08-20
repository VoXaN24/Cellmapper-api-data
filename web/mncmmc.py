import json

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
    list_of_networks = []
    
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
    
    return list_of_networks

# Example usage
country_name = "Colombia"  # Replace with the country you want to process
country_code = "co"  # Replace with the country code
network_inserts = generate_network_inserts(country_name, country_code)

# Print the results
for insert_statement in network_inserts:
    print(insert_statement)
