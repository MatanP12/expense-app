from flask import Flask, request, jsonify
from pymongo import MongoClient
import os
import logging
from json_formatter import get_json_handler
from bson import ObjectId

app = Flask(__name__)

client = MongoClient(os.getenv('MONGO_URI', 'mongodb://localhost:27017'))
db = client['expense_tracker']
expenses_collection = db['expenses']

app.logger.addHandler(get_json_handler())
app.logger.setLevel(logging.INFO)

def parser(expense):
    expense['_id'] = str(expense['_id'])
    return expense

@app.route("/")
def home():
    return "I am ok!", 200

@app.route("/metrics")
def metrics():
    pass # todo

@app.route("/expenses", methods=['POST','GET'])
def get_expenses_route():
    if request.method == "POST":
        data = request.json
        if 'product' not in data or 'price' not in data:
            return jsonify({'eror': 'no product or price specified'})
        new_expense = {
            'product' : data['product'],
            'price' : float(data['price'])
        }
        result = expenses_collection.insert_one(new_expense)
        new_expense = expenses_collection.find_one({'_id': result.inserted_id})
        app.logger.info('Expense added', extra={'request': request, 'log_details': new_expense})

        return jsonify(parser(new_expense)), 201
    if request.method == "GET":
        expenses = list(expenses_collection.find({}))
        expenses = list(map(parser, expenses))
        app.logger.info('Fetched expenses', extra={'request': request, 'log_details': expenses})
        return jsonify(expenses), 200


@app.route('/expenses/<string:id>', methods=['DELETE','PUT','GET'])
def delete_expense(id):
    if request.method == "DELETE":
        result = expenses_collection.delete_one({'_id': ObjectId(id)})
        if result.deleted_count == 0:
            app.logger.warning('Expense not found', extra={'request': request, 'log_details': id})
            return jsonify({'error': f'Expense with id {id} not found'}), 404
        app.logger.info('Expense deleted', extra={'request': request, 'log_details': id})
        return jsonify({'message': 'Expense deleted successfully'}), 200
    if request.method == "PUT":
        data = request.json
        if 'product' not in data and 'price' not in data:
            app.logger.warning('No fields to update', extra={'request': request})
            return jsonify({'error': 'Product or price is required to update'}), 400
        update_fields = {}
        if 'product' in data:
            update_fields['product'] = data['product']
        if 'price' in data:
            update_fields['price'] = float(data['price'])
        try:
            result = expenses_collection.update_one(
                {'_id': ObjectId(id)},
                {'$set': update_fields}
            )
            if result.matched_count == 0:
                app.logger.warning('Expense not found', extra={'request': request, 'log_details': id})
                return jsonify({'error': 'Expense not found'}), 404  
            updated_expense = expenses_collection.find_one({'_id': ObjectId(id)})
            app.logger.info('Expense updated', extra={'request': request, 'log_details': updated_expense})
            return jsonify(parser(updated_expense)), 200
        except Exception as e:
            app.logger.error('Invalid expense ID', extra={'request': request, 'log_details': str(e)})
            return jsonify({'error': 'Invalid expense ID', 'message':f'{e}'}), 400
    if request.method == "GET":
        try:
            expense = expenses_collection.find_one({'_id': ObjectId(id)})
            app.logger.info('Expense recieved', extra={'request': request, 'log_details': expense})
            return jsonify(parser(expense)), 200
        except Exception as e:
            app.logger.error('Invalid expense ID', extra={'request': request, 'log_details': str(e)})
            return jsonify({'error': 'Invalid expense ID'}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False)