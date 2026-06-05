import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="ares_db",
    user="postgres",
    password="Sarita2017"
)
cur = conn.cursor()

# Insertar cruces de ejemplo (Octavos de final)
# Aquí debes poner los id correctos de national_teams. Ejemplo con México (id=1) vs Sudáfrica (id=2)
cruces = [
    (1, 2, 'Octavos'),   # México vs Sudáfrica
    (3, 4, 'Octavos'),   # Corea del Sur vs República Checa
    # ... añade todos los cruces reales de octavos
]

for local, visit, ronda in cruces:
    cur.execute("""
        INSERT INTO knockout_matches (local_id, visitante_id, ronda, fecha)
        VALUES (%s, %s, %s, NOW())
        ON CONFLICT DO NOTHING
    """, (local, visit, ronda))

conn.commit()
cur.close()
conn.close()
print("🎉 Cruces de fase final cargados")