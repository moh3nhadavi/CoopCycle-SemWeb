from datetime import datetime
from global_functions import *
from rich import print_json
from rich.table import Table
from rich.console import Console

def run_query(**kwargs):
    if kwargs.get('datetime'):
        day_of_week, time_24_hours = convert_iso8601_to_day_time(kwargs.get('datetime'))
        query = f"""
            {FUSEKI_SPARQL_PREFIXES_PREFIXES}
            SELECT DISTINCT ?restaurant ?name
            WHERE {{
            ?restaurant a schema:Restaurant;
                        schema:openingHoursSpecification ?openingHours.

            ?openingHours schema:opens ?opens;
                            schema:closes ?closes;
                            schema:dayOfWeek ?dayOfWeek.
            FILTER (
                ?dayOfWeek = "{day_of_week}" &&
                ?opens <= "{time_24_hours}" &&
                ?closes >= "{time_24_hours}"
            )
            OPTIONAL {{ ?restaurant schema:name ?name }}
            }}
        """
        items = run_sparql_query(query)
        # Process and print the results
        table = Table(show_header=True, header_style="bold magenta",title=f"Restaurants open at {kwargs.get('datetime')}")
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
        
    else:
        print(f"{bcolors.FAIL}Error: Please pass an argument at least{bcolors.ENDC}")
        return None



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
