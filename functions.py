# Modules
import sqlite3
import random


# Functions
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def db_executequery(query, mode):
    conn = sqlite3.connect("buchungssystem.sqlite")
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    cursor.execute(query)
    if mode == "insert" or mode == "update":
        conn.commit()
    else:
        return cursor.fetchall()


def service_getalltables():
    return db_executequery("SELECT tischnummer, anzahlPlaetze FROM tische", mode="select")


def service_getreservations(date):
    return db_executequery(f"SELECT reservierungsnummer,tischnummer,zeitpunkt FROM reservierungen WHERE zeitpunkt LIKE '{date}%'", mode="select")


def service_getlastreservationnumber():
    queryresult = db_executequery("SELECT max(reservierungsnummer) AS max_reservsnr FROM reservierungen", mode="select")
    return queryresult


def service_getallreservationsontimestamp(date, time):
    query = f"""
    SELECT tische.tischnummer, tische.anzahlPlaetze, reservierungen.reservierungsnummer, reservierungen.zeitpunkt, reservierungen.storniert
    FROM tische
    LEFT JOIN reservierungen ON tische.tischnummer = reservierungen.tischnummer
    WHERE reservierungen.zeitpunkt = '{date} {time}'
    """
    queryresult = db_executequery(query, mode="select")
    return queryresult


def service_getfreetables(date, time):
    allTables = service_getalltables()
    allReservations = service_getallreservationsontimestamp(date, time)
    free_tables = []
    for table in allTables:
        reserved = False
        for reservation in allReservations:
            if table["tischnummer"] == reservation["tischnummer"] and reservation["storniert"] == "False":
                reserved = True
        if not reserved:
            free_tables.append(table)
    return free_tables


def service_reservetable(date, time, tableid):
    allReservations = service_getallreservationsontimestamp(date, time)
    nextReservation = service_getlastreservationnumber()[0]["max_reservsnr"] + 1
    reserved = False
    stornopin = random.randint(1000, 9999)
    query = f"""
        INSERT INTO reservierungen
        (reservierungsnummer,zeitpunkt,tischnummer,pin,storniert)
        VALUES ('{nextReservation}','{date} {time}',{tableid}, {stornopin},'False')
        """
    for reservation in allReservations:
        if reservation["tischnummer"] == int(tableid):
            reserved = True
    if not reserved:
        db_executequery(query, mode="insert")
        return {
            "status": "Success",
            "tag": date,
            "uhrzeit": time,
            "tischnummer": tableid,
            "reservation": nextReservation,
            "stornierungspin": stornopin
        }
    else:
        return service_getfreetables(date=date, time=time)


def service_canceltable(reservierungsnummer, pin):
    reservationToCancel = db_executequery(f"SELECT * FROM reservierungen WHERE reservierungsnummer == {reservierungsnummer} AND pin == {pin}", mode="select")
    if reservationToCancel[0]["storniert"] == "False":
        db_executequery(f"UPDATE reservierungen SET storniert='True' WHERE pin={pin}", mode="update")
        return {
            "status": "Success",
            "timestamp": reservationToCancel[0]["zeitpunkt"],
            "tischnummer": reservationToCancel[0]["tischnummer"],
            "reservation": reservationToCancel[0]["reservierungsnummer"]
        }
    else:
        return {
            "status": "Error: Reservation already cancelled"
        }
