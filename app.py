from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from bson import ObjectId
import json
import os

from modules.nlu import parse_query
from modules.query_builder import build_query

app = Flask(__name__)


client = MongoClient(MONGO_URI)
db = client['ecommerce_catalog']
collection = db['products']


def convert_objectid_to_str(obj):
    """Convert ObjectId to string for JSON serialization"""
    if isinstance(obj, list):
        return [convert_objectid_to_str(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: convert_objectid_to_str(value) for key, value in obj.items()}
    elif isinstance(obj, ObjectId):
        return str(obj)
    return obj


from flask.json.provider import DefaultJSONProvider

class MongoJSONProvider(DefaultJSONProvider):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super().default(obj)

app.json = MongoJSONProvider(app)



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/query', methods=['POST'])
def handle_query():
    data = request.get_json()
    if not data or 'query' not in data:
        return jsonify({"error": "Missing 'query' in request body"}), 400

    user_query = data['query']

    try:
        entities = parse_query(user_query)

        if not entities:
            return jsonify({
                "summary": "Sorry, I didn't understand your query...",
                "query": user_query, 
                "results": []
            }), 200

        mongo_query = build_query(entities)
        
        results = list(collection.find(mongo_query))
        
        results = convert_objectid_to_str(results)
        
        result_count = len(results)

        if result_count > 0:
            summary = f"Found {result_count} product(s) matching your criteria."
        else:
            summary = "No products found matching your criteria."

        response_data = {
            "summary": summary,
            "query": user_query,
            "interpreted_query": convert_objectid_to_str(mongo_query),
            "result_count": result_count,
            "results": results
        }

        return jsonify(response_data)

    except Exception as e:
        return jsonify({"error": f"A critical server error occurred: {str(e)}"}), 500


# **SOLUTION 2**: Alternative endpoint that removes _id field entirely
@app.route('/query_no_id', methods=['POST'])
def handle_query_no_id():
    data = request.get_json()
    if not data or 'query' not in data:
        return jsonify({"error": "Missing 'query' in request body"}), 400

    user_query = data['query']

    try:
        entities = parse_query(user_query)

        if not entities:
            return jsonify({
                "summary": "Sorry, I didn't understand your query...",
                "query": user_query, 
                "results": []
            }), 200

        mongo_query = build_query(entities)
        
        results = list(collection.find(mongo_query, {"_id": 0}))
        result_count = len(results)

        if result_count > 0:
            summary = f"Found {result_count} product(s) matching your criteria."
        else:
            summary = "No products found matching your criteria."

        return jsonify({
            "summary": summary,
            "query": user_query,
            "result_count": result_count,
            "results": results
        })

    except Exception as e:
        return jsonify({"error": f"A critical server error occurred: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True, port=8080)