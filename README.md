# Semantic Web Project Report
**Group Members:** 
- Mohsen Hadavi 
- Alale Mohammadi Golrang


## Table of Contents

1. [Setup](#setup)

2. [How to Run the Program](#how-to-run-the-program)
    
3. [Collect CoopCycle Data](#collect-coopcycle-data)
    
4. [Collect Data](#collect-data)
    
5. [Query Data](#query-data)
    
6. [Describe User](#describe-user)



## Setup

Follow these steps to set up and configure the project:

1. **Install Virtual Environment:**

- Open a terminal or command prompt.
- Navigate to the project's root directory using the `cd` command. For example:

   ```bash
   cd path/to/project
   ```
- Run the following command to create a virtual environment. Replace the second `venv` with your preferred virtual environment name.
    -  For Windows:
        ```bash
        python -m venv venv
        ```
    -  For macOS/Linux:
        ```bash
        python3 -m venv venv
        ```
- Activate the virtual environment:
    -  For Windows:
        ```bash
        venv\Scripts\activate
        ```
    -  For macOS/Linux:
        ```bash
        source venv/bin/activate
        ```

    Once activated, you should see the virtual environment's name in your command prompt or terminal.
        

2. **Install Dependencies:**

   ```bash
   pip3 install -r requirements.txt
   ```

3. **Install and Run Jena Fuseki:**
    
    Download and install [Jena Fuseki](https://jena.apache.org/documentation/fuseki2/index.html). Start the server according to the documentation.

4. **Configure Database:**
- Open `global_functions.py`
- Update the database name in the following lines:
    ```python
    FUSEKI_UPDATE_ENDPOINT = 'http://localhost:3030/[DB_NAME]/update'
    FUSEKI_QUERY_ENDPOINT = 'http://localhost:3030/[DB_NAME]/query'
   ```
   Replace `[DB_NAME]` with your desired database name.

5. **Create JSON Files:**
- Create the following JSON files with their values in the project directory:
    - `services_to_check.json`
    ```json
    []
    ```
    - `added_restaurants.json`
    ```json
    []
    ```
    - `services_to_check.json`
    ```json
    [
        "Beefast",
        "Biclooo",
        "Chorlton Bike Deliveries",
        "CYCLOME",
        "Les Coursiers Dinannais",
        "Envici",
        "Eraman Repartos Gasteiz",
        "FACTTIC",
        "Feel à Vélo",
        "Hotline Couriers",
        "Hull Delivery Coop",
        "Kooglof",
        "Les Coursiers Rennais",
        "COCO Collectif de Coursiers Orléanais ",
        "Les Coursiers Bordelais",
        "Les Coursiers Brestois",
        "Les coursiers Metz",
        "Les Coursiers Montpelliérains",
        "Les Coursiers Nancéiens",
        "Les Coursiers Nantais",
        "Les Coursiers Stéphanois",
        "Wings: ethical food delivery",
        "Mensakas",
        "Naofood",
        "KroKoop",
        "Les Coursiers Niortais",
        "RAYON9",
        "Robin Food",
        "S!cklo",
        "Les Coliporteurs Nazairiens",
        "Samo",
        "SIRApps Unión Mexicana de Bicimensajeros por Aplicación",
        "Zampate",
        "Ziclo-P"
    ]
    ```

Now, the project is set up and configured for use.

## How to run the program

The `main.py` file uses Typer for command-line interface (CLI) functionality. To run the program with different parameters, you can use the following commands in the terminal or command prompt.

1. **Show Version:**
    ```bash
    python3 main.py --version
    ```
    This will display the version of the application.

2. [**Collect CoopCycle Data:**](#collect-coopcycle-data)
    ```bash
    python3 main.py collect_coopcycle
    ```
    This command will execute the `collect_coopcycle` function, collecting data from the CoopCycle JSON file and publishing them to the `Jena Fuseki` triple store.

3. [**Collect Data:**](#collect-data)
    ```bash
    python3 main.py collect
    ```
    This command will execute the `collect` function, to crawl through the web and collect data from different restaurants

4. [**Query Data:**](#query-data)
    
    ```bash
    python3 main.py query --datetime="2024-01-03T12:30:00" --location="2.3522,48.8566" --max-distance=10 --price=10 --rank-by=distance
    ```
    
    You can customize the parameters (datetime, location, max_distance, price, rank_by) based on your needs.

5. [**Describe User:**](#describe-user)
    ```bash
    python3 main.py describe
    ```
    his command will execute the `describe` function, asking some questions from user to create his/her prefrences and publish them to the [Linked Data Platform.](http://193.49.165.77:3000/semweb/)

> You can also use the --help option for each command to see more information about the available parameters:

```bash
python3 main.py collect_coopcycle --help
python3 main.py collect --help
python3 main.py query --help
python3 main.py describe --help
```


### Collect CoopCycle Data

This Python file focuses on collecting data from CoopCycle, converting it into RDF format, and storing it in a Turtle file. The collected data can be further analyzed or used for various purposes.

To collect data from CoopCycle and store it in a Turtle file and Jena Fuseki, use the following command:

```bash
python3 main.py collect_coopcycle
```

**What happens when you run this command?**

1. The script reads data from a CoopCycle JSON file (`COOPCYCLE_JSON_FILE`).
1. A new RDF graph is created from the JSON data.
1. RDF triples are generated for each CoopCycle entity, including name, location, URLs, and descriptions.
1. The RDF graph is serialized into Turtle format.
1. Old data is cleared from the Fuseki triplestore using the SPARQL query `CLEAR ALL`.
1. The new RDF data is saved to a Turtle file (`coopcycle.ttl`).
1. The updated data is published to Fuseki using the `publish_graph_to_fuseki` function.



### Collect Data 

This Python file focuses on collecting data from CoopCycle, converting it into RDF format, and storing it in a Turtle file. The collected data can be further analyzed or used for various purposes.

To collect data from CoopCycle and store it in the Jena Fuseki, use the following command:

```bash
python3 main.py collect
```

**What happens when you run this command?**

1. The script reads data from a CoopCycle JSON file (`COOPCYCLE_JSON_FILE`).
1. Reads lists of checked services, services to check, and added restaurants.
1. Iterates through delivery services in the CoopCycles.
1. Checks if a service needs to be checked and has not been checked before.
1. Crawls the CoopCycle page for the service and fetches restaurant URLs.
1. Processes each restaurant's HTML content, extracts JSON data, and runs the `process_json_data` function.
1. In `process_json_data`, JSON data is cleaned, the subject tag is modified, and validation against SHACL shapes is performed.
1. If the JSON data represents a restaurant, triples are added to the RDF graph (g).
1. Updated data is published to Fuseki using the `publish_graph_to_fuseki` function.
1. The script completes, and you can explore the triple store.



### Query Data

This Python script allows you to query CoopCycle data based on various parameters such as datetime, location, max_distance, price, and rank_by. Customize the parameters to tailor your query to specific needs.

To run a query, use the following command:

```bash
python3 main.py query
```

**Available Parameters:**
- `datetime`: ISO 8601 formatted datetime string (e.g., "2024-01-15T12:30:00").
- `location`: Latitude and longitude separated by a comma (e.g., "48.8566,2.3522").
- `max-distance`: Maximum distance (in kilometers) from the specified location.
- `price`: Maximum price for filtering restaurants.
- `rank-by`: Sorting option, either "price" or "distance".

**Example:**
```bash
python3 main.py query --datetime="2024-01-15T12:30:00" --location="48.8566,2.3522" --max_distance=5 --price=20 --rank-by=distance
```

**What Happens When You Run a Query?**
1. The script converts the provided datetime string into the day of the week and 24-hour time format.
1. Constructs a SPARQL query based on the given parameters.
1. Executes the query on the Fuseki server.
1. Filters and sorts the results based on location and/or price.
1. Prints the query results in a tabular format, including the total number of matching restaurants.


***More Details About This File:***

1. **`run_query(**kwargs)` function:**

    This function serves as the entry point for running a CoopCycle data query. It takes keyword arguments (**kwargs) representing the parameters for the query. Here's a breakdown of the significant components:

    - *Input Parameters*:
        - `datetime`: ISO 8601 formatted datetime string (e.g., "2024-01-15T12:30:00").
        - `location`: Latitude and longitude separated by a comma (e.g., "48.8566,2.3522").
        - `max-distance`: Maximum distance (in kilometers) from the specified location.
        - `price`: Maximum price for filtering restaurants.
        - `rank-by`: Sorting option, either "price" or "distance".

    - *Query Construction:*

        - Constructs a SPARQL query based on the provided parameters, including optional filtering and sorting clauses.

    - *Data Retrieval:*

        - Executes the SPARQL query on the Fuseki server using `run_sparql_query()`.

    - *Post-Processing:*

        - Filters and sorts the query results based on location and/or price.
        - Prints the formatted results using `print_query_results()`.

1. **`convert_iso8601_to_day_time(iso_datetime)` function:**

    This utility function converts an ISO 8601 formatted datetime string to the corresponding day of the week and 24-hour time format. It returns a tuple containing the day of the week and time.

1. **`print_query_results(items, title)` function:**

    Prints the query results in a tabular format using the Rich library. It creates a table with columns representing different variables and rows containing the data. The `title` parameter is used to set the title of the table.

1. **`calculate_distance(lat1, lon1, lat2, lon2)` function:**

    Calculates the distance between two sets of latitude and longitude coordinates using the geopy library.

1. **`filter_by_location(data, lat2, lon2, max_distance=None)` function:**

    Filters the query results based on the specified location and maximum distance. It calculates the distance for each restaurant and includes it in the results. If `max_distance` is provided, entries beyond this distance are filtered out.

1. **`sort_by_distance(data)` function:**

    Sorts the query results based on the calculated distance in ascending order.



### Describe User

The "describe" application is a Python script designed to interactively collect user preferences through a series of questions and publish this information to the [Linked Data Platform](http://193.49.165.77:3000/semweb/) (LDP) in RDF format. The collected data is serialized into Turtle format and stored in a file.

**Usage**

To run the "describe" application, execute the following command. The application will prompt you with a set of questions related to personal information, food preferences, and location details.

```bash
python3 main.py describe
```

**Questions Asked**

1. *Personal Information*

    - Full Name
    - Postal Code
    - Locality

1. *Food Preferences*

    - Restaurant URI
    - Maximum Delivery Price in EUR

1. *Location Information*

    - User's Location (longitude,latitude)
    - Maximum Distance

**RDF Representation**

The user's data is represented in RDF using the `rdflib` library. The RDF graph includes concepts such as the user as a person (`SDO.Person`), the user's address as a `SDO.PostalAddress`, and user preferences represented through `SDO.seeks`. Geo-location details are represented using `SDO.availableAtOrFrom`, `SDO.GeoShape`, etc.

**Serialization and Saving**

The RDF graph is serialized into Turtle format and saved to a file named after the user's full name with underscores.

> Example filename: `John_Doe-preference.ttl`

**Publishing to Linked Data Platform**

The application publishes the user's preferences to a Linked Data Platform (LDP). It sends a POST request to the LDP endpoint with the serialized RDF data.

