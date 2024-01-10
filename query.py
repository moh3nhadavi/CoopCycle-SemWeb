from datetime import datetime
from global_functions import *
from rich import print_json
from rich.table import Table
from rich.console import Console
import geopy.distance

def run_query(**kwargs):
    if kwargs.get('datetime'):
        day_of_week, time_24_hours = convert_iso8601_to_day_time(kwargs.get('datetime'))
        
        location = kwargs.get('location')
        price = kwargs.get('price')
        max_distance = kwargs.get('max_distance')
        location_select, price_select = "", ""
        price_filter = ""
        location_where, price_where = "", ""
        
        if location:
            latitude, longitude = location.split(',')
            
            location_select = f"""
                ?latitude ?longitude
            """
            location_where = f"""
                ?restaurant schema:address ?address.
                
                ?address    a schema:PostalAddress;
                            schema:geo ?baddress.
                ?baddress   a schema:GeoCoordinates;
                            schema:latitude ?latitude;
                            schema:longitude ?longitude.
            """
        
        if price:
            price_select = f"""
                ?price
            """
            price_filter = f"""
                FILTER (?price <= {price})
            """
            price_where = f"""
                ?potentialAction schema:priceSpecification/schema:priceCurrency "EUR" ;
                         schema:priceSpecification/schema:price ?price.
            """
        
        query = f"""
            {FUSEKI_SPARQL_PREFIXES_PREFIXES}
            SELECT DISTINCT ?restaurant ?name {location_select} {price_select}
            WHERE {{
            ?restaurant a schema:Restaurant;
                        schema:openingHoursSpecification ?openingHours;
                        schema:potentialAction ?potentialAction.
                        

            ?openingHours schema:opens ?opens;
                            schema:closes ?closes;
                            schema:dayOfWeek ?dayOfWeek.
            
            {location_where}
            {price_where}
            
            FILTER (
                ?dayOfWeek = "{day_of_week}" &&
                ?opens <= "{time_24_hours}" &&
                ?closes >= "{time_24_hours}"
            )
            {price_filter}
            OPTIONAL {{ ?restaurant schema:name ?name }}
            }}
        """
            
        items = run_sparql_query(query)
        
        if location:
            items = filter_by_location(items, float(latitude), float(longitude), max_distance)
            
                
        
    else:
        print(f"{bcolors.FAIL}Error: Please pass an argument at least{bcolors.ENDC}")
        return None
    
    title = f"Restaurants open at {kwargs.get('datetime')}"
    print_query_results(items, title)



def convert_iso8601_to_day_time(iso_datetime):
    try:
        # Parse ISO 8601 datetime string
        dt_object = datetime.fromisoformat(iso_datetime)
        
        # Extract day of the week (e.g., Monday, Tuesday, etc.)
        day_of_week = dt_object.strftime('%A')
        
        # Extract 24-hour time format (e.g., 10:30)
        time_24_hours = dt_object.strftime('%H:%M')
        
        return day_of_week, time_24_hours
    
    except ValueError as e:
        print(f"Error: {e}")
        return None, None


def print_query_results(items, title):
    # Process and print the results
    table = Table(show_header=True, header_style="bold magenta",title=title)
    # add columns
    keys = items["head"]["vars"]
    for key in keys:
        table.add_column(key)
        
    # add rows
    for result in items["results"]["bindings"]:
        row = []
        for key in keys:
            row.append(result[key]['value'])
        table.add_row(*row)
    
    # print table
    console = Console()
    console.print(table)
    
    print(f"{bcolors.UNDERLINE}{bcolors.HEADER}Total: {len(items['results']['bindings'])}{bcolors.ENDC}")
        
        
def calculate_distance(lat1, lon1, lat2, lon2):
    coords_1 = (lat1, lon1)
    coords_2 = (lat2, lon2) 
    return geopy.distance.distance(coords_1, coords_2).km


def filter_by_location(data, lat2, lon2, max_distance=None):
    filtered_data = []
    for entry in data["results"]["bindings"]:
        lat1 = float(entry["latitude"]["value"])
        lon1 = float(entry["longitude"]["value"])
        
        distance = calculate_distance(lat1, lon1, lat2, lon2)
        
        # Add distance key and remove lat1 and lon1
        entry["distance"] = {"type": "literal", "datatype": "http://www.w3.org/2001/XMLSchema#double", "value": str(distance)}
        del entry["latitude"]
        del entry["longitude"]
        
        # Filter out entries above max_distance
        if max_distance is None or distance <= float(max_distance):
            filtered_data.append(entry)
    
    # Replace "lat1" and "lon1" with "distance" in "vars" list
    data["head"]["vars"].remove("latitude")
    data["head"]["vars"].remove("longitude")
    data["head"]["vars"].append("distance")
    
    # Update bindings with filtered entries
    data["results"]["bindings"] = filtered_data
    
    return data