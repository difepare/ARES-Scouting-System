import os
import requests
import psycopg2
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    host="localhost",
    database="ares_db",
    user="postgres",
    password="Sarita2017"
)
cursor = conn.cursor()

API_KEY = os.getenv("API_FOOTBALL_KEY")
API_HOST = "v3.football.api-sports.io"

headers = {
    "x-rapidapi-key": API_KEY,
    "x-rapidapi-host": API_HOST
}

# Obtener ID del equipo del Real Madrid desde nuestra BD
cursor.execute("SELECT id FROM teams WHERE nombre = 'Real Madrid'")
real_madrid_id = cursor.fetchone()[0]

print(f"ID Real Madrid en BD: {real_madrid_id}")

# Obtener jugadores del Real Madrid desde la API
url = f"https://{API_HOST}/players"
params = {
    "team": real_madrid_id,
    "season": 2025
}

response = requests.get(url, headers=headers, params=params)

if response.status_code == 200:
    data = response.json()
    print(f"Jugadores encontrados en API: {len(data['response'])}")
    for jugador in data['response'][:5]:
        nombre_api = jugador['player']['name']
        # Buscar en nuestra BD
        cursor.execute("SELECT id FROM players WHERE nombre = %s", (nombre_api,))
        existe = cursor.fetchone()
        if existe:
            print(f"✅ {nombre_api} existe en BD (ID {existe[0]})")
        else:
            print(f"❌ {nombre_api} NO existe en BD")
else:
    print(f"Error API: {response.status_code}")

cursor.close()
conn.close()