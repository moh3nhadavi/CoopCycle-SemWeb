import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
from global_functions import *
from rdflib import Graph
from pyshacl import validate


added_restaurants = []
checked_services = []
services_to_check = []
g = Graph()


def crawl_and_process_urls(url):
    try:
        # Fetch the HTML content of the URL
        response = requests.get(url)
        response.raise_for_status()

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all "a" tags with the property "data-restaurant-path"
        restaurant_tags = soup.find_all('a', {'data-restaurant-path': True})

        for restaurant_tag in restaurant_tags:
            # Extract the href value and append it to the original URL
            restaurant_url = urljoin(url, restaurant_tag['href'])
        
            # Fetch the HTML content of the new URL
            restaurant_response = requests.get(restaurant_url)
            restaurant_response.raise_for_status()

            # Parse the HTML content of the restaurant page
            restaurant_soup = BeautifulSoup(restaurant_response.content, 'html.parser')

            # Find the script tag with type "application/ld+json"
            script_tag = restaurant_soup.find('script', {'type': 'application/ld+json'})

            if script_tag:
                # Extract the JSON content from the script tag
                json_data = str(script_tag.string)
                if "nsfnvmsfvnsgfbvn" not in json_data:
                # Run your function on the JSON data
                    process_json_data(json_data, url)
                

    except requests.exceptions.RequestException as e:
        print(f"Error fetching or parsing content from {url}: {e}")

def process_json_data(json_data, url):
    global g
    
    # clean data
    json_data = json_data.replace("\\r\\n", "\\n")
    json_data = json.loads(json_data)
    
    # clean the subject tag (replace file:// with the base url) 
    replace_value(json_data, "@id", url)
    
    # check the @type is Restaurant
    if json_data['@id'] not in added_restaurants and json_data['@type'] == 'http://schema.org/Restaurant':
        # add triples to graph
        g.parse(data=json_data, format="json-ld")
        added_restaurants.append(json_data['@id'])
        write_json_file(ADDED_RESTAURANTS_FILE, added_restaurants)
        # print("added restaurant: ")
        print(json_data['@id'])
            

def check_validation(json_data):
    shacl = Graph().parse('shacl.ttl', format='turtle')
    g_temp = Graph()
    g_temp.parse(data=json_data, format="json-ld")
    valid, results_graph, results_text = validate(
        g_temp.serialize(format="turtle"), shacl_graph=shacl)
    if valid:
        return True
    else:
        print("shacl validation error: ")
        print(results_text)
        return False
    
    

def replace_value(json_obj, key_to_replace, new_value):
    if isinstance(json_obj, dict):
        for key, value in json_obj.items():
            if key == key_to_replace:
                json_obj[key] = urljoin(new_value, value)
            else:
                replace_value(value, key_to_replace, new_value)
    elif isinstance(json_obj, list):
        for item in json_obj:
            replace_value(item, key_to_replace, new_value)    
    



def store_data():
    
    global added_restaurants, checked_services, services_to_check
    
    # read json file
    delivery_services = read_json_file(COOPCYCLE_JSON_FILE)
    checked_services = read_json_file(CHECKED_SERVICES_FILE)
    services_to_check = read_json_file(SERVICES_TO_CHECK_FILE)
    added_restaurants = read_json_file(ADDED_RESTAURANTS_FILE)
    # for loop in json file
    for delivery_service in delivery_services:
        # if service is not checked
        if delivery_service['name'] in services_to_check and delivery_service['name'] not in checked_services:
            # crawl
            crawl_and_process_urls(delivery_service['coopcycle_url'])
            # finished crawling, add service to checked_services
            checked_services.append(delivery_service['name'])
            write_json_file(CHECKED_SERVICES_FILE, checked_services)
            
    global g 
    output_text = g.serialize(format="turtle")
    # clean prefix
    output_text = output_text.replace("schema1", "schema")
    publish_graph_to_fuseki(output_text)
            

