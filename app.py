from flask import Flask, render_template, jsonify
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

app = Flask(__name__)

# --- Connexion Mongo Atlas ---
uri = "mongodb+srv://ludovic:uIrcGAaSI5zgCNAf@tpbigdata.wbz99nw.mongodb.net/?appName=TPBigData"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["OpenData"]
collection = db["Velib"]

@app.route("/")
def map_page():
    return render_template("map.html")

@app.route("/analytics")
def analytics_page():
    return render_template("analytics.html")

@app.route("/api/stations")
def api_stations():
    """Renvoie les stations Vélib au format JSON (coordonnées + stats)"""
    stations = list(collection.find(
        {"coordonnees_geo": {"$exists": True}},
        {"_id": 0, "name": 1, "ebike": 1, "mechanical": 1, "numbikesavailable": 1,
         "coordonnees_geo": 1, "nom_arrondissement_communes": 1, "stationcode": 1}
    ))
    return jsonify(stations)

if __name__ == "__main__":
    app.run(debug=True)
