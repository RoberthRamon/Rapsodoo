import requests
import json
import argparse
from collections import defaultdict
from datetime import datetime


def fetch_data(url):
    # retrieve data from a URL
    try:
        response = requests.get(url)
        response.raise_for_status()  
        return response.json() 
    except requests.exceptions.RequestException as e:
        print(f"Error while retrieving JSON data: {e}")
        return None
    
def get_latest_data(data):

    # convert date strings to datetime objects for the correct search
    for entry in data:
        if not "data" in entry:
           print(f'Error: At least one JSON object is missing the "data" key.')
           return None

        try:
            entry["parsed_date"] = datetime.strptime(entry["data"], "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            print(f"Errore di formattazione della data in entry: {entry}")
    
    # find the maximum date in the JSON
    max_date = max(entry["parsed_date"] for entry in data)
    
    # filter records with the maximum date
    latest_data = [entry for entry in data if entry["parsed_date"] == max_date]
    
    return latest_data

def main():
    #argparse.ArgumentParser: helps manage and interpret the arguments passed to the script from the command line.
    parser = argparse.ArgumentParser(description="Aggregate COVID-19 cases by region.")
    #optional argument --fileJSON. Name of the local JSON file containing COVID data.
    parser.add_argument("--fileJSON", type=str, help="Path to local dpc-covid19-ita-region.json file.")
    # list of arguments
    args = parser.parse_args()

    # python init.py --file dati.json
    # python init.py --file dpc-covid19-ita-regioni-vuoto.json
    # python init.py --file dpc-covid19-ita-regioni-error.json
    # python init.py --file dpc-covid19-ita-regioni-noKeyData.json

    url = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-regioni.json"
    #url = "___https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-region-latest.json"
    
    if args.fileJSON:
        # if in the command line are the arguments
        try:
            with open(args.fileJSON, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content:  
                    print(f"Error: the file '{args.fileJSON}' is empty.")
                    return  
                data = json.loads(content)
        except FileNotFoundError:
            print(f"Error: the file '{args.fileJSON}' was not found.")
            return  
        except json.JSONDecodeError:
            print(f"Error: the file '{args.fileJSON}' does not contain valid JSON data.")
            return 
    else:
        data = fetch_data(url)

    # Handling errors for an incorrect URL
    if not data:
        print("Error: unable to fetch or read JSON data.")
        return
    
     # get data for the latest date
    latest_data = get_latest_data(data)

    # TODO: return latest_data = None
    print(latest_data)


    print ("END ")
