from flask import Flask, request, Response
import json
import logging
import mysql.connector

app = Flask(__name__)

def read_database(sql):
    db = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        passwd="my-secret-pw",
        database="friend",
        auth_plugin='mysql_native_password'
    )
    cursor = db.cursor()
    cursor.execute(sql)
    return cursor.fetchall()

result = read_database('SELECT * FROM Users')
print('type', type(result))
print('result', result)

def update_database(sql):
    db = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        passwd="my-secret-pw",
        database="friend",
        auth_plugin='mysql_native_password'
    )
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()


@app.route('/v1/places', methods=["GET"])
def find_nearby_favorite():
    if request.headers['Content-Type'] == 'application/x-www-form-urlencoded':
        latitude = request.form.get("latitude")
        longitude = request.form.get("longitude")
        place = request.form.get("place")
    elif request.headers['Content-Type'] == 'application/json':
        arguments = request.get_json()
        latitude = arguments.get("latitude")
        longitude = arguments.get("longitude")
        place = arguments.get("place")



@app.route('/v1/liked', methods=["GET"])
def list_all_frind_liked(placeID):
    placeID = None

    if request.headers['Content-Type'] == 'application/x-www-form-urlencoded':
        placeID = reqeust.form.get("place_id")
    elif request.headers['Content-Type'] == 'application/json':
        placeID = arguments.get("place_id")

    if placeID:
        read_database("SELECT user_id FROM Likes WHERE place_id = '{}'".format(placeID))


@app.route('/v1/visited', methods=["GET"])
def list_all_friend_visited():
    placeID = None

    if request.headers['Content-Type'] == 'application/x-www-form-urlencoded':
        placeID = reqeust.form.get("place_id")
    elif request.headers['Content-Type'] == 'application/json':
        placeID = arguments.get("place_id")

    if placeID:
        return_data = read_database("SELECT user_id FROM Likes WHERE place_id = '{}'".format(placeID))
        print(return_data)




@app.route('/v1/like', methods=["POST"])
def like_a_place():
    if request.headers['Content-Type'] == 'application/x-www-form-urlencoded':
        placeID = request.form.get("placeID")
        userID = request.form.get("userID")
    elif request.headers['Content-Type'] == 'application/json':
        arguments = request.get_json()
        placeID = arguments.get("placeID")
        userID = arguments.get("userID")

    sql_query = "INSERT INTO Likes (place_id, user_id) VALUES ({}, {})".format(placeID, userID)
    update_database(sql_query)

    return_code = 201
    logging.info("PlaceID {} is liked by userID {}.".format(placeID, userID))
    data = {"placeID": placeID, "userLiked": userID}
    
    resp = Response(json.dumps(data), status = return_code, mimetype='application/json')
    return resp



@app.route('/v1/visit', methods=["POST"])
def visit_a_place():
    if request.headers['Content-Type'] == 'application/x-www-form-urlencoded':
        placeID = request.form.get("place_id")
        userID = request.form.get("user_id")
    elif request.headers['Content-Type'] == 'application/json':
        arguments = request.get_json()
        placeID = arguments.get("place_id")
        userID = arguments.get("user_id")

    sql_query = "INSERT INTO Visits (place_id, user_id) VALUES ({}, {})".format(placeID, userID)
    update_database(sql_query)

    return_code = 201
    logging.info("PlaceID {} is visited by userID {}.".format(placeID, userID))
    data = {"placeID": placeID, "userVisited": userID}
    
    resp = Response(json.dumps(data), status = return_code, mimetype='application/json')
    return resp









