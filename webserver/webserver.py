from flask import Flask, request, Response
import json
import logging
import mysql.connector
import pymysql
import requests
#import get_Closest

app = Flask(__name__)
db = mysql.connector.connect(
        # host="127.0.0.1",
        host="my-mysql",
        user="root",
        passwd="my-secret-pw",
        database="friend",
        auth_plugin='mysql_native_password'
    )

def read_database(sql):
    global db     
    cursor = db.cursor()
    cursor.execute(sql)
    return cursor.fetchall()

def update_database(sql):
    global db 
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()

def convert_to_str(item):
    attr = ['address1', 'address2', 'address3', 'city', 'state', 'zip_code']
    str_list = []
    for x in attr:
        if not item['location'][x]:
            continue
        else:
            str_list.append(str(item['location'][x]).strip())
    num = len(str_list)
    temp = '{} ' * num
    addr = temp.strip().format(*tuple(str_list))
    return addr

@app.route('/v1/places', methods=["GET"])
def find_nearby_favorite():
    if request.headers['Content-Type'] == 'application/x-www-form-urlencoded':
        current_address = request.form.get("current_address")
        #latitude = request.form.get("latitude")
        #longitude = request.form.get("longitude")

        # place: user's favotite place in hometown
        place = request.form.get("place")

        # place_address: that place's address
        place_address = request.form.get("place_address")

    elif request.headers['Content-Type'] == 'application/json':
        arguments = request.get_json()
        current_address = arguments.get("current_address")
        #latitude = arguments.get("latitude")
        #longitude = arguments.get("longitude")

        place = arguments.get("place")
        place_address = arguments.get("place_address")


    # convert user's current address into latitude and longitude
    current_address = current_address.replace(" ", "+")
    key = "tfl7CPD56XnakZ4CJ0S42MtaAZEaIA1G"
    url = "https://www.mapquestapi.com/geocoding/v1/address?key={}&inFormat=kvp&outFormat=json&location={}&thumbMaps=false".format(key, current_address)
    response = requests.get(url).json()
    latitude = response["results"][0]["locations"][0]["displayLatLng"]["lat"]
    longitude = response["results"][0]["locations"][0]["displayLatLng"]["lng"]

    #  convert user's favorite place's address into latitude and longitude
    place_address = place_address.replace(" ", "+")
    key = "tfl7CPD56XnakZ4CJ0S42MtaAZEaIA1G"
    url = "https://www.mapquestapi.com/geocoding/v1/address?key={}&inFormat=kvp&outFormat=json&location={}&thumbMaps=false".format(key, place_address)
    response = requests.get(url).json()
    place_latitude = response["results"][0]["locations"][0]["displayLatLng"]["lat"]
    place_longitude = response["results"][0]["locations"][0]["displayLatLng"]["lng"]


    # Get user's favorite place in hometown
    api_key = "dGda5UmGwgtvW3LfCpcgla5WwqVfkeFBlx6TKczXJ3AvIRIs-6eCclrsUOi-xvp6VVOYu_V-rX1sje2yKIMcKX_PgpPdgf9y2VCgoYFosaMJ_laJd8ZT_IhdgY7DXHYx"
    headers = {
            'Authorization': 'Bearer {}'.format(api_key),
    }
    url = "https://api.yelp.com/v3/businesses/search?term={}&latitude={}&longitude={}&limit=1".format(place, place_latitude, place_longitude)
    response = requests.get(url, headers=headers).json()

    user_place_dict = {}
    user_place_dict["rating"] = response["businesses"][0]["rating"]
    user_place_dict["id"] = response["businesses"][0]["id"]
    user_place_dict["name"] = response["businesses"][0]["name"]
    user_place_dict["price"] = response["businesses"][0]["price"]
    user_place_dict["categories"] = response["businesses"][0]["categories"]

    # Get 5 similar places nearby
    url = "https://api.yelp.com/v3/businesses/search?term={}&latitude={}&longitude={}&limit=5".format(place, latitude, longitude)
    response = requests.get(url, headers=headers).json()

    results_list = []
    for business in response["businesses"]:
        d = {}
        d["rating"] = business["rating"]
        d["id"] = business["id"]
        d["name"] = business["name"]
        d["price"] = business["price"]
        d["categories"] = business["categories"][0]["title"]
        # d["address"]  = str(business["location"]["address1"]) + " " + str(business["location"]["address2"]) \
        #                 + str(business["location"]["address3"]) + str(business["location"]["city"]) + " "\
        #                 + str(business["location"]["state"]) + " " + str(business["location"]["zip_code"])
        d["address"] = convert_to_str(business)
        results_list.append(d)

    print("results_list: ", results_list)
    print("user_place_dict: ", user_place_dict)
    sorted_list = get_closest(results_list, user_place_dict)
    data = {"results": sorted_list}
    resp = Response(json.dumps(data), status=201, mimetype='application/json')

    return resp

