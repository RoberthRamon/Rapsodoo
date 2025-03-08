import requests
import json
import argparse
from collections import defaultdict


def fetch_data(url):
    # retrieve data from a URL
    try:
        response = requests.get(url)
        response.raise_for_status()  
        return response.json() 
    except requests.exceptions.RequestException as e:
        print(f"Error while retrieving data: {e}")
        return None


def main():
    #argparse.ArgumentParser: helps manage and interpret the arguments passed to the script from the command line.
    parser = argparse.ArgumentParser(description="Aggregate COVID-19 cases by region.")
    #optional argument --fileJSON. Name of the local JSON file containing COVID data.
    parser.add_argument("--fileJSON", type=str, help="Path to local dpc-covid19-ita-region.json file.")
    # list of arguments
    args = parser.parse_args()
    # python script.py --file dati.json

    url = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-regioni.json"
    #url = "___https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-region-latest.json"
    
    if args.fileJSON:
        try:
            with open(args.fileJSON, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            print(f"Error: The file '{args.fileJSON}' was not found.")
            return  
    else:
        data = fetch_data(url)

    # Handling errors for an incorrect URL
    if not data:
        print("Error: Unable to fetch or read JSON data.")
        return
    
    print ("END ")
