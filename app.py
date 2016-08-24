#!flask/bin/python
from flask import Flask, jsonify, request, Response
from get_enriched_entities import get_enriched_entities

app = Flask(__name__)


@app.route('/response', methods=['POST'])
def request_entities():
    if not request.json or not 'headline' in request.json:
        abort(400)
    text = request.json['headline'] + request.json['description_text'] + request.json['body_text'] 
    
    response = get_enriched_entities(text)
    
    resp = Response(response=response,
        status=200, \
        mimetype="application/json")
    return(resp)


    #return jsonify(response), 201

if __name__ == '__main__':
    app.run(debug=True)
