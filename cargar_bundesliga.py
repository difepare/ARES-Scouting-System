import os
import requests
import psycopg2
from datetime import datetime, timedelta

conn = psycopg2.connect(
    host="localhost",
    database="ares_db",
    user="postgres",
    password="Sarita2017"  # <--- CAMBIA TU CONTRASEÑA
)
cursor = conn.cursor()

API_KEY = "TU_API_KEY_AQUI"  # <--- TU CLAVE DE API-FOOTBALL
headers = {"x-rapidapi-key": API_KEY, "x-rapidapi-host": "v3.football.api-sports.io"}

# ID de la Bundesliga en API-Football
LIGA_ID = 78
LIGA_NOMBRE = "Bundesliga"
TEMPORADA = 2025

def obtener_partidos():
    url = "https://v3.football.api-sports.io/fixtures"
    params = {"league": LIGA_ID, "season": TEMPORADA}
    response = requests.get(url, headers=headers, params=params)
    return response.json()['response'] if response.status_code == 200 else []

def obtener_estadisticas(fixture_id):
    url = "https://v3.football.api-sports.io/fixtures/statistics"
    params = {"fixture": fixture_id}
    response = requests.get(url, headers=headers, params=params)
    return response.json()['response'] if response.status_code == 200 else []

def guardar_partido_y_prediccion(partido):
    local = partido['teams']['home']['name']
    visitante = partido['teams']['away']['name']
    fecha = partido['fixture']['date']
    estado = partido['fixture']['status']['short']
    goles_local = partido['goals']['home'] if partido['goals']['home'] else None
    goles_visitante = partido['goals']['away'] if partido['goals']['away'] else None

    # Verificar si los equipos existen
    cursor.execute("SELECT id FROM teams WHERE nombre = %s", (local,))
    local_id = cursor.fetchone()
    cursor.execute("SELECT id FROM teams WHERE nombre = %s", (visitante,))
    visitante_id = cursor.fetchone()
    if not local_id or not visitante_id:
        print(f"⚠️ Equipo no encontrado: {local} o {visitante}")
        return

    # Insertar partido
    cursor.execute("""
        INSERT INTO matches (local_id, visitante_id, liga, fecha, temporada, estado, goles_local, goles_visitante)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT DO NOTHING
        RETURNING id
    """, (local_id[0], visitante_id[0], LIGA_NOMBRE, fecha, str(TEMPORADA), estado, goles_local, goles_visitante))
    partido_id = cursor.fetchone()
    if not partido_id:
        print(f"⏩ Partido ya existente: {local} vs {visitante}")
        return
    partido_id = partido_id[0]
    print(f"✅ Partido insertado: {local} vs {visitante} (ID {partido_id})")

    # Simular predicción (puedes poner fórmula más compleja después)
    cursor.execute("""
        INSERT INTO predictions (partido_id, prob_local, prob_empate, prob_visitante, xG_local, xG_visitante)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (partido_id, 40.0, 30.0, 30.0, 1.5, 1.5))
    print(f"   🤖 Predicción generada para {local} vs {visitante}")

    conn.commit()

# Procesar todos los partidos de la temporada
partidos = obtener_partidos()
for p in partidos:
    guardar_partido_y_prediccion(p)

cursor.close()
conn.close()
print("🎉 Bundesliga cargada completamente en ARES")