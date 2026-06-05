import os
import requests
import psycopg2
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

# ============================================================
# CONEXIÓN A POSTGRESQL
# ============================================================
conn = psycopg2.connect(
    host="localhost",
    database="ares_db",
    user="postgres",
    password="Sarita2017"  # <--- CAMBIALA por la que pusiste al instalar PostgreSQL
)
cursor = conn.cursor()

# ============================================================
# CONFIGURACIÓN DE API DE FÚTBOL
# ============================================================
API_KEY = os.getenv("API_FOOTBALL_KEY")  # Tu clave paga
API_HOST = "v3.football.api-sports.io"

headers = {
    "x-rapidapi-key": API_KEY,
    "x-rapidapi-host": API_HOST
}

# ============================================================
# 1. OBTENER Y GUARDAR EQUIPOS (Premier League y La Liga)
# ============================================================
def obtener_guardar_equipos(liga_id, liga_nombre):
    url = f"https://{API_HOST}/teams"
    params = {"league": liga_id, "season": 2025}
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        for equipo in data['response']:
            nombre = equipo['team']['name']
            pais = equipo['team'].get('country', 'Desconocido')
            logo = equipo['team']['logo']
            
            cursor.execute("""
                INSERT INTO teams (nombre, liga, pais, logo_url)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (nombre) DO NOTHING
            """, (nombre, liga_nombre, pais, logo))
        conn.commit()
        print(f"✅ {liga_nombre}: equipos guardados")
    else:
        print(f"❌ Error al obtener equipos de {liga_nombre}: {response.status_code}")

# Ejecutar para Premier League (ID 39) y La Liga (ID 140)
obtener_guardar_equipos(39, "Premier League")
obtener_guardar_equipos(140, "La Liga")
obtener_guardar_equipos(78, "Bundesliga")  # <-- ID 78 en API-Football
obtener_guardar_equipos(2, "Champions League")
obtener_guardar_equipos(135, "Serie A")
obtener_guardar_equipos(61, "Ligue 1")
obtener_guardar_equipos(71, "Brasileirão")      # Brasil
obtener_guardar_equipos(128, "Liga Argentina") # Argentina
obtener_guardar_equipos(88, "Eredivisie")      # Países Bajos

# ============================================================
# 2. OBTENER Y GUARDAR JUGADORES (requiere equipo_id)
# ============================================================
def obtener_guardar_jugadores(equipo_id, equipo_nombre):
    url = f"https://{API_HOST}/players"
    params = {"team": equipo_id, "season": 2025}
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        for jugador in data['response']:
            nombre = jugador['player']['name']
            posicion = jugador['statistics'][0]['games']['position'] if jugador['statistics'] else "Desconocida"
            edad = jugador['player']['age']
            nacionalidad = jugador['player']['nationality']
            foto = jugador['player']['photo']
            
            cursor.execute("""
                INSERT INTO players (nombre, equipo_id, posicion, edad, nacionalidad, foto_url)
                VALUES (%s, (SELECT id FROM teams WHERE nombre = %s), %s, %s, %s, %s)
                ON CONFLICT DO NOTHING
            """, (nombre, equipo_nombre, posicion, edad, nacionalidad, foto))
        conn.commit()
        print(f"   ✅ Jugadores de {equipo_nombre} guardados")
    else:
        print(f"   ❌ Error al obtener jugadores de {equipo_nombre}")

# Obtener todos los equipos de la base de datos y luego sus jugadores
cursor.execute("SELECT id, nombre FROM teams")
equipos = cursor.fetchall()

for equipo_id, equipo_nombre in equipos:
    obtener_guardar_jugadores(equipo_id, equipo_nombre)

# ============================================================
# CIERRE DE CONEXIÓN
# ============================================================
cursor.close()
conn.close()
print("\n🎉 ARES ha sido alimentado con datos reales.")

# ============================================================
# PRÓXIMO PASO: Agregar partidos, estadísticas y predicciones
# ============================================================