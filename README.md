### Setup the project
 1. clone the project:
 
 ```
 git clone https://gitlab.emse.fr/mohsen.hadavi/sem-web-coop-cycle
 ```

 2. create a virtual enviornment:

 ```
 python3 -m vene ./venv
 source ./venv/bin/activate
 ```

 3. install dependencies:
 ```
 pip3 install -r requirements.txt
 ```


### Python files
This project contains multiple python files:

- `collect.py` is for collecting data from json file and crawling on the web per CoopCycle center to gather information.

- `main.py` it is the main file and runs other files based on the argument you pass to this file.


### How to run

```[python]
python3 main.py [argument]
```
- instead of `arguement` you should pass the value that you want to pass bases on your needs. see below section

### Arguments

- `collect` : to collect data from the web and publish it on Fuseki triple store. 
