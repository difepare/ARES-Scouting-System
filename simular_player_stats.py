import psycopg2
import random

conn = psycopg2.connect(
    host="localhost",
    database="ares_db",
    user="postgres",
    password="Sarita2017"
)
cursor = conn.cursor()

# Obtener todos los jugadores
cursor.execute("SELECT id, posicion FROM players")
jugadores = cursor.fetchall()

for jugador_id, posicion in jugadores:
    # Simular estadísticas según posición
    if posicion == "Delantero":
        partidos = random.randint(20, 38)
        goles = random.randint(8, 25)
        asistencias = random.randint(3, 12)
    elif posicion == "Mediocampista":
        partidos = random.randint(25, 38)
        goles = random.randint(4, 15)
        asistencias = random.randint(5, 15)
    else:  # Defensa o Portero
        partidos = random.randint(20, 38)
        goles = random.randint(0, 5)
        asistencias = random.randint(0, 5)
    
    minutos = partidos * 85  # Aprox
    tarjetas_amarillas = random.randint(0, 8)
    tarjetas_rojas = random.randint(0, 2)
    
    cursor.execute("""
        INSERT INTO player_stats (jugador_id, temporada, partidos_jugados, minutos_totales, 
                                 goles, asistencias, tarjetas_amarillas, tarjetas_rojas)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (jugador_id, temporada) DO NOTHING
    """, (jugador_id, "2025", partidos, minutos, goles, asistencias, tarjetas_amarillas, tarjetas_rojas))

conn.commit()
cursor.close()
conn.close()
print(f"🎉 Estadísticas simuladas para {len(jugadores)} jugadores.")