def get_closest(list_of_nearby, favorite_place):
    """ score = 0 + no. pf duplicates in categories * 5 - price dollar sign digits difference * 2 - rating difference * 10 """
    ref_rating = float(favorite_place["rating"]) # this is a float
    ref_price_len = len(favorite_place["price"]) # this is the length of the dollar sign - an int
    ref_categ = favorite_place["categories"] # this is a string!

    for item in list_of_nearby:
        score = 0
        list_of_cat_words = item["categories"].split()
        for word in list_of_cat_words:
            if word in ref_categ:
                score += 1
        score = score * 5
        score = score - 2 * abs(len(item["price"]) - ref_price_len)
        score = score - 10 * abs(float(item["rating"]) - ref_rating)
        item["score"] = score

    return_list = []

    for item in list_of_nearby:
        return_list.append({"name": item["name"], "address": item["address"],
                            "id": item["id"], "score": item["score"]})

    return_list = sorted(return_list, key = lambda i: i["score"], reverse = True)
    return return_list




@app.route('/v1/liked', methods=["GET"])
def list_all_friend_liked():
    if request.headers['Content-Type'] == 'application/x-www-form-urlencoded':
        place_name = request.form.get("place_name")
        place_address = request.form.get("place_address")
    elif request.headers['Content-Type'] == 'application/json':
        place_name = arguments.get("place_name")
        place_address = arguments.get("place_address")

    placeID = address_to_id_helper(place_name, place_address)

    return_data = read_database("SELECT U.first_name, U.last_name FROM Likes AS L INNER JOIN Users AS U ON L.user_id = U.id WHERE place_id = '{}'".format(placeID))
    # return_data is a list of tuples (each tuple is a row)
    return_data = [' '.join(list(item)) for item in return_data]
    data = {"results": return_data}
    resp = Response(json.dumps(data), status=200, mimetype='application/json')
    return resp


@app.route('/v1/visited', methods=["GET"])
def list_all_friend_visited():
    if request.headers['Content-Type'] == 'application/x-www-form-urlencoded':
        place_name = request.form.get("place_name")
        place_address = request.form.get("place_address")
    elif request.headers['Content-Type'] == 'application/json':
        place_name = arguments.get("place_name")
        place_address = arguments.get("place_address")

    placeID = address_to_id_helper(place_name, place_address)

    return_data = read_database("SELECT U.first_name, U.last_name FROM Visits AS V INNER JOIN Users AS U ON V.user_id = U.id WHERE place_id = '{}'".format(placeID))
    return_data = [' '.join(list(item)) for item in return_data]
    data = {"results": return_data}
    resp = Response(json.dumps(data), status=200, mimetype='application/json')
    return resp



@app.route('/v1/like', methods=["POST"])
def like_a_place():
    if request.headers['Content-Type'] == 'application/x-www-form-urlencoded':
        place_name = request.form.get("place_name")
        place_address = request.form.get("place_address")
        userID = request.form.get("user_id")
    elif request.headers['Content-Type'] == 'application/json':
        arguments = request.get_json()
        place_name = arguments.get("place_name")
        place_address = arguments.get("place_address")
        userID = arguments.get("user_id")

    placeID = address_to_id_helper(place_name, place_address)

    sql_query = "INSERT INTO Likes (place_id, user_id) VALUES ('{}', {})".format(placeID, userID)
    print('sql_query', sql_query)
    update_database(sql_query)

    return_code = 201
    logging.info("PlaceID {} is liked by userID {}.".format(placeID, userID))
    data = {"placeID": placeID, "userLiked": userID}
    
    resp = Response(json.dumps(data), status = return_code, mimetype='application/json')
    return resp



@app.route('/v1/visit', methods=["POST"])
def visit_a_place():
    if request.headers['Content-Type'] == 'application/x-www-form-urlencoded':
        place_name = request.form.get("place_name")
        place_address = request.form.get("place_address")
        userID = request.form.get("user_id")
    elif request.headers['Content-Type'] == 'application/json':
        arguments = request.get_json()
        place_name = arguments.get("place_name")
        place_address = arguments.get("place_address")
        userID = arguments.get("user_id")

    placeID = address_to_id_helper(place_name, place_address)

    sql_query = "INSERT INTO Visits (place_id, user_id) VALUES ('{}', {})".format(placeID, userID)
    update_database(sql_query)

    return_code = 201
    logging.info("PlaceID {} is visited by userID {}.".format(placeID, userID))
    data = {"placeID": placeID, "userVisited": userID}
    
    resp = Response(json.dumps(data), status = return_code, mimetype='application/json')
    return resp


def address_to_id_helper(place, place_address):
    place_address = place_address.replace(" ", "+")
    key = "tfl7CPD56XnakZ4CJ0S42MtaAZEaIA1G"
    url = "https://www.mapquestapi.com/geocoding/v1/address?key={}&inFormat=kvp&outFormat=json&location={}&thumbMaps=false".format(key, place_address)
    response = requests.get(url).json()
    place_latitude = response["results"][0]["locations"][0]["displayLatLng"]["lat"]
    place_longitude = response["results"][0]["locations"][0]["displayLatLng"]["lng"]

    yelp_api_key = "dGda5UmGwgtvW3LfCpcgla5WwqVfkeFBlx6TKczXJ3AvIRIs-6eCclrsUOi-xvp6VVOYu_V-rX1sje2yKIMcKX_PgpPdgf9y2VCgoYFosaMJ_laJd8ZT_IhdgY7DXHYx"
    headers = {
            'Authorization': 'Bearer {}'.format(yelp_api_key),
    }
    yelp_url = "https://api.yelp.com/v3/businesses/search?term={}&latitude={}&longitude={}&limit=1".format(place, place_latitude, place_longitude)
    response = requests.get(yelp_url, headers=headers).json()

    return response["businesses"][0]["id"]







