from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import psycopg2

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    return psycopg2.connect(
        host="localhost",
        database="ares_db",
        user="postgres",
        password="Sarita2017"
    )

# ==================================================
# ENDPOINTS PRINCIPALES
# ==================================================

@app.get("/api/partidos_ares")
def get_partidos_ares():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT m.id, t1.nombre as local, t2.nombre as visitante, m.fecha
        FROM matches m
        JOIN teams t1 ON m.local_id = t1.id
        JOIN teams t2 ON m.visitante_id = t2.id
        WHERE t1.liga IN ('Premier League', 'La Liga')
          AND t2.liga IN ('Premier League', 'La Liga')
        ORDER BY m.fecha
        LIMIT 50
    """)
    partidos = cur.fetchall()
    cur.close()
    conn.close()

    return [{
        "id": p[0],
        "local": p[1],
        "visitante": p[2],
        "fecha": p[3],
        "estado": "Pendiente",
        "prob_local": 40,
        "prob_empate": 25,
        "prob_visitante": 35,
        "xG_local": 1.4,
        "xG_visitante": 1.3
    } for p in partidos]

@app.get("/api/jugadores")
def get_jugadores():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT p.nombre, t.nombre as equipo, ps.goles
        FROM players p
        JOIN teams t ON p.equipo_id = t.id
        JOIN player_stats ps ON p.id = ps.jugador_id
        ORDER BY ps.goles DESC
        LIMIT 20
    """)
    data = cur.fetchall()
    cur.close()
    conn.close()
    return [{"nombre": d[0], "equipo": d[1], "goles": d[2]} for d in data]

@app.get("/api/ofertas")
def get_ofertas():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT DISTINCT ON (p.nombre) p.nombre, teo.nombre as origen, ted.nombre as destino, tof.monto_oferta
        FROM transfer_offers tof
        JOIN players p ON tof.jugador_id = p.id
        JOIN teams teo ON tof.equipo_origen_id = teo.id
        JOIN teams ted ON tof.equipo_destino_id = ted.id
        LIMIT 20
    """)
    data = cur.fetchall()
    cur.close()
    conn.close()
    return [{"jugador": d[0], "origen": d[1], "destino": d[2], "monto": d[3]} for d in data]

@app.get("/api/talentos_v2")
def get_talentos_v2():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT p.id, p.nombre, p.edad, p.posicion, p.nacionalidad, t.nombre as equipo,
               ps.goles, ps.asistencias, ps.partidos_jugados, ps.minutos_totales
        FROM players p
        JOIN teams t ON p.equipo_id = t.id
        JOIN player_stats ps ON p.id = ps.jugador_id
        WHERE p.edad <= 22 AND ps.partidos_jugados > 5
        ORDER BY (ps.goles + ps.asistencias) DESC
        LIMIT 30
    """)
    jugadores = cur.fetchall()
    cur.close()
    conn.close()

    talentos = []
    for j in jugadores:
        (id_jugador, nombre, edad, posicion, nacionalidad, equipo,
         goles, asistencias, partidos, minutos) = j
        
        productividad = round((goles + asistencias) / partidos, 2) if partidos > 0 else 0
        indice = round((goles + asistencias) + (minutos / 1000), 1)
        indice = min(10, max(0, indice))
        
        nivel = "🌟 CRACK MUNDIAL" if indice >= 7 else ("📈 PROMESA DE ÉLITE" if indice >= 5 else "🔍 VALOR EN ALZA")
        
        talentos.append({
            "id": id_jugador,
            "nombre": nombre,
            "edad": edad,
            "posicion": posicion,
            "nacionalidad": nacionalidad or "Desconocida",
            "equipo": equipo,
            "indice_talento": indice,
            "nivel": nivel,
            "recomendacion": "Seguimiento prioritario",
            "valor_mercado": round(indice * 3, 1),
            "estadisticas": {
                "goles": goles,
                "asistencias": asistencias,
                "partidos": partidos,
                "minutos": minutos,
                "productividad": productividad
            }
        })
    return talentos

