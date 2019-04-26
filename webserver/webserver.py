from flask import Flask, request, Response
import json
import logging
import MySQLdb

app = Flask(__name__)


@app.route('/v1/places', methods=["GET"])
def find_nearby_favorite():





@app.route('/v1/liked', methods=["GET"])
def list_all_frind_liked():








@app.route('/v1/visited', methods=["GET"])
def list_all_friend_visited():






@app.route('/v1/like', methods=["POST"])
def like_a_place():






@app.route('/v1/visit', methods=["POST"])
def visit_a_place():


















