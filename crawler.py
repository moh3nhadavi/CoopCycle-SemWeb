import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json

from rdflib import Graph

def crawl_and_process_urls(url_list):
    for url in url_list:
        try:
            # Fetch the HTML content of the URL
            response = requests.get(url)
            response.raise_for_status()

            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find all "a" tags with the property "data-restaurant-path"
            restaurant_tags = soup.find_all('a', {'data-restaurant-path': True})

            for restaurant_tag in restaurant_tags:
                # print(restaurant_tag)
                # Extract the href value and append it to the original URL
                restaurant_url = urljoin(url, restaurant_tag['href'])
                print(restaurant_url)
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

                    # Run your function on the JSON data
                    process_json_data(json_data)
                    return

        except requests.exceptions.RequestException as e:
            print(f"Error fetching or parsing content from {url}: {e}")

def process_json_data(json_data):
    # clean data
    json_data = json_data.replace("\\r\\n", "\\n")
    json_data = json.loads(json_data)
    replace_value(json_data, "@id", "https://beefast.coopcycle.org")
    json_ld_to_rdf(json_data)

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

def json_ld_to_rdf(json_ld_data):    
    g = Graph()

    g.parse(data=json_ld_data, format="json-ld")
    output_text = g.serialize(format="turtle")
    # clean prefix
    output_text = output_text.replace("schema1", "schema")
    with open('test.ttl', 'w') as f:
        f.write(output_text)
    



# Example usage with a list of URLs
url_list = ["https://beefast.coopcycle.org"]
crawl_and_process_urls(url_list)
