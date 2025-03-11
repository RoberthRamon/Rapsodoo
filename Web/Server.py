import sys
import os

# add the parent folder to the path.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask,request
import json
import Covid as co
import Covid_Utils as utl

app = Flask(__name__)

@app.route('/covid-data', methods=['GET'])
def get_covid_data():
    url = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-regioni.json"
    if request.args.get("fileJSON") :
        # if in the command line are the arguments
        try:
            #opens/closure a JSON file in read mode
            with open(request.args.get("fileJSON"), "r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content:  
                    return  {"error": "the file is empty."},400
                data = json.loads(content)
        except FileNotFoundError:
            return {"error": "the file  was not found."},400
        except json.JSONDecodeError:
            return {"error": "the file does not contain valid JSON data."},400
    else:
        data = co.fetch_data(url)

    dateJSON=None
    if request.args.get("dateJSON"):
        dateJSON=utl.convert_valid_date(request.args.get("dateJSON"))
    latest_data,date_data = co.get_latest_data(data,dateJSON)    

    sorted_cases = co.process_data(latest_data)
    return sorted_cases

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)


