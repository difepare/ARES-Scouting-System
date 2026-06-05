import psycopg2
from datetime import datetime, timedelta

# --- ¡CAMBIA ESTO POR TU CONTRASEÑA! ---
conn = psycopg2.connect(
    host="localhost",
    database="ares_db",
    user="postgres",
    password="Sarita2017"
)
cur = conn.cursor()

# Borramos predicciones y partidos antiguos para empezar limpios
cur.execute("DELETE FROM world_cup_predictions;")
cur.execute("DELETE FROM world_cup_matches;")
print("🗑️ Datos antiguos eliminados.")

# --- FUNCIÓN PARA INSERTAR PARTIDOS DE UN GRUPO ---
def insertar_partidos_grupo(grupo_letra, equipos, fecha_inicio):
    for i in range(len(equipos)):
        for j in range(i+1, len(equipos)):
            cur.execute("SELECT id FROM national_teams WHERE nombre = %s", (equipos[i],))
            local = cur.fetchone()
            cur.execute("SELECT id FROM national_teams WHERE nombre = %s", (equipos[j],))
            visit = cur.fetchone()

            if local and visit:
                cur.execute("""
                    INSERT INTO world_cup_matches (local_id, visitante_id, grupo, fecha, estadio, ciudad)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (local[0], visit[0], grupo_letra, fecha_inicio, "Estadio Ejemplo", "Ciudad Ejemplo"))
                print(f"📅 Partido {equipos[i]} vs {equipos[j]} ({grupo_letra}) agregado")
                fecha_inicio += timedelta(days=2)
            else:
                print(f"⚠️ Error: No se encontró a {equipos[i]} o {equipos[j]}")
    return fecha_inicio

# --- TODOS LOS GRUPOS (Equipos confirmados) ---
grupo_a = ["México", "Sudáfrica", "Corea del Sur", "República Checa"]
grupo_b = ["Canadá", "Bosnia", "Catar", "Suiza"]
grupo_c = ["Brasil", "Marruecos", "Haití", "Escocia"]
grupo_d = ["EE.UU.", "Paraguay", "Australia", "Turquía"]
grupo_e = ["Alemania", "Curazao", "Costa de Marfil", "Ecuador"]
grupo_f = ["Países Bajos", "Japón", "Túnez", "Suecia"]
grupo_g = ["Bélgica", "Egipto", "Irán", "Nueva Zelanda"]
grupo_h = ["España", "Cabo Verde", "Arabia Saudita", "Uruguay"]
grupo_i = ["Francia", "Senegal", "Irak", "Noruega"]
grupo_j = ["Argentina", "Argelia", "Austria", "Jordania"]
grupo_k = ["Portugal", "RD Congo", "Uzbekistán", "Colombia"]
grupo_l = ["Inglaterra", "Croacia", "Ghana", "Panamá"]

fecha_base = datetime(2026, 6, 11, 15, 0)  # 11 de junio, partido inaugural

fecha_base = insertar_partidos_grupo("A", grupo_a, fecha_base)
fecha_base = insertar_partidos_grupo("B", grupo_b, fecha_base)
fecha_base = insertar_partidos_grupo("C", grupo_c, fecha_base)
fecha_base = insertar_partidos_grupo("D", grupo_d, fecha_base)
fecha_base = insertar_partidos_grupo("E", grupo_e, fecha_base)
fecha_base = insertar_partidos_grupo("F", grupo_f, fecha_base)
fecha_base = insertar_partidos_grupo("G", grupo_g, fecha_base)
fecha_base = insertar_partidos_grupo("H", grupo_h, fecha_base)
fecha_base = insertar_partidos_grupo("I", grupo_i, fecha_base)
fecha_base = insertar_partidos_grupo("J", grupo_j, fecha_base)
fecha_base = insertar_partidos_grupo("K", grupo_k, fecha_base)
fecha_base = insertar_partidos_grupo("L", grupo_l, fecha_base)

conn.commit()
cur.close()
conn.close()
print("🎉 Mundial 2026: ¡104 partidos cargados en ARES!")