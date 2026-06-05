import psycopg2
from datetime import datetime, timedelta

# CONEXIÓN A TU BD (¡CAMBIA LA CONTRASEÑA!)
conn = psycopg2.connect(
    host="localhost",
    database="ares_db",
    user="postgres",
    password="Sarita2017"  # <--- Cambia esto
)
cur = conn.cursor()

# 1. LIMPIAR TABLAS ANTIGUAS (opcional, si quieres empezar de cero)
# cur.execute("DELETE FROM world_cup_predictions;")
# cur.execute("DELETE FROM world_cup_matches;")
# cur.execute("DELETE FROM national_teams;")
# print("🗑️ Datos antiguos eliminados.")

# 2. INSERTAR TODAS LAS SELECCIONES (48 EQUIPOS)
equipos = [
    # Grupo A
    ("México", 15, "CONCACAF", "A"), ("Sudáfrica", 60, "CAF", "A"),
    ("Corea del Sur", 23, "AFC", "A"), ("República Checa", 36, "UEFA", "A"),
    # Grupo B
    ("Canadá", 45, "CONCACAF", "B"), ("Bosnia", 55, "UEFA", "B"),
    ("Catar", 50, "AFC", "B"), ("Suiza", 18, "UEFA", "B"),
    # Grupo C
    ("Brasil", 1, "CONMEBOL", "C"), ("Marruecos", 14, "CAF", "C"),
    ("Haití", 85, "CONCACAF", "C"), ("Escocia", 30, "UEFA", "C"),
    # Grupo D
    ("EE.UU.", 11, "CONCACAF", "D"), ("Paraguay", 42, "CONMEBOL", "D"),
    ("Australia", 28, "AFC", "D"), ("Turquía", 32, "UEFA", "D"),
    # Grupo E
    ("Alemania", 3, "UEFA", "E"), ("Curazao", 88, "CONCACAF", "E"),
    ("Costa de Marfil", 40, "CAF", "E"), ("Ecuador", 24, "CONMEBOL", "E"),
    # Grupo F
    ("Países Bajos", 5, "UEFA", "F"), ("Japón", 19, "AFC", "F"),
    ("Túnez", 35, "CAF", "F"), ("Suecia", 26, "UEFA", "F"),
    # Grupo G
    ("Bélgica", 4, "UEFA", "G"), ("Egipto", 39, "CAF", "G"),
    ("Irán", 22, "AFC", "G"), ("Nueva Zelanda", 105, "OFC", "G"),
    # Grupo H
    ("España", 7, "UEFA", "H"), ("Cabo Verde", 72, "CAF", "H"),
    ("Arabia Saudita", 56, "AFC", "H"), ("Uruguay", 13, "CONMEBOL", "H"),
    # Grupo I
    ("Francia", 2, "UEFA", "I"), ("Senegal", 21, "CAF", "I"),
    ("Irak", 65, "AFC", "I"), ("Noruega", 44, "UEFA", "I"),
    # Grupo J
    ("Argentina", 6, "CONMEBOL", "J"), ("Argelia", 41, "CAF", "J"),
    ("Austria", 27, "UEFA", "J"), ("Jordania", 71, "AFC", "J"),
    # Grupo K
    ("Portugal", 8, "UEFA", "K"), ("RD Congo", 68, "CAF", "K"),
    ("Uzbekistán", 77, "AFC", "K"), ("Colombia", 16, "CONMEBOL", "K"),
    # Grupo L
    ("Inglaterra", 9, "UEFA", "L"), ("Croacia", 10, "UEFA", "L"),
    ("Ghana", 61, "CAF", "L"), ("Panamá", 59, "CONCACAF", "L")
]

for nombre, ranking, conf, grupo in equipos:
    cur.execute("""
        INSERT INTO national_teams (nombre, fifa_ranking, confederacion, grupo_mundial)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (nombre) DO NOTHING
    """, (nombre, ranking, conf, grupo))
print("✅ 48 selecciones cargadas.")

# 3. INSERTAR PARTIDOS DE FASE DE GRUPOS (104 partidos)
# Vamos a generar los partidos del Grupo A como ejemplo.
# Para el resto de grupos, la lógica es idéntica. 
# (Por simplicidad, este script inserta el Grupo A. 
#  Puedes repetir la estructura para los grupos B-L)

grupo_a = ["México", "Sudáfrica", "Corea del Sur", "República Checa"]
fecha_base = datetime(2026, 6, 11, 15, 0)  # 11 de junio, 3 PM (Partido inaugural)

def insertar_partidos_grupo(grupo_letra, equipos, fecha_inicio):
    for i in range(len(equipos)):
        for j in range(i+1, len(equipos)):
            cur.execute("SELECT id FROM national_teams WHERE nombre = %s", (equipos[i],))
            local_id = cur.fetchone()[0]
            cur.execute("SELECT id FROM national_teams WHERE nombre = %s", (equipos[j],))
            visit_id = cur.fetchone()[0]
            
            cur.execute("""
                INSERT INTO world_cup_matches (local_id, visitante_id, grupo, fecha, estadio, ciudad)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT DO NOTHING
            """, (local_id, visit_id, grupo_letra, fecha_inicio, "Estadio Ejemplo", "Ciudad Ejemplo"))
            print(f"📅 Partido {equipos[i]} vs {equipos[j]} ({grupo_letra}) agregado")
            fecha_inicio += timedelta(days=2)

# Insertar partidos del Grupo A
insertar_partidos_grupo("A", grupo_a, fecha_base)

conn.commit()
cur.close()
conn.close()
print("🎉 Mundial 2026 cargado en ARES")