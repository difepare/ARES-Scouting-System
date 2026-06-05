import psycopg2

# Conexión a tu base de datos (¡cambia la contraseña!)
conn = psycopg2.connect(
    host="localhost",
    database="ares_db",
    user="postgres",
    password="Sarita2017"  # <--- Cambia por tu contraseña real
)
cur = conn.cursor()

# Primero, limpiamos la tabla para evitar duplicados
cur.execute("DELETE FROM knockout_matches;")
print("🗑️ Datos antiguos eliminados.")

# --- CRUCES DE OCTAVOS DE FINAL (MUNDIAL USA 2026) ---
# Formato: (local_id, visitante_id, ronda)
# ¡ATENCIÓN! Estos IDs son los que tiene ARES en national_teams.
# Si cambian en tu BD, ajústalos.

octavos = [
    # (local_id, visitante_id, 'Octavos')
    (1, 2, 'Octavos'),   # Ejemplo: México vs Sudáfrica (Grupo A)
    (3, 4, 'Octavos'),   # Corea del Sur vs República Checa
    (5, 6, 'Octavos'),   # Canadá vs Bosnia (Grupo B)
    (7, 8, 'Octavos'),   # Catar vs Suiza
    (9, 10, 'Octavos'),  # Brasil vs Marruecos (Grupo C)
    (11, 12, 'Octavos'), # Haití vs Escocia
    (13, 14, 'Octavos'), # EE.UU. vs Paraguay (Grupo D)
    (15, 16, 'Octavos'), # Australia vs Turquía
    # ... puedes añadir más hasta completar los 8 partidos
]

for local, visitante, ronda in octavos:
    cur.execute("""
        INSERT INTO knockout_matches (local_id, visitante_id, ronda, fecha)
        VALUES (%s, %s, %s, NOW())
        ON CONFLICT (id) DO NOTHING
    """, (local, visitante, ronda))
    print(f"✅ Partido {local} vs {visitante} ({ronda}) agregado")

conn.commit()
cur.close()
conn.close()
print("🎉 Octavos de final cargados. ¡ARES ya puede predecir la fase final!")