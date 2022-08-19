# Modules

from flask import Flask, jsonify
import sqlite3

# Create instance of Flask

app = Flask(__name__)

# Functions


@app.route("/getTables/")
def get_table():
    conn = sqlite3.connect("buchungssystem.sqlite")
    print(f"Erfolgreich mit der Datenbank verbunden.")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tische")
    result = cursor.fetchall()
    return jsonify(result)


# Main

if __name__ == "__main__":
    app.run()
