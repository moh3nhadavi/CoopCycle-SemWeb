import sys

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Please pass an argument")
    else:
        if sys.argv[1] == 'collect':
            from collect import collect_data
            collect_data()
        else:
            print("Wrong argument")
        
    