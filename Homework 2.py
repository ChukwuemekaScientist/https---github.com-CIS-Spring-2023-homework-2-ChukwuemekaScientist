import flask
from flask import jsonify
from flask import request

from sql import create_connection
from sql import execute_read_query
from sql import execute_query

import creds

#setting up an application name
app = flask.Flask(__name__)
app.config["DEBUG"] = True #allow to show errors in browser

#default url without any routing as GET request
@app.route('/', methods=['GET'])
def home():
    return "<h1> WELCOME to API class</h1>"
     
#create a endpoint to get a single snowboard from DB : http://127.0.0.1:5000/api/snowboard?id=1
@app.route('/api/snowboard', methods=['GET'])
def api_snowboard_by_id():
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return 'Error: No ID is provided!'
    myCreds = creds.Creds()
    conn = create_connection(myCreds.connectionstring, myCreds.username, myCreds.passwd, myCreds.dataBase)
    sql ="select * from snowboard"
    snowboard = execute_read_query(conn, sql)
    results = []
    for board in snowboard:
        if snowboard['id']== id:
            results.append(board)
    return jsonify(results)

#get all snowboards
@app.route('/api/snowboard/all', methods=['GET'])
def api_snowboard_all():
    myCreds = creds.Creds()
    conn = create_connection(myCreds.connectionstring, myCreds.username, myCreds.passwd, myCreds.dataBase)
    sql ="select * from snowboard"
    snowboard = execute_read_query(conn, sql)
    return jsonify(snowboard)

#add a snowboard as POST method
@app.route('/api/snowboard', methods=['POST'])
def api_add_snowboard():
    request_data = request.get_json()
    newtype = request_data['boardtype']
    newbrand = request_data['brand']
    newmsrp = request_data['msrp']
    newsize = request_data['size']

    myCreds = creds.Creds()
    conn = create_connection(myCreds.connectionstring, myCreds.username, myCreds.passwd, myCreds.dataBase)
    sql = "insert into snowboard(boardtype, brand, msrp, size) values ('%s','%s','%s','%s')" % (newtype, newbrand, newmsrp, newsize)

    execute_query(conn, sql)
    return 'Add snowboard request successful!'

# Delete a snowboard with DELETE method
@app.route('/api/snowboard', methods=['DELETE'])
def api_delete_snowboard_byID():
    request_data = request.get_json()
    idtodelete = request_data['id']
    
    myCreds = creds.Creds()
    conn = create_connection(myCreds.connectionstring, myCreds.username, myCreds.passwd, myCreds.dataBase)
    sql = "delete from snowboard where id = %s" % (idtodelete)
    execute_query(conn, sql)
        
    return "Delete request successful!"

#update a snowboard as PUT method
@app.route('/api/snowboard', methods=['PUT'])
def api_update_snowboard():
    request_data = request.get_json()
    idtoupdate = request_data['id']
    newtype = request_data['boardtype']
    newbrand = request_data['brand']
    newmsrp = request_data['msrp']
    newsize = request_data['size']

    myCreds = creds.Creds()
    conn = create_connection(myCreds.connectionstring, myCreds.username, myCreds.passwd, myCreds.dataBase)
    sql = "update snowboard set boardtype = '%s', brand = '%s', msrp = '%s', size = '%s' where id = '%s'" % (newtype, newbrand, newmsrp, newsize, idtoupdate)

    execute_query(conn, sql)
    return 'Update snowboard request successful!'

app.run()