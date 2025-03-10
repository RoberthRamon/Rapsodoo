from flask import Flask

app = Flask(__name__)

@app.route('/covid-data', methods=['GET'])
def get_covid_data():

    return "Ciao Roberth"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