@app.get("/api/worldcup/predictions")
def get_worldcup_predictions():
    # ==============================================
    # MUNDIAL USA 2026 - GRUPOS REALES (12 GRUPOS)
    # Basado en el calendario oficial que me compartiste
    # ==============================================
    
    partidos = []
    partido_id = 1
    
    # GRUPO A
    grupo_a = [
        {"local": "🇲🇽 México", "visitante": "🇿🇦 Sudáfrica", "prob_local": 55, "prob_empate": 25, "prob_visitante": 20},
        {"local": "🇰🇷 Corea del Sur", "visitante": "🇨🇿 Chequia", "prob_local": 45, "prob_empate": 30, "prob_visitante": 25},
        {"local": "🇨🇿 Chequia", "visitante": "🇿🇦 Sudáfrica", "prob_local": 48, "prob_empate": 28, "prob_visitante": 24},
        {"local": "🇲🇽 México", "visitante": "🇰🇷 Corea del Sur", "prob_local": 52, "prob_empate": 27, "prob_visitante": 21},
    ]
    
    # GRUPO B
    grupo_b = [
        {"local": "🇨🇦 Canadá", "visitante": "🇧🇦 Bosnia y Herzegovina", "prob_local": 53, "prob_empate": 26, "prob_visitante": 21},
        {"local": "🇶🇦 Qatar", "visitante": "🇨🇭 Suiza", "prob_local": 35, "prob_empate": 28, "prob_visitante": 37},
        {"local": "🇨🇭 Suiza", "visitante": "🇧🇦 Bosnia y Herzegovina", "prob_local": 50, "prob_empate": 28, "prob_visitante": 22},
        {"local": "🇨🇦 Canadá", "visitante": "🇶🇦 Qatar", "prob_local": 48, "prob_empate": 27, "prob_visitante": 25},
    ]
    
    # GRUPO C
    grupo_c = [
        {"local": "🇧🇷 Brasil", "visitante": "🇲🇦 Marruecos", "prob_local": 58, "prob_empate": 24, "prob_visitante": 18},
        {"local": "🇭🇹 Haití", "visitante": "🏴󠁧󠁢󠁳󠁣󠁴󠁿 Escocia", "prob_local": 30, "prob_empate": 28, "prob_visitante": 42},
        {"local": "🏴󠁧󠁢󠁳󠁣󠁴󠁿 Escocia", "visitante": "🇲🇦 Marruecos", "prob_local": 40, "prob_empate": 30, "prob_visitante": 30},
        {"local": "🇧🇷 Brasil", "visitante": "🇭🇹 Haití", "prob_local": 70, "prob_empate": 18, "prob_visitante": 12},
    ]
    
    # GRUPO D
    grupo_d = [
        {"local": "🇺🇸 USA", "visitante": "🇵🇾 Paraguay", "prob_local": 55, "prob_empate": 26, "prob_visitante": 19},
        {"local": "🇦🇺 Australia", "visitante": "🇹🇷 Turquía", "prob_local": 38, "prob_empate": 28, "prob_visitante": 34},
        {"local": "🇺🇸 USA", "visitante": "🇦🇺 Australia", "prob_local": 56, "prob_empate": 25, "prob_visitante": 19},
        {"local": "🇹🇷 Turquía", "visitante": "🇵🇾 Paraguay", "prob_local": 48, "prob_empate": 27, "prob_visitante": 25},
    ]
    
    # GRUPO E
    grupo_e = [
        {"local": "🇨🇮 Costa de Marfil", "visitante": "🇪🇨 Ecuador", "prob_local": 42, "prob_empate": 30, "prob_visitante": 28},
        {"local": "🇩🇪 Alemania", "visitante": "🇨🇼 Curazao", "prob_local": 72, "prob_empate": 18, "prob_visitante": 10},
        {"local": "🇩🇪 Alemania", "visitante": "🇨🇮 Costa de Marfil", "prob_local": 58, "prob_empate": 24, "prob_visitante": 18},
        {"local": "🇪🇨 Ecuador", "visitante": "🇨🇼 Curazao", "prob_local": 55, "prob_empate": 26, "prob_visitante": 19},
    ]
    
    # GRUPO F
    grupo_f = [
        {"local": "🇳🇱 Países Bajos", "visitante": "🇯🇵 Japón", "prob_local": 54, "prob_empate": 26, "prob_visitante": 20},
        {"local": "🇸🇪 Suecia", "visitante": "🇹🇳 Túnez", "prob_local": 48, "prob_empate": 28, "prob_visitante": 24},
        {"local": "🇳🇱 Países Bajos", "visitante": "🇸🇪 Suecia", "prob_local": 50, "prob_empate": 27, "prob_visitante": 23},
    ]
    
    # GRUPO G
    grupo_g = [
        {"local": "🇧🇪 Bélgica", "visitante": "🇪🇬 Egipto", "prob_local": 52, "prob_empate": 27, "prob_visitante": 21},
        {"local": "🇮🇷 Irán", "visitante": "🇳🇿 Nueva Zelanda", "prob_local": 48, "prob_empate": 28, "prob_visitante": 24},
    ]
    
    # GRUPO H
    grupo_h = [
        {"local": "🇪🇸 España", "visitante": "🇨🇻 Cabo Verde", "prob_local": 65, "prob_empate": 22, "prob_visitante": 13},
        {"local": "🇸🇦 Arabia Saudita", "visitante": "🇺🇾 Uruguay", "prob_local": 30, "prob_empate": 28, "prob_visitante": 42},
    ]
    
    # GRUPO I
    grupo_i = [
        {"local": "🇫🇷 Francia", "visitante": "🇸🇳 Senegal", "prob_local": 55, "prob_empate": 25, "prob_visitante": 20},
        {"local": "🇮🇶 Irak", "visitante": "🇳🇴 Noruega", "prob_local": 32, "prob_empate": 28, "prob_visitante": 40},
    ]
    
    # GRUPO J
    grupo_j = [
        {"local": "🇦🇷 Argentina", "visitante": "🇩🇿 Argelia", "prob_local": 58, "prob_empate": 24, "prob_visitante": 18},
        {"local": "🇦🇹 Austria", "visitante": "🇯🇴 Jordania", "prob_local": 48, "prob_empate": 28, "prob_visitante": 24},
    ]
    
    # GRUPO K
    grupo_k = [
        {"local": "🇵🇹 Portugal", "visitante": "🇨🇩 RD Congo", "prob_local": 56, "prob_empate": 25, "prob_visitante": 19},
        {"local": "🇺🇿 Uzbekistán", "visitante": "🇨🇴 Colombia", "prob_local": 28, "prob_empate": 27, "prob_visitante": 45},
    ]
    
    # GRUPO L
    grupo_l = [
        {"local": "🏴󠁧󠁢󠁥󠁮󠁧󠁿 Inglaterra", "visitante": "🇭🇷 Croacia", "prob_local": 48, "prob_empate": 29, "prob_visitante": 23},
        {"local": "🇬🇭 Ghana", "visitante": "🇵🇦 Panamá", "prob_local": 46, "prob_empate": 28, "prob_visitante": 26},
    ]
    
    # Unir todos los grupos
    grupos = {
        "🇦 Grupo A": grupo_a,
        "🇧 Grupo B": grupo_b,
        "🇨 Grupo C": grupo_c,
        "🇩 Grupo D": grupo_d,
        "🇪 Grupo E": grupo_e,
        "🇫 Grupo F": grupo_f,
        "🇬 Grupo G": grupo_g,
        "🇭 Grupo H": grupo_h,
        "🇮 Grupo I": grupo_i,
        "🇯 Grupo J": grupo_j,
        "🇰 Grupo K": grupo_k,
        "🇱 Grupo L": grupo_l,
    }
    
    # Convertir a lista de partidos con ID único
    for grupo, matches in grupos.items():
        for match in matches:
            # Determinar favorito para la recomendación
            if match["prob_local"] > match["prob_visitante"]:
                favorito = match["local"]
            elif match["prob_visitante"] > match["prob_local"]:
                favorito = match["visitante"]
            else:
                favorito = "Equilibrado"
            
            partidos.append({
                "id": partido_id,
                "grupo": grupo,
                "local": match["local"],
                "visitante": match["visitante"],
                "prob_local": match["prob_local"],
                "prob_empate": match["prob_empate"],
                "prob_visitante": match["prob_visitante"],
                "recomendacion": f"🔮 ARES predice: {favorito} {'favorito' if favorito != 'Equilibrado' else 'partido muy parejo'}"
            })
            partido_id += 1
    
    return partidos
