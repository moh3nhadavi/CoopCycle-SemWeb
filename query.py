from datetime import datetime
from global_functions import *

def run_query(**kwargs):
    if kwargs.get('datetime'):
        day_of_week, time_24_hours = convert_iso8601_to_day_time(kwargs.get('datetime'))
        query = f"""
            {FUSEKI_SPARQL_PREFIXES_PREFIXES}
            SELECT DISTINCT ?name
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
        print(f"{bcolors.BOLD}Restaurants open at {kwargs.get('datetime')}: {bcolors.ENDC}")
        print(f"{bcolors.OKBLUE}{items}{bcolors.ENDC}")
        print(f"{bcolors.UNDERLINE}{bcolors.HEADER}Total: {len(items)}{bcolors.ENDC}")
        # print(len(items))
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
