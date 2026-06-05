import psycopg2
from collections import defaultdict

conn = psycopg2.connect(
    host="localhost",
    database="ares_db",
    user="postgres",
    password="Sarita2017"
)
cur = conn.cursor()

# Obtener todos los partidos finalizados con sus resultados
cur.execute("""
    SELECT t1.id as club_id, 
           CASE 
               WHEN m.goles_local > m.goles_visitante THEN 'win'
               WHEN m.goles_local = m.goles_visitante THEN 'draw'
               ELSE 'loss'
           END as resultado,
           m.goles_local, m.goles_visitante,
           m.temporada
    FROM matches m
    JOIN teams t1 ON m.local_id = t1.id
    WHERE m.estado = 'FT' AND m.goles_local IS NOT NULL
""")
partidos_local = cur.fetchall()

cur.execute("""
    SELECT t2.id as club_id, 
           CASE 
               WHEN m.goles_visitante > m.goles_local THEN 'win'
               WHEN m.goles_local = m.goles_visitante THEN 'draw'
               ELSE 'loss'
           END as resultado,
           m.goles_visitante, m.goles_local,
           m.temporada
    FROM matches m
    JOIN teams t2 ON m.visitante_id = t2.id
    WHERE m.estado = 'FT' AND m.goles_local IS NOT NULL
""")
partidos_visitante = cur.fetchall()

# Unir todos los resultados
partidos = list(partidos_local) + list(partidos_visitante)

# Diccionario para acumular estadísticas por club
stats = defaultdict(lambda: {
    'partidos': 0, 'victorias': 0, 'empates': 0, 'derrotas': 0,
    'goles_favor': 0, 'goles_contra': 0, 'temporada': None
})

for club_id, resultado, gf, gc, temporada in partidos:
    stats[club_id]['partidos'] += 1
    stats[club_id]['goles_favor'] += gf
    stats[club_id]['goles_contra'] += gc
    stats[club_id]['temporada'] = temporada
    if resultado == 'win':
        stats[club_id]['victorias'] += 1
    elif resultado == 'draw':
        stats[club_id]['empates'] += 1
    else:
        stats[club_id]['derrotas'] += 1

# Calcular puntuación ARES y actualizar tabla
for club_id, data in stats.items():
    puntos_ares = (
        data['victorias'] * 3 +
        data['empates'] * 1 +
        data['goles_favor'] * 0.1 -
        data['goles_contra'] * 0.05
    )
    cur.execute("""
        INSERT INTO club_rankings (club_id, temporada, puntos_ares, partidos_jugados,
                                   victorias, empates, derrotas, goles_favor, goles_contra)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (club_id, temporada) DO UPDATE SET
            puntos_ares = EXCLUDED.puntos_ares,
            partidos_jugados = EXCLUDED.partidos_jugados,
            victorias = EXCLUDED.victorias,
            empates = EXCLUDED.empates,
            derrotas = EXCLUDED.derrotas,
            goles_favor = EXCLUDED.goles_favor,
            goles_contra = EXCLUDED.goles_contra,
            updated_at = CURRENT_TIMESTAMP
    """, (club_id, data['temporada'], puntos_ares, data['partidos'],
          data['victorias'], data['empates'], data['derrotas'],
          data['goles_favor'], data['goles_contra']))

conn.commit()
cur.close()
conn.close()
print("🏆 Ranking ARES para clubes actualizado correctamente.")