from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
import os
import logging 
from logging.handlers import RotatingFileHandler
from bson import ObjectId
from prometheus_flask_exporter import PrometheusMetrics
app = Flask(__name__)

mongo_username = os.getenv('MONGODB_USERNAME', 'root')
mongo_password = os.getenv('MONGODB_PASSWORD','example')
mongo_host = os.getenv('MONGODB_HOST', 'localhost')

client = MongoClient(f'mongodb://{mongo_username}:{mongo_password}@{mongo_host}')
db = client['expenses']
expenses_collection = db['expenses']

file_handler = RotatingFileHandler('app.log', maxBytes=10240, backupCount=10)
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
file_handler.setFormatter(formatter)

app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)

metrics = PrometheusMetrics(app)
metrics.info('app_info','Application info')


@app.before_request
def log_request_info():
    app.logger.info('Request: %s %s %s', request.method, request.path, request.data)

    
@app.after_request
def log_response_info(response):
    app.logger.info('Response: %s %s', response.status, response.data)
    return response


def parser(expense):
    return {
        "product" : expense['product'],
        "price" : expense['price'],
        "id" : str(expense['_id'])
    }

@app.route("/")
def home():
    return render_template("index.html")

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
        # app.logger.info('Expense added', extra={'request': request, 'log_details': new_expense})
        return jsonify(parser(new_expense)), 201
    if request.method == "GET":
        expenses = list(expenses_collection.find({}))
        expenses = list(map(parser, expenses))
        # app.logger.info('Fetched expenses', extra={'request': request, 'log_details': expenses})
        return jsonify(expenses), 200


@app.route('/expenses/<string:id>', methods=['DELETE','PUT','GET'])
def delete_expense(id):
    if request.method == "DELETE":
        result = expenses_collection.delete_one({'_id': ObjectId(id)})
        if result.deleted_count == 0:
            app.logger.warning('Expense not found', extra={'request': request, 'log_details': id})
            return jsonify({'error': f'Expense with id {id} not found'}), 404
        # app.logger.info('Expense deleted', extra={'request': request, 'log_details': id})
        return jsonify({'message': 'Expense deleted successfully'}), 200
    if request.method == "PUT":
        data = request.json
        if 'product' not in data and 'price' not in data:
            # app.logger.warning('No fields to update', extra={'request': request})
            return jsonify({'error': 'Product or price is required to update'}), 400
        update_fields = {}
        if 'product' in data:
            update_fields['product'] = data['product']
        if 'price' in data :
            update_fields['price'] = float(data['price'])
        try:
            result = expenses_collection.update_one(
                {'_id': ObjectId(id)},
                {'$set': update_fields}
            )
            if result.matched_count == 0:
                # app.logger.warning('Expense not found', extra={'request': request, 'log_details': id})
                return jsonify({'error': 'Expense not found'}), 404  
            updated_expense = expenses_collection.find_one({'_id': ObjectId(id)})
            # app.logger.info('Expense updated', extra={'request': request, 'log_details': updated_expense})
            return jsonify(parser(updated_expense)), 200
        except Exception as e:
            # app.logger.error('Invalid expense ID', extra={'request': request, 'log_details': str(e)})
            return jsonify({'error': 'Invalid expense ID', 'message':f'{e}'}), 400
    if request.method == "GET":
        try:
            expense = expenses_collection.find_one({'_id': ObjectId(id)})
            # app.logger.info('Expense recieved', extra={'request': request, 'log_details': expense})
            return jsonify(parser(expense)), 200
        except Exception as e:
            # app.logger.error('Invalid expense ID', extra={'request': request, 'log_details': str(e)})
            return jsonify({'error': 'Invalid expense ID'}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False)