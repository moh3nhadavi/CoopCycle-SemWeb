import json, requests

COOPCYCLE_JSON_FILE = 'coopcycle.json'
CHECKED_SERVICES_FILE = 'checked_services.json'
SERVICES_TO_CHECK_FILE = 'services_to_check.json'
ADDED_RESTAURANTS_FILE = 'added_restaurants.json'

FUESKI_UPDATE_ENDPOINT = 'http://localhost:3030/coopcycle/update'
FUSEKI_SPARQL_PREFIXES_PREFIXES = f'''
    PREFIX schema: <https://schema.org/>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
'''

def read_json_file(file_name):
    with open(file_name) as json_file:
        data = json.load(json_file)
    return data


def write_json_file(file_name, data):
    with open(file_name, 'w') as json_file:
        json.dump(data, json_file, indent=4)
        
        
def publish_graph_to_fuseki(output_text):
    triples_data = '\n'.join(line for line in output_text.split('\n') if not line.startswith('@prefix'))
    sparql_update_query = f'''
        {FUSEKI_SPARQL_PREFIXES_PREFIXES}
        INSERT DATA {{
            {triples_data}
        }}
    '''
    # Send the SPARQL Update query to Fuseki
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post(FUESKI_UPDATE_ENDPOINT, data={"update":sparql_update_query}, headers=headers)
    if response.status_code == 200:
        print("Data added successfully to Fuseki.")
    else:
        print(f"Error: {response.status_code}\n{response.text}")
        
