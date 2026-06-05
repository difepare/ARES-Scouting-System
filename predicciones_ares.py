import os
import requests
import psycopg2
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

# ============================================================
# CONEXIÓN A POSTGRESQL
# ============================================================
conn = psycopg2.connect(
    host="localhost",
    database="ares_db",
    user="postgres",
    password="Sarita2017"  # <--- CAMBIALA
)
cursor = conn.cursor()

# ============================================================
# CONFIGURACIÓN DE API DE FÚTBOL
# ============================================================
API_KEY = os.getenv("API_FOOTBALL_KEY")
API_HOST = "v3.football.api-sports.io"

headers = {
    "x-rapidapi-key": API_KEY,
    "x-rapidapi-host": API_HOST
}

# ============================================================
# 1. OBTENER Y GUARDAR PARTIDOS
# ============================================================
def obtener_guardar_partidos(liga_id, liga_nombre):
    hoy = datetime.now()
    fecha_desde = (hoy - timedelta(days=30)).strftime("%Y-%m-%d")
    fecha_hasta = (hoy + timedelta(days=30)).strftime("%Y-%m-%d")
    
    url = f"https://{API_HOST}/fixtures"
    params = {
        "league": liga_id,
        "season": 2025,
        "from": fecha_desde,
        "to": fecha_hasta
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        for partido in data['response']:
            local_nombre = partido['teams']['home']['name']
            visitante_nombre = partido['teams']['away']['name']
            fecha = partido['fixture']['date']
            estado = partido['fixture']['status']['short']
            goles_local = partido['goals']['home'] if partido['goals']['home'] is not None else None
            goles_visitante = partido['goals']['away'] if partido['goals']['away'] is not None else None
            
            # Verificar si el partido ya existe (evitar duplicados)
            cursor.execute("""
                SELECT id FROM matches 
                WHERE local_id = (SELECT id FROM teams WHERE nombre = %s) 
                AND visitante_id = (SELECT id FROM teams WHERE nombre = %s) 
                AND fecha = %s
            """, (local_nombre, visitante_nombre, fecha))
            existing = cursor.fetchone()
            
            if existing:
                partido_id = existing[0]
                print(f"   ⏩ Partido ya existe: {local_nombre} vs {visitante_nombre} (ID {partido_id})")
            else:
                # Insertar nuevo partido
                cursor.execute("""
                    INSERT INTO matches (local_id, visitante_id, liga, fecha, temporada, estado, goles_local, goles_visitante)
                    VALUES ((SELECT id FROM teams WHERE nombre = %s), (SELECT id FROM teams WHERE nombre = %s), %s, %s, %s, %s, %s, %s)
                    RETURNING id
                """, (local_nombre, visitante_nombre, liga_nombre, fecha, "2025", estado, goles_local, goles_visitante))
                partido_id = cursor.fetchone()[0]
                conn.commit()
                print(f"   ✅ Nuevo partido insertado: {local_nombre} vs {visitante_nombre} (ID {partido_id})")
            
            # Si el partido ya se jugó, obtener estadísticas y generar predicción
            if estado == "FT" or estado == "AET":
                obtener_guardar_estadisticas(partido['fixture']['id'], partido_id)
                generar_prediccion(partido_id, local_nombre, visitante_nombre)
                
        conn.commit()
        print(f"✅ {liga_nombre}: partidos actualizados")
    else:
        print(f"❌ Error al obtener partidos de {liga_nombre}: {response.status_code}")

# ============================================================
# 2. OBTENER Y GUARDAR ESTADÍSTICAS DE PARTIDOS (mejorado)
# ============================================================
def obtener_guardar_estadisticas(fixture_id, partido_id):
    url = f"https://{API_HOST}/fixtures/statistics"
    params = {"fixture": fixture_id}
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        for equipo_stats in data['response']:
            es_local = equipo_stats['team']['name'] == "Local"  # Simplificado, la API puede usar nombres diferentes
            # Aquí puedes mapear las estadísticas reales que devuelve la API
            # Por ahora, guardamos un registro genérico
            cursor.execute("""
                INSERT INTO match_stats (partido_id, posesion_local, posesion_visitante, xG_local, xG_visitante)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT DO NOTHING
            """, (partido_id, 50.0, 50.0, 1.5, 1.5))  # Datos simulados por ahora
        conn.commit()
        print(f"   📊 Estadísticas guardadas para partido {partido_id}")
    else:
        print(f"   ⚠️ No se pudieron obtener estadísticas para fixture {fixture_id}")

# ============================================================
# 3. GENERAR PREDICCIÓN (ARES mejorado)
# ============================================================
def generar_prediccion(partido_id, local, visitante):
    # Verificar si ya existe una predicción para este partido
    cursor.execute("SELECT id FROM predictions WHERE partido_id = %s", (partido_id,))
    if cursor.fetchone():
        print(f"   ⏩ Predicción ya existe para {local} vs {visitante}")
        return
    
    # Lógica de predicción (la migraremos de tu script original)
    prob_local = 55.0
    prob_empate = 25.0
    prob_visitante = 20.0
    xG_local = 1.8
    xG_visitante = 1.2
    confluencia = False
    recomendacion = "Partido equilibrado, esperar señales"
    
    try:
        cursor.execute("""
            INSERT INTO predictions (partido_id, prob_local, prob_empate, prob_visitante, xG_local, xG_visitante, confluencia_activada, recomendacion)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (partido_id, prob_local, prob_empate, prob_visitante, xG_local, xG_visitante, confluencia, recomendacion))
        conn.commit()
        print(f"   🤖 Predicción generada para {local} vs {visitante}")
    except Exception as e:
        print(f"   ❌ Error al guardar predicción: {e}")

# ============================================================
# EJECUTAR PARA PREMIER LEAGUE (ID 39) Y LA LIGA (ID 140)
# ============================================================
print("🚀 ARES: Iniciando ingesta de partidos y predicciones...\n")
obtener_guardar_partidos(39, "Premier League")
obtener_guardar_partidos(140, "La Liga")

# ============================================================
# CIERRE DE CONEXIÓN
# ============================================================
cursor.close()
conn.close()
print("\n🎉 ARES ha sido alimentado con partidos, estadísticas y predicciones.")