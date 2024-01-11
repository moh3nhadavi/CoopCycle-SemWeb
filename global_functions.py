import json, requests

COOPCYCLE_JSON_FILE = 'coopcycle.json'
CHECKED_SERVICES_FILE = 'checked_services.json'
SERVICES_TO_CHECK_FILE = 'services_to_check.json'
ADDED_RESTAURANTS_FILE = 'added_restaurants.json'

# FUESKI_UPDATE_ENDPOINT = 'http://localhost:3030/coopcycle/update'
FUESKI_UPDATE_ENDPOINT = 'http://localhost:3030/coop/update'
# FUSEKI_QUERY_ENDPOINT = 'http://localhost:3030/coopcycle/query'
FUSEKI_QUERY_ENDPOINT = 'http://localhost:3030/coop/query'
FUSEKI_SPARQL_PREFIXES_PREFIXES = f'''
    PREFIX schema: <https://schema.org/>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
    PREFIX sh: <http://www.w3.org/ns/shacl#>
'''

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
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
        

def run_sparql_query(query):
    # Define the headers for the HTTP request
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
    }

    # Define the parameters for the HTTP request
    params = {
        'query': query,
        'format': 'json',
    }

    # Send the HTTP request to the Fuseki server
    try:
        response = requests.get(FUSEKI_QUERY_ENDPOINT, headers=headers, params=params)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            print(f"{bcolors.OKGREEN}Data retrieved successfully from Fuseki.{bcolors.ENDC}")
            return response.json()

        else:
            print(f"{bcolors.FAIL}Error executing SPARQL query. Status code: {response.status_code}{bcolors.ENDC}")
            print(response.text)

    except Exception as e:
        print(f"{bcolors.FAIL}Error executing SPARQL query: {e}{bcolors.ENDC}")
    