# Semantic Web Project Report
**Group Members:** 
- Mohsen Hadavi 
- Alale Mohammadi Golrang

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

3. **Collect Data:**
    ```bash
    python3 main.py collect
    ```
    This command will execute the `collect` function, to crawl through the web and collect data from different restaurants

4. **Query Data:**
    
    ```bash
    python3 main.py query --datetime="2024-01-03T12:30:00" --location="2.3522,48.8566" --max-distance=10 --price=10 --rank-by=distance
    ```
    
    You can customize the parameters (datetime, location, max_distance, price, rank_by) based on your needs.

5. **Describe Data:**
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





