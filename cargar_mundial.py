import psycopg2
from datetime import datetime

conn = psycopg2.connect(
    host="localhost",
    database="ares_db",
    user="postgres",
    password="Sarita2017"
)
cur = conn.cursor()

equipos_grupo_a = [
    ("México", 15, "CONCACAF", "A"),
    ("Sudáfrica", 60, "CAF", "A"),
    ("Corea del Sur", 23, "AFC", "A"),
    ("República Checa", 36, "UEFA", "A"),
]

for equipo in equipos_grupo_a:
    nombre, ranking, conf, grupo = equipo
    # Verificar si ya existe
    cur.execute("SELECT id FROM national_teams WHERE nombre = %s", (nombre,))
    if not cur.fetchone():
        cur.execute("""
            INSERT INTO national_teams (nombre, fifa_ranking, confederacion, grupo_mundial)
            VALUES (%s, %s, %s, %s)
        """, (nombre, ranking, conf, grupo))
        print(f"✅ {nombre} agregado")
    else:
        print(f"⏩ {nombre} ya existe, omitido")

conn.commit()
cur.close()
conn.close()
print("🎉 Proceso completado")