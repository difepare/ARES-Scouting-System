import os
import requests
import psycopg2
from dotenv import load_dotenv

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
# 1. OBTENER ESTADÍSTICAS DE JUGADORES POR EQUIPO
# ============================================================
def obtener_estadisticas_jugadores(equipo_id, equipo_nombre, temporada=2025):
    url = f"https://{API_HOST}/players"
    params = {
        "team": equipo_id,
        "season": temporada
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        for jugador_data in data['response']:
            jugador = jugador_data['player']
            estadisticas = jugador_data['statistics'][0] if jugador_data['statistics'] else None
            
            if not estadisticas:
                continue
            
            nombre = jugador['name']
            posicion = estadisticas['games']['position'] if estadisticas['games']['position'] else 'Desconocida'
            partidos = estadisticas['games']['appearences'] or 0
            minutos = estadisticas['games']['minutes'] or 0
            goles = estadisticas['goals']['total'] or 0
            asistencias = estadisticas['goals']['assists'] or 0
            tarjetas_amarillas = estadisticas['cards']['yellow'] or 0
            tarjetas_rojas = estadisticas['cards']['red'] or 0
            
            # Buscar ID del jugador en nuestra tabla
            cursor.execute("SELECT id FROM players WHERE nombre = %s", (nombre,))
            jugador_id_row = cursor.fetchone()
            
            if jugador_id_row:
                jugador_id = jugador_id_row[0]
                # Insertar o actualizar estadísticas
                cursor.execute("""
                    INSERT INTO player_stats (jugador_id, temporada, partidos_jugados, minutos_totales, 
                                             goles, asistencias, tarjetas_amarillas, tarjetas_rojas)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (jugador_id, temporada) DO UPDATE SET
                        partidos_jugados = EXCLUDED.partidos_jugados,
                        minutos_totales = EXCLUDED.minutos_totales,
                        goles = EXCLUDED.goles,
                        asistencias = EXCLUDED.asistencias,
                        tarjetas_amarillas = EXCLUDED.tarjetas_amarillas,
                        tarjetas_rojas = EXCLUDED.tarjetas_rojas,
                        updated_at = CURRENT_TIMESTAMP
                """, (jugador_id, str(temporada), partidos, minutos, goles, asistencias, 
                      tarjetas_amarillas, tarjetas_rojas))
                print(f"   ✅ {nombre} - {partidos} PJ, {goles} G, {asistencias} A")
            else:
                print(f"   ⚠️ Jugador {nombre} no encontrado en la base de datos")
        conn.commit()
        print(f"✅ Estadísticas guardadas para {equipo_nombre}")
    else:
        print(f"❌ Error al obtener estadísticas de {equipo_nombre}: {response.status_code}")

# ============================================================
# 2. EJECUTAR PARA TODOS LOS EQUIPOS
# ============================================================
cursor.execute("SELECT id, nombre FROM teams")
equipos = cursor.fetchall()

for equipo_id, equipo_nombre in equipos:
    print(f"📊 Procesando {equipo_nombre}...")
    obtener_estadisticas_jugadores(equipo_id, equipo_nombre)

# ============================================================
# CIERRE DE CONEXIÓN
# ============================================================
cursor.close()
conn.close()
print("\n🎉 ARES ahora tiene estadísticas reales de jugadores.")