@app.get("/api/knockout/predictions")
def get_knockout_predictions():
    return [
        {
            "id": 101,
            "ronda": "Octavos",
            "local": "🇧🇷 Brasil",
            "visitante": "🇨🇴 Colombia",
            "prob_local": 55,
            "prob_visitante": 45,
            "ganador_predicho": "🇧🇷 Brasil",
            "fecha": "2026-07-01"
        },
        {
            "id": 102,
            "ronda": "Octavos",
            "local": "🇦🇷 Argentina",
            "visitante": "🇺🇾 Uruguay",
            "prob_local": 52,
            "prob_visitante": 48,
            "ganador_predicho": "🇦🇷 Argentina",
            "fecha": "2026-07-02"
        },
        {
            "id": 103,
            "ronda": "Octavos",
            "local": "🏴󠁧󠁢󠁥󠁮󠁧󠁿 Inglaterra",
            "visitante": "🇳🇱 Países Bajos",
            "prob_local": 48,
            "prob_visitante": 52,
            "ganador_predicho": "🇳🇱 Países Bajos",
            "fecha": "2026-07-03"
        },
        {
            "id": 104,
            "ronda": "Octavos",
            "local": "🇫🇷 Francia",
            "visitante": "🇵🇹 Portugal",
            "prob_local": 50,
            "prob_visitante": 50,
            "ganador_predicho": "🇫🇷 Francia",
            "fecha": "2026-07-04"
        },
        {
            "id": 201,
            "ronda": "Cuartos",
            "local": "🇧🇷 Brasil",
            "visitante": "🇦🇷 Argentina",
            "prob_local": 48,
            "prob_visitante": 52,
            "ganador_predicho": "🇦🇷 Argentina",
            "fecha": "2026-07-08"
        },
        {
            "id": 202,
            "ronda": "Cuartos",
            "local": "🇫🇷 Francia",
            "visitante": "🇳🇱 Países Bajos",
            "prob_local": 53,
            "prob_visitante": 47,
            "ganador_predicho": "🇫🇷 Francia",
            "fecha": "2026-07-09"
        },
        {
            "id": 301,
            "ronda": "Semis",
            "local": "🇦🇷 Argentina",
            "visitante": "🇫🇷 Francia",
            "prob_local": 47,
            "prob_visitante": 53,
            "ganador_predicho": "🇫🇷 Francia",
            "fecha": "2026-07-13"
        },
        {
            "id": 302,
            "ronda": "Semis",
            "local": "🏴󠁧󠁢󠁥󠁮󠁧󠁿 Inglaterra",
            "visitante": "🇪🇸 España",
            "prob_local": 45,
            "prob_visitante": 55,
            "ganador_predicho": "🇪🇸 España",
            "fecha": "2026-07-14"
        },
        {
            "id": 401,
            "ronda": "Final",
            "local": "🇫🇷 Francia",
            "visitante": "🇪🇸 España",
            "prob_local": 51,
            "prob_visitante": 49,
            "ganador_predicho": "🇫🇷 Francia",
            "fecha": "2026-07-19"
        },
        {
            "id": 402,
            "ronda": "Tercer Lugar",
            "local": "🇦🇷 Argentina",
            "visitante": "🏴󠁧󠁢󠁥󠁮󠁧󠁿 Inglaterra",
            "prob_local": 50,
            "prob_visitante": 50,
            "ganador_predicho": "🇦🇷 Argentina",
            "fecha": "2026-07-18"
        }
    ]

