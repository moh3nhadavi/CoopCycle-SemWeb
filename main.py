import sys
from global_functions import bcolors
    
    

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print(f"{bcolors.FAIL}Error: Please pass an argument{bcolors.ENDC}")
    else:
        if sys.argv[1] == 'collect':
            from collect import collect_data
            collect_data()
        elif sys.argv[1] == 'crawl':
            from crawler import store_data
            store_data()
        elif sys.argv[1] == 'query':
            from query import run_query
            if len(sys.argv) == 3:
                run_query(datetime=sys.argv[2])
            else:
                run_query()
        else:
            print(f"{bcolors.FAIL}Error: Wrong argument{bcolors.ENDC}")
        
    