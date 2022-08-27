# Modules
import random
import sqlite3
from flask import jsonify


# Functions
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def db_getalltables():
    conn = sqlite3.connect("buchungssystem.sqlite")
    conn.row_factory = dict_factory
    print(f"Established connection to database")
    print(f"Getting all tables")
    cursor = conn.cursor()
    cursor.execute("SELECT tischnummer, anzahlPlaetze FROM tische")
    return jsonify(cursor.fetchall())


def db_getlastreservationnumber():
    conn = sqlite3.connect("buchungssystem.sqlite")
    conn.row_factory = dict_factory
    print(f"Established connection to database")
    print(f"Getting last reservation")
    cursor = conn.cursor()
    cursor.execute("SELECT max(reservierungsnummer) FROM reservierungen")
    return jsonify(cursor.fetchall())


def db_getallreservationsontimestamp(date, time):
    conn = sqlite3.connect("buchungssystem.sqlite")
    conn.row_factory = dict_factory
    print(f"Established connection to database")
    print(f"Getting all reservations on {date} {time}")
    cursor = conn.cursor()
    query = f"""
    SELECT tische.tischnummer, tische.anzahlPlaetze, reservierungen.zeitpunkt
    FROM tische
    LEFT JOIN reservierungen ON tische.tischnummer = reservierungen.tischnummer
    WHERE reservierungen.zeitpunkt = '{date} {time}'
    """
    cursor.execute(query)
    return jsonify(cursor.fetchall())


def db_getfreetables(date, time):
    allTables = db_getalltables().get_json()
    allReservations = db_getallreservationsontimestamp(date, time).get_json()
    print(f"Getting free tables on {date} {time}")
    free_tables = []
    for table in allTables:
        reserved = False
        for reservation in allReservations:
            if table["tischnummer"] == reservation["tischnummer"]:
                reserved = True
        if not reserved:
            free_tables.append(table)
    returnDict = {
        "tag": date,
        "uhrzeit": time,
        "tables": free_tables
    }
    return returnDict


def db_reservetable(date, time, tableid):
    allReservations = db_getallreservationsontimestamp(date, time).get_json()
    lastReservation = db_getlastreservationnumber().get_json()

    exit()
    for reservation in allReservations:
        if reservation["tischnummer"] == tableid:  # Es gibt zu dem Zeitpunkt bereits eine Reservierung mit der Tisch ID
            print("Error: Tisch zu dieser Zeit bereits belegt.")
    conn = sqlite3.connect("buchungssystem.sqlite")
    conn.row_factory = dict_factory
    print(f"Established connection to database")
    print(f"Creating reservation on {date} {time} for table {tableid}")
    cursor = conn.cursor()
    query = f"""
    INSERT INTO reservierungen
    (reservierungsnummer,zeitpunkt,tischnummer,pin,storniert)
    VALUES ('11','{date} {time}',{tableid},{random.randint(1000,9999)},'False')
    """  # TODO: Reservierungsnummer entsprechend setzen.
    cursor.execute(query)
    conn.commit()
    return "Success"
