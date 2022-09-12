from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

stores = [
    {
        'name': 'Tashcom',
        'items': [
            {
                'name': 'Charger',
                'price': 100
            }
        ]
    }
]

@app.route('/')
def home_page():
    return render_template('index.html')

# From Client to server
# POST: used to send data
# GET: used to request for data 

# From server to client
# POST: used to recieve data
# GET: used to send data back

# To create a store: POST /store data:{name}
@app.route('/store', methods = ['POST']) #Whoever is going to call our API is going to call this endpoint via a POST request.
def create_store():
    request_data = request.get_json() #converts json to python dictionary
    new_store = {
        'name': request_data['name'],
        'items': []
    }
    stores.append(new_store)
    return jsonify(new_store) #converts dictionary to json to be displayed on browser

# To return info about store for a given name: GET /store/<string:name>
@app.route('/store/<string:name>') #When we create our method it must have a parameter name which matches the one of the URI
def get_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify(store)
    return jsonify({'message': 'store not found'})

# To return list of all stores: GET /store
@app.route('/store')
def get_stores():
    return jsonify({'stores': stores})

# Create an item for a specific store: POST /store/<string:name>/item{name, price}
@app.route('/store/<string:name>/item', methods = ['POST']) 
def create_item(name):
    request_data = request.get_json()
    for store in stores:
        if store['name'] == name:
            new_item = {
                'name': request_data['name'],
                'price': request_data['price']
            }
            store['items'].append(new_item)
            return jsonify(new_item)
    return jsonify({'message': 'store not found'})

# To return all items of a specific store: GET /store/<string:name>/item
@app.route('/store/<string:name>/items')
def get_items_in_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify({'items': store['items']})
    return jsonify({'message': 'store not found'})

app.run(debug = True)