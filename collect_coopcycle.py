from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef, XSD, SDO
import requests
from global_functions import *
    
turtle_file_name = 'coopcycle.ttl'
# fuseki_update_endpoint = 'http://localhost:3030/coopcycle/update'
# fuseki_sparql_prefixes = 

 


def create_graph_from_json(data):
    # Create a Graph
    g = Graph()

    for item in data:
        # print(item['country'])
        # items of every object
        name = item['name']
        uri_name = URIRef(name.replace(" ", "_"))
        latitude = item['latitude']
        longitude = item['longitude']
        city = item['city']
        country = item['country']
        
        g.add((uri_name, RDF.type, SDO.ProfessionalService))
        g.add((uri_name, SDO.name, Literal(name)))
        
        b_address = BNode()
        g.add((uri_name, SDO.address, b_address))
        g.add((b_address, SDO.addressLocality, Literal(city)))
        g.add((b_address, SDO.addressCountry, Literal(country)))
        
        b_geo = BNode()
        g.add((uri_name, SDO.geo, b_geo))
        g.add((b_geo, SDO.latitude, Literal(latitude, datatype=XSD.decimal)))
        g.add((b_geo, SDO.longitude, Literal(longitude, datatype=XSD.decimal)))
        
        
        
        # items for some objects
        url = item['url'] if 'url' in item else None
        if url:
            g.add((uri_name, SDO.url, Literal(url)))
            
        facebook_url = item['facebook_url'] if 'facebook_url' in item else None
        if facebook_url:
            g.add((uri_name, SDO.sameAs, Literal(facebook_url)))
            
        twitter_url = item['twitter_url'] if 'twitter_url' in item else None
        if twitter_url:
            g.add((uri_name, SDO.sameAs, Literal(twitter_url)))
        
        coopcycle_url = item['coopcycle_url'] if 'coopcycle_url' in item else None
        if coopcycle_url:
            g.add((uri_name, SDO.sameAs, Literal(coopcycle_url)))
            
        description = item['text'] if 'text' in item else None
        if description:
            for index,item in description.items():
                g.add((uri_name, SDO.description, Literal(item, lang=index)))
            
    return g

def serialize_graph_and_save(g, file_name):
    output_text = g.serialize(format='turtle')
    with open(file_name, 'w') as f:
        f.write(output_text)
    return output_text

def delete_old_data_from_fuseki():
    sparql_update_query = f'''
        CLEAR ALL
    '''
    # Send the SPARQL Update query to Fuseki
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post(FUESKI_UPDATE_ENDPOINT, data={"update":sparql_update_query}, headers=headers)
    if response.status_code == 200:
        print("Data deleted successfully from Fuseki.")
    else:
        print(f"Error: {response.status_code}\n{response.text}")


def collect_data():
    data = read_json_file(COOPCYCLE_JSON_FILE)
    graph = create_graph_from_json(data)
    output_text = serialize_graph_and_save(graph, turtle_file_name)
    # Temperory: delete old data from Fuseki
    delete_old_data_from_fuseki()
    # Publish new data to Fuseki
    publish_graph_to_fuseki(output_text)