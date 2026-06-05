import asyncio
import psycopg2
from datetime import datetime
import yagmail

# --- CONFIGURACIÓN DE EMAIL (¡CAMBIA ESTOS DATOS!) ---
EMAIL_ARES = "diegof.palomino@gmail.com"          # El correo que usará ARES para enviar
PASSWORD_APP = "ylcu nrbn fezd szrl"       # La contraseña de 16 dígitos que generaste
EMAIL_DESTINO = "diegof.palomino@gmail.com" # Tu correo personal para recibir alertas
# -------------------------------------------------------

def enviar_alerta_email(jugador):
    """Envía un correo si el jugador es un CRACK MUNDIAL"""
    try:
        yag = yagmail.SMTP(EMAIL_ARES, PASSWORD_APP)
        subject = f"⚽ NUEVO TALENTO DE ÉLITE: {jugador['nombre']}"
        contents = f"""
        <h2>🌟 ARES ha detectado una nueva estrella</h2>
        <p><b>Nombre:</b> {jugador['nombre']}</p>
        <p><b>Edad:</b> {jugador['edad']} años</p>
        <p><b>Posición:</b> {jugador['posicion']}</p>
        <p><b>Equipo:</b> {jugador['equipo']}</p>
        <p><b>Índice ARES:</b> {jugador['indice_talento']} / 10</p>
        <p><b>Valor estimado:</b> {jugador['valor_mercado']}M€</p>
        <br>
        <p><a href="http://localhost:5173/talento/{jugador['id']}">👉 Ver perfil completo en ARES</a></p>
        <hr>
        <p><i>ARES - Advanced Real-time Evaluation System</i></p>
        """
        yag.send(to=EMAIL_DESTINO, subject=subject, contents=contents)
        print(f"   📧 Alerta enviada para {jugador['nombre']}")
    except Exception as e:
        print(f"   ❌ Error al enviar email para {jugador['nombre']}: {e}")

async def actualizar_talentos():
    """Actualiza valores y envía alertas para nuevos talentos élite"""
    conn = psycopg2.connect(
        host="localhost",
        database="ares_db",
        user="postgres",
        password="Sarita2017"
    )
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

    for j in jugadores:
        id_jugador, nombre, edad, posicion, nacionalidad, equipo, goles, asistencias, partidos, minutos = j
        indice = round((goles + asistencias) + (minutos / 1000), 1)
        
        # Si es un CRACK MUNDIAL (índice >= 7), se envía el correo
        if indice >= 7:
            valor_mercado = round(indice * 3, 1)
            jugador_data = {
                "id": id_jugador, "nombre": nombre, "edad": edad,
                "posicion": posicion, "equipo": equipo,
                "indice_talento": indice, "valor_mercado": valor_mercado
            }
            enviar_alerta_email(jugador_data)

# ... (El resto de tu script de actualización, como `actualizar_partidos_recientes`, sigue igual)

async def main():
    print("🚀 ARES - Iniciando actualización diaria...")
    await actualizar_talentos()  # Esta línea ahora también envía correos
    print("✅ ARES actualizado correctamente.")

if __name__ == "__main__":
    asyncio.run(main())