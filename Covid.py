import requests
import json
import argparse
import pandas as pd
import os
from collections import defaultdict
from datetime import datetime

import Covid_Utils as utl


def fetch_data(url):
    """ 
    retrieve data from a URL
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  
        return response.json() 
    except requests.exceptions.RequestException as e:
        print(f"Error while retrieving JSON data: {e}")
        return None
    
def get_latest_data(data,dateJSON):
    """
    Extract the data for a specific date or max date
    """
    # convert date strings to datetime objects for the correct search
    for entry in data:
        if not "data" in entry:
           print(f'Error: At least one JSON object is missing the "data" key.')
           return None

        try:
            entry["parsed_date"] = datetime.strptime(entry["data"], "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            print(f"Date formatting error in entry: {entry}")

    # TASK2: 
    if dateJSON!=None:
        ####################################
        #TODO: verifie the time
        ####################################
        # filter records with the maximum date
        latest_data = [entry for entry in data if entry["parsed_date"].date() == dateJSON]
        date_data=dateJSON
        print("COVID data grouped by regions on the date",dateJSON)
    else:
        # find the maximum date in the JSON
        max_date = max(entry["parsed_date"] for entry in data)
        # filter records with the maximum date
        latest_data = [entry for entry in data if entry["parsed_date"] == max_date]
        date_data=max_date
        print("COVID data grouped by regions on the date",max_date)
    
    return latest_data,date_data

def check_duplicate_regions(data):
    """
    Check for duplicate region codes in the data and print a warning if necessary.

    Returns:
        dict: Dictionary with duplicated region codes and their number of occurrences.
    """
    region_duplicate=defaultdict(int)
    for entry in data:
        cod_region= entry["codice_regione"]
        region_duplicate[cod_region] += 1

    duplicate_keys = {k: v for k, v in region_duplicate.items() if v > 1}

    if duplicate_keys:
        print("Warning: Duplicated codice_regione found!", duplicate_keys)

    return duplicate_keys


def process_data(data):
    # TODO ASK: If the JSON contains two or more records with the same cod_region, should I sum the cases, or is it a mistake?

    check_duplicate_regions(data)

    # in this dictionary save the (denominazione_regione, sum all totale_casi)
    region_cases = defaultdict(int)
    for entry in data:
        name_region= entry["denominazione_regione"]
        cases      = entry["totale_casi"]
        region_cases[name_region] += cases
    
    return sorted(region_cases.items(), key=lambda x: (-x[1], x[0]))


#TASK3
def save_to_excel(data, dateFile):
    filename = f"covid_data_{dateFile.strftime('%Y%m%d')}.xlsx"
    download_path = os.path.join(os.path.expanduser("~"), "Downloads", filename)
    df = pd.DataFrame(data, columns=["Region", "Total number of cases"])
    df.to_excel(download_path, index=False)
    print(f"Data saved to {download_path}")

def main():

    #argparse.ArgumentParser: helps manage and interpret the arguments passed to the script from the command line.
    parser = argparse.ArgumentParser(description="Aggregate COVID-19 cases by region.")
    #TASK1: optional argument --fileJSON. Name of the local JSON file containing COVID data. 
    parser.add_argument("--fileJSON", type=str, help="Name of the JSON file to analyze.")
    #TASK2: optinal argument --dateJSON. 
    parser.add_argument("--dateJSON", type=str, help="Date to search for COVID data within the range from 24/02/2020 to today.")
    # list of arguments
    args = parser.parse_args()

    url = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-regioni.json"
    
    if args.fileJSON:
        # if in the command line are the arguments
        try:
            #opens/closure a JSON file in read mode
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
    
    #TASK2...
    dateJSON=None
    if args.dateJSON:
        dateJSON=utl.convert_valid_date(args.dateJSON)
        if dateJSON==None:
            print ("Warning: the date '{args.dateJSON}' is not in a correct format, try again.")
            return
    #...TASK2    

    # get data for the latest date
    latest_data,date_data = get_latest_data(data,dateJSON)
    if latest_data==None or latest_data==[]:
        print("There is no data in the JSON for the date",dateJSON)
        return
    
    sorted_cases = process_data(latest_data)

    for region, cases in sorted_cases:
        print(f"{region}: {cases}")
    
    #TASK3  
    save_to_excel(sorted_cases,date_data)


