#!flask/bin/python
from flask import Flask, jsonify, request, Response
from api.get_enriched_entities import get_enriched_entities

app = Flask(__name__)

@app.route('/response', methods=['POST'])
def request_entities():
    if not request.json or not 'headline' in request.json:
        abort(400)

    body_splitted = str.split(request.json['body_text'] ,'\n\n')
    body_3_first_sent = body_splitted[:min(len(body_splitted),3)]
    text = request.json['headline'] + request.json['description_text'] + '. '.join(body_3_first_sent)

    resp = Response(response=get_enriched_entities(text), status=200, mimetype="application/json")

    return(resp)

if __name__ == '__main__':
    app.run(debug=True)
