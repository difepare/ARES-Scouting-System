import psycopg2
from collections import defaultdict
import random  # Solo para simular, en tu sistema real usarías puntos y diferencia de goles

conn = psycopg2.connect(
    host="localhost",
    database="ares_db",
    user="postgres",
    password="Sarita2017"
)
cur = conn.cursor()

# 1. Obtener equipos por grupo
cur.execute("SELECT id, nombre, grupo_mundial FROM national_teams ORDER BY grupo_mundial")
equipos = cur.fetchall()

grupos = defaultdict(list)
for id_equipo, nombre, grupo in equipos:
    grupos[grupo].append((id_equipo, nombre))

# 2. Simular clasificación (en tu sistema real, aquí leerías puntos)
# Para este ejemplo, asumimos que el primer equipo de cada grupo es el de menor ID (simulación)
clasificados = {}
for grupo, equipos_grupo in grupos.items():
    # Simulamos los 2 primeros y un tercero (para tener 8 mejores terceros)
    clasificados[grupo] = {
        "primero": equipos_grupo[0][0],
        "segundo": equipos_grupo[1][0],
        "tercero": equipos_grupo[2][0]
    }

# 3. Emparejamientos oficiales (simplificado para 12 grupos)
# Regla: 1A vs 3B/C/D, 1B vs 2A, 1C vs 2D, 1D vs 2C, etc.
cruces = [
    (clasificados["A"]["primero"], clasificados["B"]["tercero"]),  # 1A vs 3B
    (clasificados["B"]["primero"], clasificados["A"]["segundo"]),  # 1B vs 2A
    (clasificados["C"]["primero"], clasificados["D"]["tercero"]),  # 1C vs 3D
    (clasificados["D"]["primero"], clasificados["C"]["segundo"]),  # 1D vs 2C
    (clasificados["E"]["primero"], clasificados["F"]["tercero"]),
    (clasificados["F"]["primero"], clasificados["E"]["segundo"]),
    (clasificados["G"]["primero"], clasificados["H"]["tercero"]),
    (clasificados["H"]["primero"], clasificados["G"]["segundo"]),
    (clasificados["I"]["primero"], clasificados["J"]["tercero"]),
    (clasificados["J"]["primero"], clasificados["I"]["segundo"]),
    (clasificados["K"]["primero"], clasificados["L"]["tercero"]),
    (clasificados["L"]["primero"], clasificados["K"]["segundo"]),
]

# 4. Limpiar tabla y guardar nuevos cruces
cur.execute("DELETE FROM knockout_matches;")
for local_id, visitante_id in cruces:
    cur.execute("""
        INSERT INTO knockout_matches (local_id, visitante_id, ronda, fecha)
        VALUES (%s, %s, 'Octavos', NOW())
    """, (local_id, visitante_id))
    print(f"✅ Cruce generado: {local_id} vs {visitante_id}")

conn.commit()
cur.close()
conn.close()
print("🎉 Octavos de final generados correctamente.")