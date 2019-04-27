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
        place_address = request.form.get("place_address")

    elif request.headers['Content-Type'] == 'application/json':
        arguments = request.get_json()
        latitude = arguments.get("latitude")
        longitude = arguments.get("longitude")
        place = arguments.get("place")
        place_address = arguments.get("place_address")


    place_address = place_address.replace(" ", "+")
    key = "tfl7CPD56XnakZ4CJ0S42MtaAZEaIA1G"
    url = "https://www.mapquestapi.com/geocoding/v1/address?key={}&inFormat=kvp&outFormat=json&location={}&thumbMaps=false".format(key, place_address)
    response = requests.get(url)
    place_latitude = response["results"][0]["locations"][0]["displayLatLng"]["lat"]
    place_longitude = response["results"][0]["locations"][0]["displayLatLng"]["lng"]


    # Get user's favorite place
    auth = ("api", "dGda5UmGwgtvW3LfCpcgla5WwqVfkeFBlx6TKczXJ3AvIRIs-6eCclrsUOi-xvp6VVOYu_V-rX1sje2yKIMcKX_PgpPdgf9y2VCgoYFosaMJ_laJd8ZT_IhdgY7DXHYx")
    url = "https://api.yelp.com/v3/businesses/search?term={}&latitude={}&longitude={}&limit=1".format(place, place_latitude, place_longitude)
    response = requests.get(url, auth=auth)

    user_place_dict = {}
    user_place_dict["rating"] = response["businesses"][0]["rating"]
    user_place_dict["id"] = response["businesses"][0]["id"]
    user_place_dict["name"] = response["businesses"][0]["name"]
    user_place_dict["price"] = response["businesses"][0]["price"]
    user_place_dict["categories"] = response["businesses"][0]["categories"]

    # Get 5 similar places nearby
    url = "https://api.yelp.com/v3/businesses/search?term={}&latitude={}&longitude={}&limit=5".format(place, latitude, longitude)
    response = requests.get(url, auth=auth)

    results_list = []
    for business in response["businesses"]:
        d = {}
        d["rating"] = business["rating"]
        d["id"] = business["id"]
        d["name"] = business["name"]
        d["price"] = business["price"]
        d["categories"] = business["categories"][0]["title"]
        results_list.append(d)

    sorted_list = get_closest(results_list, user_place_dict)
    data = {"results": sorted_list}
    resp = Response(json.dumps(data), status=status_code, mimetype='application/json')


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









