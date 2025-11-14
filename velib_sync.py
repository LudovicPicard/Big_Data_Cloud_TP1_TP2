import requests
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import time

# --- Connexion MongoDB Atlas ---
uri = "mongodb+srv://ludovic:uIrcGAaSI5zgCNAf@tpbigdata.wbz99nw.mongodb.net/?appName=TPBigData"
client = MongoClient(uri, server_api=ServerApi('1'))

try:
    client.admin.command('ping')
    print("✅ Connexion réussie à MongoDB Atlas (TPBigData) !")
except Exception as e:
    print("❌ Erreur de connexion :", e)
    exit()

# --- Base et collection ---
db = client["OpenData"]
collection = db["Velib"]

# --- Récupération des données Vélib avec pagination ---
url = "https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/velib-disponibilite-en-temps-reel/records"

limit = 100
offset = 0
all_data = []

while True:
    params = {"limit": limit, "offset": offset}
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        print(f"❌ Erreur HTTP {response.status_code}")
        break

    data = response.json().get("results", [])
    if not data:
        break  # fin des données
    
    all_data.extend(data)
    offset += limit
    print(f"📦 {len(all_data)} stations récupérées...")
    
    time.sleep(0.2)  # éviter de spammer l'API

# --- Insertion dans MongoDB ---
collection.delete_many({})
if all_data:
    collection.insert_many(all_data)
    print(f"🚲 {len(all_data)} stations Vélib importées dans MongoDB Atlas.")
else:
    print("⚠️ Aucune donnée récupérée.")
