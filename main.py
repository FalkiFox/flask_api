# Modules / Functions
from flask import Flask, request
from functions import db_getfreetables, db_getalltables, db_reservetable

# Create instance of the Flask class.
app = Flask(__name__)


# API Endpoints
@app.route("/api/getAllTables/", methods=["GET"])
def getalltable():
    return db_getalltables()


@app.route("/api/getFreeTables/", methods=["GET"])
def getfreetable():
    params = request.get_json()
    return db_getfreetables(date=params["date"], time=params["time"])


@app.route("/api/reserveTable/", methods=["POST"])
def reservetable():
    params = request.get_json()
    return db_reservetable(date=params["date"], time=params["time"], tableid=params["tableID"])


# Main
if __name__ == "__main__":
    app.run(debug=True)
