import json
from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef, XSD, SDO

# read coopcycle.json file
with open('coopcycle.json') as json_file:
    data = json.load(json_file)
    
    
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
            
    
output_text = g.serialize(format='turtle')

with open('coopcycle.ttl', 'w') as f:
    f.write(output_text)

