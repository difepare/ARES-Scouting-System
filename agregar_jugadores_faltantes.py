import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="ares_db",
    user="postgres",
    password="Sarita2017"
)
cursor = conn.cursor()

# Diccionario de jugadores a insertar: {nombre, equipo_nombre, posicion, edad, nacionalidad}
jugadores = [
    ("Jude Bellingham", "Real Madrid", "Mediocampista", 20, "Inglaterra"),
    ("Vinicius Junior", "Real Madrid", "Delantero", 23, "Brasil"),
    ("Bukayo Saka", "Arsenal", "Delantero", 22, "Inglaterra"),
    ("Phil Foden", "Manchester City", "Mediocampista", 23, "Inglaterra"),
    ("Rodri", "Manchester City", "Mediocampista", 27, "España"),
    ("Ruben Dias", "Manchester City", "Defensa Central", 26, "Portugal"),
]

for nombre, equipo_nombre, posicion, edad, nacionalidad in jugadores:
    # Obtener ID del equipo
    cursor.execute("SELECT id FROM teams WHERE nombre = %s", (equipo_nombre,))
    equipo = cursor.fetchone()
    if not equipo:
        print(f"❌ Equipo {equipo_nombre} no encontrado. Saltando...")
        continue
    
    equipo_id = equipo[0]
    
    # Verificar si el jugador ya existe
    cursor.execute("SELECT id FROM players WHERE nombre = %s", (nombre,))
    if cursor.fetchone():
        print(f"⏩ Jugador {nombre} ya existe en BD")
        continue
    
    # Insertar jugador
    cursor.execute("""
        INSERT INTO players (nombre, equipo_id, posicion, edad, nacionalidad)
        VALUES (%s, %s, %s, %s, %s)
    """, (nombre, equipo_id, posicion, edad, nacionalidad))
    print(f"✅ Jugador {nombre} agregado a {equipo_nombre}")

conn.commit()
cursor.close()
conn.close()
print("\n🎉 Jugadores faltantes agregados correctamente.")