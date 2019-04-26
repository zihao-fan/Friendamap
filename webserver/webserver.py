from flask import Flask, request, Response
import json
import logging
import MySQLdb

app = Flask(__name__)

def read_database(sql):
    db = MySQLdb.connect(
        host="localhost",
        user="root",
        passwd="my-secret-pw",
        database="friend"
    )
    cursor = db.cursor()
    cursor.execute(sql)
    return cursor.fetchall()


def update_database(sql):
    db = MySQLdb.connect(
        host="localhost",
        user="root",
        passwd="secret",
        database="friend"
    )
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()


@app.route('/v1/places', methods=["GET"])
def find_nearby_favorite():
    arguments = request.get_json()
    title = arguments.get("title")
    is_completed = arguments.get("is_completed")




@app.route('/v1/liked', methods=["GET"])
def list_all_frind_liked(placeID):

	read_database("	SELECT userID FROM Visits WHERE placeID = '{}'".format(placeID))



@app.route('/v1/visited', methods=["GET"])
def list_all_friend_visited(placeID):

	read_database("SELECT userID FROM Likes WHERE placeID = '{}'".format(placeID))



@app.route('/v1/like', methods=["POST"])
def like_a_place():






@app.route('/v1/visit', methods=["POST"])
def visit_a_place():


















