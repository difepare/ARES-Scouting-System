import psycopg2
import requests

# ==================================================
# CONEXIÓN A POSTGRESQL (¡CAMBIA TU CONTRASEÑA!)
# ==================================================
conn = psycopg2.connect(
    host="localhost",
    database="ares_db",
    user="postgres",
    password="Sarita2017"  # <--- CAMBIA AQUÍ TU CONTRASEÑA
)
cur = conn.cursor()

# ==================================================
# CONFIGURACIÓN DE API
# ==================================================
API_KEY = "9e346e18701e4928f7cd1eeee3d8d510"  # <--- CAMBIA AQUÍ TU CLAVE
HEADERS = {"x-rapidapi-key": API_KEY, "x-rapidapi-host": "v3.football.api-sports.io"}

LIGA_ID = 2  # Champions League
LIGA_NOMBRE = "Champions League"
TEMPORADA = "2025"

# ==================================================
# 1. VERIFICAR QUE LOS EQUIPOS EXISTEN
# ==================================================
cur.execute("SELECT COUNT(*) FROM teams WHERE liga = %s", (LIGA_NOMBRE,))
equipos_count = cur.fetchone()[0]
print(f"📊 Equipos en BD para {LIGA_NOMBRE}: {equipos_count}")

if equipos_count == 0:
    print("❌ No hay equipos. Ejecuta primero 'alimentar_ares.py' con el ID 2 para cargar los clubes.")
    exit()

# ==================================================
# 2. OBTENER PARTIDOS DESDE LA API
# ==================================================
url = "https://v3.football.api-sports.io/fixtures"
params = {"league": LIGA_ID, "season": TEMPORADA}

print(f"📡 Descargando partidos de {LIGA_NOMBRE}...")
response = requests.get(url, headers=HEADERS, params=params)

if response.status_code != 200:
    print(f"❌ Error en API: {response.status_code}")
    exit()

partidos = response.json().get('response', [])
print(f"✅ {len(partidos)} partidos descargados.")

# ==================================================
# 3. INSERTAR PARTIDOS Y PREDICCIONES
# ==================================================
insertados = 0
for p in partidos:
    local = p['teams']['home']['name']
    visitante = p['teams']['away']['name']
    fecha = p['fixture']['date']
    estado = p['fixture']['status']['short']
    goles_local = p['goals']['home'] if p['goals']['home'] is not None else None
    goles_visitante = p['goals']['away'] if p['goals']['away'] is not None else None

    # Obtener IDs de los equipos
    cur.execute("SELECT id FROM teams WHERE nombre = %s", (local,))
    local_id = cur.fetchone()
    cur.execute("SELECT id FROM teams WHERE nombre = %s", (visitante,))
    visitante_id = cur.fetchone()

    if not local_id or not visitante_id:
        print(f"⚠️ Equipo no encontrado: {local} o {visitante}")
        continue

    # Insertar partido (evitar duplicados)
    cur.execute("""
        INSERT INTO matches (local_id, visitante_id, liga, fecha, temporada, estado, goles_local, goles_visitante)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING
        RETURNING id
    """, (local_id[0], visitante_id[0], LIGA_NOMBRE, fecha, TEMPORADA, estado, goles_local, goles_visitante))
    
    partido_id = cur.fetchone()
    if not partido_id:
        print(f"⏩ Partido ya existe: {local} vs {visitante}")
        continue
    partido_id = partido_id[0]

    # Insertar predicción (valores iniciales, puedes mejorarlos después)
    cur.execute("""
        INSERT INTO predictions (partido_id, prob_local, prob_empate, prob_visitante, xG_local, xG_visitante)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (partido_id, 45.0, 30.0, 25.0, 1.6, 1.4))
    
    insertados += 1
    print(f"✅ Partido insertado: {local} vs {visitante}")

conn.commit()
print(f"\n🎉 {insertados} partidos de {LIGA_NOMBRE} guardados con sus predicciones.")

cur.close()
conn.close()