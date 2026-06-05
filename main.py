from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import psycopg2
import os
from dotenv import load_dotenv
import logging
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

# Configurar logging para ver errores en producción
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

app = FastAPI(title="ARES API", description="Advanced Real-time Evaluation System")

# Configurar CORS para producción y desarrollo
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "https://ares-football-analytics.onrender.com",
        "https://ares-web.onrender.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    """Conexión a PostgreSQL usando variables de entorno de Render"""
    database_url = os.getenv("DATABASE_URL")
    
    if database_url:
        logger.info(f"Conectando a DB con DATABASE_URL (primeros 20 chars: {database_url[:20]}...)")
        return psycopg2.connect(database_url)
    
    # Fallback para desarrollo local
    logger.info("Conectando a DB local")
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("DB_NAME", "ares_db"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "Sarita2017")
    )

# ==================================================
# ENDPOINTS PRINCIPALES
# ==================================================

@app.get("/")
def root():
    return {"message": "ARES API is running!", "version": "1.0", "status": "active"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/api/talentos_v2")
def get_talentos_v2():
    """Lista de jóvenes talentos con índice ARES"""
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            SELECT p.id, p.nombre, p.edad, p.posicion, p.nacionalidad, t.nombre as equipo,
                   COALESCE(ps.goles, 0) as goles, 
                   COALESCE(ps.asistencias, 0) as asistencias, 
                   COALESCE(ps.partidos_jugados, 1) as partidos, 
                   COALESCE(ps.minutos_totales, 0) as minutos
            FROM players p
            JOIN teams t ON p.equipo_id = t.id
            LEFT JOIN player_stats ps ON p.id = ps.jugador_id
            WHERE p.edad <= 22
            ORDER BY (COALESCE(ps.goles, 0) + COALESCE(ps.asistencias, 0)) DESC
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
    except Exception as e:
        logger.error(f"Error en /api/talentos_v2: {str(e)}")
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/api/worldcup/predictions")
def get_worldcup_predictions():
    """Mundial USA 2026 - Grupos completos"""
    partidos = []
    partido_id = 1
    
    grupos = {
        "🇦 Grupo A": [
            {"local": "🇲🇽 México", "visitante": "🇿🇦 Sudáfrica", "prob_local": 55, "prob_empate": 25, "prob_visitante": 20},
            {"local": "🇰🇷 Corea del Sur", "visitante": "🇨🇿 Chequia", "prob_local": 45, "prob_empate": 30, "prob_visitante": 25},
            {"local": "🇨🇿 Chequia", "visitante": "🇿🇦 Sudáfrica", "prob_local": 48, "prob_empate": 28, "prob_visitante": 24},
            {"local": "🇲🇽 México", "visitante": "🇰🇷 Corea del Sur", "prob_local": 52, "prob_empate": 27, "prob_visitante": 21},
        ],
        "🇧 Grupo B": [
            {"local": "🇨🇦 Canadá", "visitante": "🇧🇦 Bosnia", "prob_local": 53, "prob_empate": 26, "prob_visitante": 21},
            {"local": "🇶🇦 Qatar", "visitante": "🇨🇭 Suiza", "prob_local": 35, "prob_empate": 28, "prob_visitante": 37},
            {"local": "🇨🇭 Suiza", "visitante": "🇧🇦 Bosnia", "prob_local": 50, "prob_empate": 28, "prob_visitante": 22},
            {"local": "🇨🇦 Canadá", "visitante": "🇶🇦 Qatar", "prob_local": 48, "prob_empate": 27, "prob_visitante": 25},
        ],
        "🇨 Grupo C": [
            {"local": "🇧🇷 Brasil", "visitante": "🇲🇦 Marruecos", "prob_local": 58, "prob_empate": 24, "prob_visitante": 18},
            {"local": "🇭🇹 Haití", "visitante": "🏴󠁧󠁢󠁳󠁣󠁴󠁿 Escocia", "prob_local": 30, "prob_empate": 28, "prob_visitante": 42},
            {"local": "🏴󠁧󠁢󠁳󠁣󠁴󠁿 Escocia", "visitante": "🇲🇦 Marruecos", "prob_local": 40, "prob_empate": 30, "prob_visitante": 30},
            {"local": "🇧🇷 Brasil", "visitante": "🇭🇹 Haití", "prob_local": 70, "prob_empate": 18, "prob_visitante": 12},
        ],
        "🇩 Grupo D": [
            {"local": "🇺🇸 USA", "visitante": "🇵🇾 Paraguay", "prob_local": 55, "prob_empate": 26, "prob_visitante": 19},
            {"local": "🇦🇺 Australia", "visitante": "🇹🇷 Turquía", "prob_local": 38, "prob_empate": 28, "prob_visitante": 34},
            {"local": "🇺🇸 USA", "visitante": "🇦🇺 Australia", "prob_local": 56, "prob_empate": 25, "prob_visitante": 19},
            {"local": "🇹🇷 Turquía", "visitante": "🇵🇾 Paraguay", "prob_local": 48, "prob_empate": 27, "prob_visitante": 25},
        ],
        "🇪 Grupo E": [
            {"local": "🇨🇮 Costa de Marfil", "visitante": "🇪🇨 Ecuador", "prob_local": 42, "prob_empate": 30, "prob_visitante": 28},
            {"local": "🇩🇪 Alemania", "visitante": "🇨🇼 Curazao", "prob_local": 72, "prob_empate": 18, "prob_visitante": 10},
            {"local": "🇩🇪 Alemania", "visitante": "🇨🇮 Costa de Marfil", "prob_local": 58, "prob_empate": 24, "prob_visitante": 18},
            {"local": "🇪🇨 Ecuador", "visitante": "🇨🇼 Curazao", "prob_local": 55, "prob_empate": 26, "prob_visitante": 19},
        ],
        "🇫 Grupo F": [
            {"local": "🇳🇱 Países Bajos", "visitante": "🇯🇵 Japón", "prob_local": 54, "prob_empate": 26, "prob_visitante": 20},
            {"local": "🇸🇪 Suecia", "visitante": "🇹🇳 Túnez", "prob_local": 48, "prob_empate": 28, "prob_visitante": 24},
            {"local": "🇳🇱 Países Bajos", "visitante": "🇸🇪 Suecia", "prob_local": 50, "prob_empate": 27, "prob_visitante": 23},
        ],
        "🇬 Grupo G": [
            {"local": "🇧🇪 Bélgica", "visitante": "🇪🇬 Egipto", "prob_local": 52, "prob_empate": 27, "prob_visitante": 21},
            {"local": "🇮🇷 Irán", "visitante": "🇳🇿 Nueva Zelanda", "prob_local": 48, "prob_empate": 28, "prob_visitante": 24},
        ],
        "🇭 Grupo H": [
            {"local": "🇪🇸 España", "visitante": "🇨🇻 Cabo Verde", "prob_local": 65, "prob_empate": 22, "prob_visitante": 13},
            {"local": "🇸🇦 Arabia Saudita", "visitante": "🇺🇾 Uruguay", "prob_local": 30, "prob_empate": 28, "prob_visitante": 42},
        ],
        "🇮 Grupo I": [
            {"local": "🇫🇷 Francia", "visitante": "🇸🇳 Senegal", "prob_local": 55, "prob_empate": 25, "prob_visitante": 20},
            {"local": "🇮🇶 Irak", "visitante": "🇳🇴 Noruega", "prob_local": 32, "prob_empate": 28, "prob_visitante": 40},
        ],
        "🇯 Grupo J": [
            {"local": "🇦🇷 Argentina", "visitante": "🇩🇿 Argelia", "prob_local": 58, "prob_empate": 24, "prob_visitante": 18},
            {"local": "🇦🇹 Austria", "visitante": "🇯🇴 Jordania", "prob_local": 48, "prob_empate": 28, "prob_visitante": 24},
        ],
        "🇰 Grupo K": [
            {"local": "🇵🇹 Portugal", "visitante": "🇨🇩 RD Congo", "prob_local": 56, "prob_empate": 25, "prob_visitante": 19},
            {"local": "🇺🇿 Uzbekistán", "visitante": "🇨🇴 Colombia", "prob_local": 28, "prob_empate": 27, "prob_visitante": 45},
        ],
        "🇱 Grupo L": [
            {"local": "🏴󠁧󠁢󠁥󠁮󠁧󠁿 Inglaterra", "visitante": "🇭🇷 Croacia", "prob_local": 48, "prob_empate": 29, "prob_visitante": 23},
            {"local": "🇬🇭 Ghana", "visitante": "🇵🇦 Panamá", "prob_local": 46, "prob_empate": 28, "prob_visitante": 26},
        ],
    }
    
    for grupo, matches in grupos.items():
        for match in matches:
            favorito = match["local"] if match["prob_local"] > match["prob_visitante"] else match["visitante"]
            partidos.append({
                "id": partido_id,
                "grupo": grupo,
                "local": match["local"],
                "visitante": match["visitante"],
                "prob_local": match["prob_local"],
                "prob_empate": match["prob_empate"],
                "prob_visitante": match["prob_visitante"],
                "recomendacion": f"🔮 ARES predice: {favorito} favorito"
            })
            partido_id += 1
    
    return partidos

@app.get("/api/knockout/predictions")
def get_knockout_predictions():
    return [
        {"id": 101, "ronda": "Octavos", "local": "🇧🇷 Brasil", "visitante": "🇨🇴 Colombia", "prob_local": 55, "prob_visitante": 45, "ganador_predicho": "🇧🇷 Brasil", "fecha": "2026-07-01"},
        {"id": 102, "ronda": "Octavos", "local": "🇦🇷 Argentina", "visitante": "🇺🇾 Uruguay", "prob_local": 52, "prob_visitante": 48, "ganador_predicho": "🇦🇷 Argentina", "fecha": "2026-07-02"},
        {"id": 103, "ronda": "Cuartos", "local": "🇧🇷 Brasil", "visitante": "🇦🇷 Argentina", "prob_local": 48, "prob_visitante": 52, "ganador_predicho": "🇦🇷 Argentina", "fecha": "2026-07-08"},
        {"id": 104, "ronda": "Semis", "local": "🇦🇷 Argentina", "visitante": "🇫🇷 Francia", "prob_local": 47, "prob_visitante": 53, "ganador_predicho": "🇫🇷 Francia", "fecha": "2026-07-13"},
        {"id": 105, "ronda": "Final", "local": "🇫🇷 Francia", "visitante": "🇪🇸 España", "prob_local": 51, "prob_visitante": 49, "ganador_predicho": "🇫🇷 Francia", "fecha": "2026-07-19"},
    ]

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
    
    # Por ahora devolvemos datos de ejemplo mientras la BD se llena
    return [
        {"id": 1, "local": "Bayern Munich", "visitante": "Borussia Dortmund", "fecha": "2025-12-15", "estado": "Pendiente", "prob_local": 55, "prob_empate": 25, "prob_visitante": 20, "xG_local": 2.1, "xG_visitante": 1.4},
        {"id": 2, "local": "Bayer Leverkusen", "visitante": "RB Leipzig", "fecha": "2025-12-16", "estado": "Pendiente", "prob_local": 48, "prob_empate": 27, "prob_visitante": 25, "xG_local": 1.8, "xG_visitante": 1.6},
    ]

@app.get("/api/jugadores")
def get_jugadores():
    return [
        {"nombre": "Harry Kane", "equipo": "Bayern Munich", "goles": 18},
        {"nombre": "Victor Osimhen", "equipo": "Napoli", "goles": 15},
        {"nombre": "Kylian Mbappé", "equipo": "Real Madrid", "goles": 14},
        {"nombre": "Erling Haaland", "equipo": "Manchester City", "goles": 13},
        {"nombre": "Lautaro Martínez", "equipo": "Inter", "goles": 12},
    ]

@app.get("/api/ofertas")
def get_ofertas():
    return [
        {"jugador": "Endrick", "origen": "Palmeiras", "destino": "Real Madrid", "monto": 35000000},
        {"jugador": "Lamine Yamal", "origen": "Barcelona", "destino": "Paris SG", "monto": 120000000},
        {"jugador": "Alejandro Garnacho", "origen": "Manchester United", "destino": "Napoli", "monto": 45000000},
    ]

@app.get("/api/talento/{jugador_id}")
def get_talento_detalle(jugador_id: int):
    # Datos de ejemplo para demostración
    jugadores_ejemplo = {
        1: {"nombre": "Endrick", "edad": 18, "posicion": "Delantero", "nacionalidad": "Brasil", "equipo": "Real Madrid", "indice_actual": 8.4, "productividad_actual": 0.57, "proyeccion": 9.5},
        2: {"nombre": "Lamine Yamal", "edad": 17, "posicion": "Extremo", "nacionalidad": "España", "equipo": "Barcelona", "indice_actual": 8.1, "productividad_actual": 0.52, "proyeccion": 9.2},
        3: {"nombre": "Alejandro Garnacho", "edad": 20, "posicion": "Extremo", "nacionalidad": "Argentina", "equipo": "Manchester United", "indice_actual": 7.6, "productividad_actual": 0.48, "proyeccion": 8.9},
    }
    
    if jugador_id in jugadores_ejemplo:
        jugador = jugadores_ejemplo[jugador_id]
        jugador["id"] = jugador_id
        jugador["evolucion"] = [
            {"temporada": "2023", "partidos": 18, "goles": 4, "asistencias": 2, "productividad": 0.33, "indice": 6.2},
            {"temporada": "2024", "partidos": 28, "goles": 8, "asistencias": 4, "productividad": 0.43, "indice": 7.1},
            {"temporada": "2025", "partidos": 30, "goles": 11, "asistencias": 5, "productividad": 0.53, "indice": 8.0}
        ]
        return jugador
    
    return {"error": "Jugador no encontrado"}

@app.get("/api/worldcup/live_scores")
def get_live_scores():
    return [
        {"id": 1, "local": "🇺🇸 USA", "visitante": "🇲🇽 México", "goles_local": 2, "goles_visitante": 1, "minuto": "FT", "estado": "Finalizado"},
        {"id": 2, "local": "🇧🇷 Brasil", "visitante": "🇵🇹 Portugal", "goles_local": 0, "goles_visitante": 0, "minuto": 67, "estado": "En Vivo"},
        {"id": 3, "local": "🇫🇷 Francia", "visitante": "🇦🇷 Argentina", "goles_local": 1, "goles_visitante": 1, "minuto": 55, "estado": "En Vivo"},
    ]

@app.get("/api/partidos_ares")
def get_partidos_ares():
    return [
        {"id": 1, "local": "Real Madrid", "visitante": "Barcelona", "fecha": "2025-12-20", "estado": "Pendiente", "prob_local": 48, "prob_empate": 27, "prob_visitante": 25, "xG_local": 1.9, "xG_visitante": 1.8},
        {"id": 2, "local": "Manchester City", "visitante": "Liverpool", "fecha": "2025-12-21", "estado": "Pendiente", "prob_local": 52, "prob_empate": 25, "prob_visitante": 23, "xG_local": 2.1, "xG_visitante": 1.7},
    ]
frontend_dist = os.path.join(os.path.dirname(__file__), "frontend", "dist")
if os.path.exists(frontend_dist):
    app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dist, "assets")), name="assets")
    
    @app.get("/{full_path:path}")
    async def serve_react(full_path: str):
        if full_path.startswith("api/"):
            # Dejar que los endpoints API manejen esto
            return JSONResponse(status_code=404, content={"error": "Not found"})
        return FileResponse(os.path.join(frontend_dist, "index.html"))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)