import psycopg2
import requests
from datetime import datetime

# ==================================================
# CONEXIÓN A POSTGRESQL (¡CAMBIA TU CONTRASEÑA!)
# ==================================================
conn = psycopg2.connect(
    host="localhost",
    database="ares_db",
    user="postgres",
    password="Sarita2017"  # <--- CAMBIA AQUÍ
)
cur = conn.cursor()

# ==================================================
# CONFIGURACIÓN DE API
# ==================================================
API_KEY = "9e346e18701e4928f7cd1eeee3d8d510"  # <--- CAMBIA AQUÍ
HEADERS = {"x-rapidapi-key": API_KEY, "x-rapidapi-host": "v3.football.api-sports.io"}

# Lista de ligas a procesar: (ID, Nombre, Temporada)
LIGAS = [
    (135, "Serie A", "2025"),
    (61, "Ligue 1", "2025"),
    (71, "Brasileirão", "2025"),   # NUEVO
    (128, "Liga Argentina", "2025"), # NUEVO
    (88, "Eredivisie", "2025")      # NUEVO
]

# ==================================================
# PROCESAR CADA LIGA
# ==================================================
for liga_id, liga_nombre, temporada in LIGAS:
    print(f"\n📌 Procesando {liga_nombre} (ID {liga_id})...")
    
    # 1. Verificar que los equipos existen
    cur.execute("SELECT COUNT(*) FROM teams WHERE liga = %s", (liga_nombre,))
    equipos_count = cur.fetchone()[0]
    if equipos_count == 0:
        print(f"❌ No hay equipos para {liga_nombre}. Ejecuta primero 'alimentar_ares.py'.")
        continue
    
    # 2. Obtener partidos desde la API
    url = "https://v3.football.api-sports.io/fixtures"
    params = {"league": liga_id, "season": temporada}
    response = requests.get(url, headers=HEADERS, params=params)
    
    if response.status_code != 200:
        print(f"❌ Error en API para {liga_nombre}: {response.status_code}")
        continue
    
    partidos = response.json().get('response', [])
    print(f"✅ {len(partidos)} partidos descargados.")
    
    # 3. Insertar partidos y predicciones
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
        
        # Insertar partido
        cur.execute("""
            INSERT INTO matches (local_id, visitante_id, liga, fecha, temporada, estado, goles_local, goles_visitante)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING
            RETURNING id
        """, (local_id[0], visitante_id[0], liga_nombre, fecha, temporada, estado, goles_local, goles_visitante))
        
        partido_id = cur.fetchone()
        if not partido_id:
            continue
        partido_id = partido_id[0]
        
        # Insertar predicción (valores iniciales, luego se actualizarán con el ranking ARES)
        cur.execute("""
            INSERT INTO predictions (partido_id, prob_local, prob_empate, prob_visitante, xG_local, xG_visitante)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (partido_id, 45.0, 30.0, 25.0, 1.5, 1.3))
        
        insertados += 1
        if insertados % 50 == 0:
            print(f"   {insertados} partidos insertados...")
    
    conn.commit()
    print(f"🎉 {liga_nombre}: {insertados} partidos guardados con predicciones iniciales.")

cur.close()
conn.close()
print("\n✅ Serie A y Ligue 1 cargadas exitosamente.")