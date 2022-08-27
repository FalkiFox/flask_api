# Modules / Functions
from flask import Flask, request
from functions import service_getfreetables, service_getalltables, service_reservetable, service_canceltable, service_getreservations

# Create instance of the Flask class.
app = Flask(__name__)


# API Endpoints

# Beispiel URL: http://127.0.0.1:5000/api/getAllTables/
@app.route("/api/getAllTables/", methods=["GET"])
def getalltables():
    queryresult = service_getalltables()
    return {"status": "Success", "tables": queryresult}


# Beispiel URL: http://127.0.0.1:5000/api/getFreeTables?date=2022-02-02&time=17:30:00
@app.route("/api/getFreeTables/", methods=["GET"])
def getfreetable():
    params = request.args
    date = params.get("date")
    time = params.get("time")
    queryresult = service_getfreetables(date=date, time=time)
    return {"status": "Success", "tag": date, "uhrzeit": time, "tischnummer": queryresult}


# Beispiel URL: http://127.0.0.1:5000/api/reserveTable/?date=2022-02-02&time=17:30:00&tableid=2
@app.route("/api/reserveTable/", methods=["POST"])
def reservetable():
    params = request.args
    date = params.get("date")
    time = params.get("time")
    tableid = params.get("tableid")
    queryresult = service_reservetable(date=date, time=time, tableid=tableid)
    if "status" in queryresult:
        return queryresult
    else:
        return {"status": "Error: Table already reserved", "tag": date, "uhrzeit": time, "tischnummer": queryresult}


# Beispiel URL: http://127.0.0.1:5000/api/cancelTable/?pin=1336&reservierungsnummer=6
@app.route("/api/cancelTable/", methods=["PUT"])
def canceltable():
    params = request.args
    reservierungsnummer = params.get("reservierungsnummer")
    pin = params.get("pin")
    queryresult = service_canceltable(reservierungsnummer=reservierungsnummer, pin=pin)
    return queryresult


# Beispiel URL: http://127.0.0.1:5000/api/getReservations/?date=2022-02-02
@app.route("/api/getReservations/", methods=["GET"])
def getreservations():
    params = request.args
    date = params.get("date")
    queryresult = service_getreservations(date=date)
    return {"status": "Success", "tag": date, "reservierungen": queryresult}


# Main
if __name__ == "__main__":
    app.run(debug=True)
