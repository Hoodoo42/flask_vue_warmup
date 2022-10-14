import mariadb
from flask import Flask, request, make_response
import json
from apihelpers import check_endpoint_info
import dbhelpers as dbh

app = Flask(__name__)

@app.post('/api/pokemon')
def new_pokemon():
    is_valid = check_endpoint_info(request.json, ['name', 'description', 'img_url'])
    if(is_valid != None):
        return make_response(json.dumps(is_valid, default=str), 400)

    results = dbh.run_statement('CALL new_pokemon(?,?,?)', [request.json.get('name'), request.json.get('description'), request.json.get('img_url')]
    )

    if(type(results) == list):
        return make_response(json.dumps(results, default=str), 200)
    else:
        return make_response(json.dumps('error', default=str), 500)

@app.get('/api/pokemon')
def get_pokemon():
    results = dbh.run_statement('CALL get_pokemon()')

    if(type(results) == list):
        return make_response(json.dumps(results, default=str), 200)
    else:
        return make_response(json.dumps('sorry, error', default=str), 500)           


new_pokemon()
get_pokemon()

app.run(debug=True)