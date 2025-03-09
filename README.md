# Rapsodoo  

## Description  
Rapsodoo is a program that extracts and aggregates COVID-19 case data from the official sources of the Italian Civil Protection Department (https://github.com/pcm-dpc/COVID-19/blob/master/dati-json/dpc-covid19-ita-regioni.json). The program allows analyzing data by region and date and saves the results in an Excel file.  

## Prerequisites  
Before running the project, make sure you have installed:  
- Python 3.x  
- The following Python libraries:  
  - `requests`  
  - `pandas`  
  - `argparse`  
  - `collections`  

## Installation  
Clone the repository and navigate to the project directory:  
```sh  
git clone https://github.com/RoberthRamon/Rapsodoo.git  
cd Rapsodoo  
```  

## Usage  
The program can be executed from the command line with different parameters:  

### Basic Execution  
```sh  
python init.py  
```  
This command downloads the latest data from the Civil Protection Department and aggregates it by region.  

### Analyzing a Local JSON File  
If you want to analyze a specific JSON file, use:  
```sh  
python init.py --fileJSON filename.json  
```  
The local JSON file must follow the structure of the Civil Protection Department's JSON file and must be saved in the `local` folder where the entire project is located.  

### Filtering Data by a Specific Date  
You can specify a date in different formats:  
```sh  
python init.py --dateJSON 2023-01-01  
```  

### Saving Data to an Excel File  
The program automatically generates an Excel file with the aggregated data in the user's `Downloads` folder.  

## Project Structure  
- `init.py` - Main script  
- `Covid.py` - Core script  
- `Covid_Utils.py` - Utility functions for date management  
- `README.md` - Documentation  
