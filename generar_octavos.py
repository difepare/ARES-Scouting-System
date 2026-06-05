import psycopg2
from collections import defaultdict

# CONEXIÓN A BASE DE DATOS
conn = psycopg2.connect(
    host="localhost",
    database="ares_db",
    user="postgres",
    password="Sarita2017"  # <-- ¡Cambia por tu contraseña!
)
cur = conn.cursor()

# 1. OBTENER LOS EQUIPOS ORDENADOS POR GRUPO Y POSICIÓN (Para este ejemplo, se asume una clasificación ficticia)
# NOTA: En tu sistema real, aquí se leerían los puntos y diferencia de goles de cada equipo.

cur.execute("""
    SELECT grupo_mundial, id, nombre, fifa_ranking
    FROM national_teams
    ORDER BY grupo_mundial, fifa_ranking
""")
equipos = cur.fetchall()

# 2. SIMULAR LOS CLASIFICADOS: 1º y 2º de cada grupo + mejores 3ros.
# Esta es la parte que debes reemplazar con los datos reales de tu tabla de posiciones.
clasificados = []
grupos = defaultdict(list)

for grupo, id_equipo, nombre, ranking in equipos:
    grupos[grupo].append((id_equipo, nombre, ranking))

# Para este ejemplo, tomamos los 2 primeros de cada grupo (según el ranking FIFA, solo para que funcione)
for grupo, equipos_grupo in grupos.items():
    equipos_ordenados = sorted(equipos_grupo, key=lambda x: x[2])  # Ordena por ranking (menor es mejor)
    clasificados.append(equipos_ordenados[0][0])  # 1º del grupo
    clasificados.append(equipos_ordenados[1][0])  # 2º del grupo

# 3. DEFINIR LOS EMPAREJAMIENTOS SEGÚN EL CUADRO OFICIAL (MUNDIAL USA 2026)
cruces = [
    # Octavos de final: (1A vs 3B/C/D, 1B vs 2A, 1C vs 2D, 1D vs 2C, etc...)
    (clasificados[0], clasificados[1]),  # Ejemplo: 1A vs 2B (México vs Sudáfrica)
    (clasificados[2], clasificados[3]),  # Corea del Sur vs República Checa
    # Añade los 8 partidos de octavos según tu lógica de clasificación
]

# 4. INSERTAR LOS CRUCES EN knockout_matches
cur.execute("DELETE FROM knockout_matches;")  # Limpiar cruces antiguos
for local_id, visitante_id in cruces:
    cur.execute("""
        INSERT INTO knockout_matches (local_id, visitante_id, ronda, fecha)
        VALUES (%s, %s, 'Octavos', NOW())
    """, (local_id, visitante_id))
    print(f"✅ Cruce generado: {local_id} vs {visitante_id}")

conn.commit()
cur.close()
conn.close()
print("🎉 Octavos de final generados automáticamente.")