@app.get("/api/ligas/{nombre}")
def get_partidos_por_liga(nombre: str):
    # Mapear nombre de liga (solo las que funcionan)
    ligas_validas = {
        "bundesliga": "Bundesliga",
        "champions": "Champions League",
        "seriea": "Serie A",
        "ligue1": "Ligue 1"
    }
    
    if nombre not in ligas_validas:
        return {"error": "Liga no válida"}
    
    liga_bd = ligas_validas[nombre]
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT m.id, t1.nombre as local, t2.nombre as visitante, m.fecha
        FROM matches m
        JOIN teams t1 ON m.local_id = t1.id
        JOIN teams t2 ON m.visitante_id = t2.id
        WHERE t1.liga = %s AND t2.liga = %s
        ORDER BY m.fecha
        LIMIT 50
    """, (liga_bd, liga_bd))
    partidos = cur.fetchall()
    cur.close()
    conn.close()

    return [{
        "id": p[0],
        "local": p[1],
        "visitante": p[2],
        "fecha": p[3],
        "estado": "Pendiente",
        "prob_local": 40,
        "prob_empate": 30,
        "prob_visitante": 30,
        "xG_local": 1.4,
        "xG_visitante": 1.3
    } for p in partidos]
@app.get("/api/talento/{jugador_id}")
def get_talento_detalle(jugador_id: int):
    conn = get_db()
    cur = conn.cursor()
    
    # Obtener datos del jugador
    cur.execute("""
        SELECT p.id, p.nombre, p.edad, p.posicion, p.nacionalidad, 
               t.nombre as equipo, ps.goles, ps.asistencias, ps.partidos_jugados, ps.minutos_totales
        FROM players p
        JOIN teams t ON p.equipo_id = t.id
        JOIN player_stats ps ON p.id = ps.jugador_id
        WHERE p.id = %s
    """, (jugador_id,))
    jugador = cur.fetchone()
    
    if not jugador:
        return {"error": "Jugador no encontrado"}
    
    # Obtener evolución por temporada (simulada por ahora)
    cur.execute("""
        SELECT temporada, goles, asistencias, partidos_jugados
        FROM player_season_stats
        WHERE jugador_id = %s
        ORDER BY temporada
    """, (jugador_id,))
    evolucion_db = cur.fetchall()
    
    cur.close()
    conn.close()
    
    # Si no hay evolución real, crear datos simulados para demostración
    if not evolucion_db:
        evolucion = [
            {"temporada": "2023", "partidos": 18, "goles": 4, "asistencias": 2, "productividad": 0.33, "indice": 6.2},
            {"temporada": "2024", "partidos": 28, "goles": 8, "asistencias": 4, "productividad": 0.43, "indice": 7.1},
            {"temporada": "2025", "partidos": 30, "goles": 11, "asistencias": 5, "productividad": 0.53, "indice": 8.0}
        ]
    else:
        evolucion = []
        for e in evolucion_db:
            productividad = round((e[1] + e[2]) / e[3], 2) if e[3] > 0 else 0
            indice = round(e[1] + e[2] + (e[3] * 0.1), 1)
            evolucion.append({
                "temporada": e[0],
                "partidos": e[3],
                "goles": e[1],
                "asistencias": e[2],
                "productividad": productividad,
                "indice": indice
            })
    
    id_jugador, nombre, edad, posicion, nacionalidad, equipo, goles, asistencias, partidos, minutos = jugador
    
    productividad_actual = round((goles + asistencias) / partidos, 2) if partidos > 0 else 0
    indice_actual = round(goles + asistencias + (minutos / 1000), 1)
    proyeccion = round(indice_actual * 1.3, 1)
    
    return {
        "id": id_jugador,
        "nombre": nombre,
        "edad": edad,
        "posicion": posicion,
        "nacionalidad": nacionalidad or "Desconocida",
        "equipo": equipo,
        "indice_actual": min(10, indice_actual),
        "productividad_actual": productividad_actual,
        "proyeccion": min(10, proyeccion),
        "evolucion": evolucion
    }
@app.get("/api/ligas/{nombre}")
def get_partidos_por_liga(nombre: str):
    ligas_validas = {
        "bundesliga": "Bundesliga",
        "champions": "Champions League", 
        "seriea": "Serie A",
        "ligue1": "Ligue 1"
    }
    
    if nombre not in ligas_validas:
        return {"error": "Liga no válida"}
    
    liga_bd = ligas_validas[nombre]
    conn = get_db()
    cur = conn.cursor()
    
    # Ahora incluyendo predicciones reales
    cur.execute("""
        SELECT m.id, t1.nombre as local, t2.nombre as visitante, m.fecha,
               COALESCE(p.prob_local, 40) as prob_local,
               COALESCE(p.prob_empate, 30) as prob_empate,
               COALESCE(p.prob_visitante, 30) as prob_visitante,
               COALESCE(p.xG_local, 1.4) as xG_local,
               COALESCE(p.xG_visitante, 1.3) as xG_visitante
        FROM matches m
        JOIN teams t1 ON m.local_id = t1.id
        JOIN teams t2 ON m.visitante_id = t2.id
        LEFT JOIN predictions p ON m.id = p.partido_id
        WHERE t1.liga = %s AND t2.liga = %s
        ORDER BY m.fecha
        LIMIT 50
    """, (liga_bd, liga_bd))
    
    partidos = cur.fetchall()
    cur.close()
    conn.close()

    return [{
        "id": p[0],
        "local": p[1],
        "visitante": p[2],
        "fecha": p[3],
        "estado": "Pendiente",
        "prob_local": p[4] or 40,
        "prob_empate": p[5] or 30,
        "prob_visitante": p[6] or 30,
        "xG_local": p[7] or 1.4,
        "xG_visitante": p[8] or 1.3
    } for p in partidos]
@app.get("/api/worldcup/predictions")
def get_worldcup_predictions():
    # Datos de ejemplo para el Mundial 2026
    return [
        {"id": 1, "local": "Brasil", "visitante": "Francia", "prob_local": 48, "prob_empate": 28, "prob_visitante": 24, "recomendacion": "Brasil favorito por historia"},
        {"id": 2, "local": "Argentina", "visitante": "Alemania", "prob_local": 45, "prob_empate": 30, "prob_visitante": 25, "recomendacion": "Partido muy parejo"},
    ]

@app.get("/api/knockout/predictions")
def get_knockout_predictions():
    return [
        {"id": 101, "ronda": "Octavos", "local": "Brasil", "visitante": "Portugal", "prob_local": 52, "prob_visitante": 48, "ganador_predicho": "Brasil", "fecha": "2026-07-01"},
        {"id": 102, "ronda": "Cuartos", "local": "Argentina", "visitante": "Inglaterra", "prob_local": 48, "prob_visitante": 52, "ganador_predicho": "Inglaterra", "fecha": "2026-07-05"},
    ]
@app.get("/api/worldcup/live_scores")
def get_live_scores():
    return [
        {
            "id": 1,
            "local": "🇺🇸 USA",
            "visitante": "🇲🇽 México",
            "goles_local": 2,
            "goles_visitante": 1,
            "minuto": "FT",
            "estado": "Finalizado"
        },
        {
            "id": 2,
            "local": "🇧🇷 Brasil",
            "visitante": "🇵🇹 Portugal",
            "goles_local": 0,
            "goles_visitante": 0,
            "minuto": 67,
            "estado": "En Vivo"
        }
    ]
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)