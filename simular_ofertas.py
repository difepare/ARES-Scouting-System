import psycopg2
import random
from datetime import datetime, timedelta

conn = psycopg2.connect(
    host="localhost",
    database="ares_db",
    user="postgres",
    password="Sarita2017"
)
cursor = conn.cursor()

# ============================================================
# DATOS SIMULADOS (basados en valores reales de mercado)
# ============================================================
ofertas = [
    ("Jude Bellingham", "Real Madrid", "Liverpool", 120),  # Usa el nombre exacto de tu BD
    ("Vinicius Junior", "Real Madrid", "Chelsea", 100),    # Ajusta según búsqueda
    ("Bukayo Saka", "Arsenal", "Manchester City", 90),
    ("Phil Foden", "Manchester City", "Barcelona", 85),
    ("Rodri", "Manchester City", "Barcelona", 70),
    ("Ruben Dias", "Manchester City", "Real Madrid", 65),
]

# ============================================================
# FUNCIÓN PARA OBTENER ID DE JUGADOR Y EQUIPOS
# ============================================================
def obtener_ids(jugador_nombre, equipo_origen_nombre, equipo_destino_nombre):
    cursor.execute("SELECT id FROM players WHERE nombre = %s", (jugador_nombre,))
    jugador = cursor.fetchone()
    if not jugador:
        print(f"❌ Jugador {jugador_nombre} no encontrado")
        return None, None, None
    
    cursor.execute("SELECT id FROM teams WHERE nombre = %s", (equipo_origen_nombre,))
    origen = cursor.fetchone()
    if not origen:
        print(f"❌ Equipo origen {equipo_origen_nombre} no encontrado")
        return None, None, None
    
    cursor.execute("SELECT id FROM teams WHERE nombre = %s", (equipo_destino_nombre,))
    destino = cursor.fetchone()
    if not destino:
        print(f"❌ Equipo destino {equipo_destino_nombre} no encontrado")
        return None, None, None
    
    return jugador[0], origen[0], destino[0]

# ============================================================
# INSERTAR OFERTAS
# ============================================================
for jugador, origen, destino, monto in ofertas:
    jugador_id, origen_id, destino_id = obtener_ids(jugador, origen, destino)
    if jugador_id and origen_id and destino_id:
        fecha_oferta = datetime.now() - timedelta(days=random.randint(1, 180))
        estado = random.choice(["Propuesta", "Negociación", "Aceptada", "Rechazada"])
        monto_real = monto * 1000000  # Convertir a euros
        
        cursor.execute("""
            INSERT INTO transfer_offers 
            (jugador_id, equipo_origen_id, equipo_destino_id, monto_oferta, moneda, estado, fecha_oferta, observaciones)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (jugador_id, origen_id, destino_id, monto_real, 'EUR', estado, fecha_oferta, f"Oferta simulada por {monto}M€"))
        print(f"✅ Oferta insertada: {jugador} de {origen} a {destino} por {monto}M€")

conn.commit()
cursor.close()
conn.close()
print("\n🎉 transfer_offers poblada con datos simulados.")