import psycopg2
from datetime import datetime

conn = psycopg2.connect(
    host="localhost",
    database="ares_db",
    user="postgres",
    password="Sarita2017"
)
cur = conn.cursor()

def get_team_id(nombre):
    cur.execute("SELECT id FROM national_teams WHERE nombre ILIKE %s", (nombre,))
    result = cur.fetchone()
    if not result:
        # Buscar por coincidencia aproximada
        cur.execute("SELECT id, nombre FROM national_teams WHERE nombre ILIKE %s", (f"%{nombre}%",))
        result = cur.fetchone()
        if result:
            print(f"   ⚠️ Coincidencia aproximada: '{nombre}' -> '{result[1]}' (ID {result[0]})")
            return result[0]
    return result[0] if result else None

# Fixture completo
partidos = [
    # Grupo A
    (1, "México", "Sudáfrica", "2026-06-11 15:00:00", "Estadio Azteca", "Ciudad de México"),
    (1, "Corea del Sur", "República Checa", "2026-06-11 21:00:00", "Estadio Akron", "Guadalajara"),
    (1, "República Checa", "Sudáfrica", "2026-06-18 12:00:00", "Mercedes-Benz Stadium", "Atlanta"),
    (1, "México", "Corea del Sur", "2026-06-18 21:00:00", "Estadio Akron", "Guadalajara"),
    (1, "República Checa", "México", "2026-06-24 21:00:00", "Estadio Azteca", "Ciudad de México"),
    (1, "Sudáfrica", "Corea del Sur", "2026-06-24 21:00:00", "Estadio BBVA", "Monterrey"),
    
    # Grupo B
    (1, "Canadá", "Bosnia", "2026-06-12 15:00:00", "BMO Field", "Toronto"),
    (1, "Catar", "Suiza", "2026-06-13 15:00:00", "Levi's Stadium", "Santa Clara"),
    (1, "Suiza", "Bosnia", "2026-06-18 15:00:00", "SoFi Stadium", "Los Ángeles"),
    (1, "Canadá", "Catar", "2026-06-18 18:00:00", "BC Place", "Vancouver"),
    (1, "Suiza", "Canadá", "2026-06-24 15:00:00", "BC Place", "Vancouver"),
    (1, "Bosnia", "Catar", "2026-06-24 15:00:00", "Lumen Field", "Seattle"),
    
    # Grupo C
    (1, "Brasil", "Marruecos", "2026-06-13 18:00:00", "MetLife Stadium", "Nueva Jersey"),
    (1, "Haití", "Escocia", "2026-06-13 21:00:00", "Gillette Stadium", "Foxborough"),
    (1, "Escocia", "Marruecos", "2026-06-19 18:00:00", "Gillette Stadium", "Foxborough"),
    (1, "Brasil", "Haití", "2026-06-19 21:00:00", "Lincoln Financial Field", "Filadelfia"),
    (1, "Escocia", "Brasil", "2026-06-24 18:00:00", "Hard Rock Stadium", "Miami"),
    (1, "Marruecos", "Haití", "2026-06-24 18:00:00", "Mercedes-Benz Stadium", "Atlanta"),
    
    # Grupo D
    (1, "EE.UU.", "Paraguay", "2026-06-12 21:00:00", "SoFi Stadium", "Los Ángeles"),
    (1, "Australia", "Turquía", "2026-06-13 00:00:00", "BC Place", "Vancouver"),
    (1, "Turquía", "Paraguay", "2026-06-19 00:00:00", "Levi's Stadium", "Santa Clara"),
    (1, "EE.UU.", "Australia", "2026-06-19 15:00:00", "Lumen Field", "Seattle"),
    (1, "Turquía", "EE.UU.", "2026-06-25 22:00:00", "SoFi Stadium", "Los Ángeles"),
    (1, "Paraguay", "Australia", "2026-06-25 22:00:00", "Levi's Stadium", "Santa Clara"),
    
    # Grupo E
    (1, "Alemania", "Curazao", "2026-06-14 13:00:00", "NRG Stadium", "Houston"),
    (1, "Costa de Marfil", "Ecuador", "2026-06-14 19:00:00", "Lincoln Financial Field", "Filadelfia"),
    (1, "Alemania", "Costa de Marfil", "2026-06-20 16:00:00", "BMO Field", "Toronto"),
    (1, "Ecuador", "Curazao", "2026-06-20 20:00:00", "Arrowhead Stadium", "Kansas City"),
    (1, "Ecuador", "Alemania", "2026-06-25 16:00:00", "MetLife Stadium", "Nueva Jersey"),
    (1, "Curazao", "Costa de Marfil", "2026-06-25 16:00:00", "Lincoln Financial Field", "Filadelfia"),
    
    # Grupo F
    (1, "Países Bajos", "Japón", "2026-06-14 16:00:00", "AT&T Stadium", "Arlington"),
    (1, "Suecia", "Túnez", "2026-06-14 22:00:00", "Estadio BBVA", "Monterrey"),
    (1, "Países Bajos", "Suecia", "2026-06-20 13:00:00", "NRG Stadium", "Houston"),
    (1, "Túnez", "Japón", "2026-06-20 00:00:00", "Estadio BBVA", "Monterrey"),
    (1, "Túnez", "Países Bajos", "2026-06-25 19:00:00", "AT&T Stadium", "Arlington"),
    (1, "Japón", "Suecia", "2026-06-25 19:00:00", "Arrowhead Stadium", "Kansas City"),
    
    # Grupo G
    (1, "Bélgica", "Egipto", "2026-06-15 15:00:00", "Lumen Field", "Seattle"),
    (1, "Irán", "Nueva Zelanda", "2026-06-15 21:00:00", "SoFi Stadium", "Los Ángeles"),
    (1, "Bélgica", "Irán", "2026-06-21 15:00:00", "SoFi Stadium", "Los Ángeles"),
    (1, "Nueva Zelanda", "Egipto", "2026-06-21 21:00:00", "BC Place", "Vancouver"),
    (1, "Nueva Zelanda", "Bélgica", "2026-06-26 23:00:00", "BC Place", "Vancouver"),
    (1, "Egipto", "Irán", "2026-06-26 23:00:00", "Lumen Field", "Seattle"),
    
    # Grupo H
    (1, "España", "Cabo Verde", "2026-06-15 12:00:00", "Mercedes-Benz Stadium", "Atlanta"),
    (1, "Arabia Saudita", "Uruguay", "2026-06-15 18:00:00", "Hard Rock Stadium", "Miami"),
    (1, "España", "Arabia Saudita", "2026-06-21 12:00:00", "Mercedes-Benz Stadium", "Atlanta"),
    (1, "Uruguay", "Cabo Verde", "2026-06-21 18:00:00", "Hard Rock Stadium", "Miami"),
    (1, "Uruguay", "España", "2026-06-26 20:00:00", "NRG Stadium", "Houston"),
    (1, "Cabo Verde", "Arabia Saudita", "2026-06-26 20:00:00", "Estadio Akron", "Guadalajara"),
    
    # Grupo I
    (1, "Francia", "Senegal", "2026-06-16 15:00:00", "MetLife Stadium", "Nueva Jersey"),
    (1, "Irak", "Noruega", "2026-06-16 18:00:00", "Gillette Stadium", "Foxborough"),
    (1, "Francia", "Irak", "2026-06-22 17:00:00", "Lincoln Financial Field", "Filadelfia"),
    (1, "Noruega", "Senegal", "2026-06-22 20:00:00", "MetLife Stadium", "Nueva Jersey"),
    (1, "Noruega", "Francia", "2026-06-26 15:00:00", "Gillette Stadium", "Foxborough"),
    (1, "Senegal", "Irak", "2026-06-26 15:00:00", "BMO Field", "Toronto"),
    
    # Grupo J
    (1, "Argentina", "Argelia", "2026-06-16 21:00:00", "Arrowhead Stadium", "Kansas City"),
    (1, "Austria", "Jordania", "2026-06-16 00:00:00", "Levi's Stadium", "Santa Clara"),
    (1, "Argentina", "Austria", "2026-06-22 13:00:00", "AT&T Stadium", "Arlington"),
    (1, "Jordania", "Argelia", "2026-06-22 23:00:00", "Levi's Stadium", "Santa Clara"),
    (1, "Jordania", "Argentina", "2026-06-27 22:00:00", "AT&T Stadium", "Arlington"),
    (1, "Argelia", "Austria", "2026-06-27 22:00:00", "Arrowhead Stadium", "Kansas City"),
    
    # Grupo K
    (1, "Portugal", "RD Congo", "2026-06-17 13:00:00", "NRG Stadium", "Houston"),
    (1, "Uzbekistán", "Colombia", "2026-06-17 22:00:00", "Estadio Azteca", "Ciudad de México"),
    (1, "Portugal", "Uzbekistán", "2026-06-23 13:00:00", "NRG Stadium", "Houston"),
    (1, "Colombia", "RD Congo", "2026-06-23 22:00:00", "Estadio Akron", "Guadalajara"),
    (1, "Colombia", "Portugal", "2026-06-27 19:30:00", "Hard Rock Stadium", "Miami"),
    (1, "RD Congo", "Uzbekistán", "2026-06-27 19:30:00", "Mercedes-Benz Stadium", "Atlanta"),
    
    # Grupo L
    (1, "Inglaterra", "Croacia", "2026-06-17 16:00:00", "AT&T Stadium", "Arlington"),
    (1, "Ghana", "Panamá", "2026-06-17 19:00:00", "BMO Field", "Toronto"),
    (1, "Inglaterra", "Ghana", "2026-06-23 16:00:00", "Gillette Stadium", "Foxborough"),
    (1, "Panamá", "Croacia", "2026-06-23 19:00:00", "BMO Field", "Toronto"),
    (1, "Panamá", "Inglaterra", "2026-06-27 17:00:00", "MetLife Stadium", "Nueva Jersey"),
    (1, "Croacia", "Ghana", "2026-06-27 17:00:00", "Lincoln Financial Field", "Filadelfia"),
]

print("🚀 Insertando partidos uno por uno...\n")

insertados = 0
for p in partidos:
    grupo, local, visitante, fecha, estadio, ciudad = p
    
    local_id = get_team_id(local)
    visitante_id = get_team_id(visitante)
    
    if local_id and visitante_id:
        try:
            cur.execute("""
                INSERT INTO world_cup_matches (local_id, visitante_id, grupo, fecha, estadio, ciudad)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (local_id, visitante_id, grupo, fecha, estadio, ciudad))
            insertados += 1
            print(f"✅ {insertados:3d}. {local} vs {visitante}")
        except Exception as e:
            print(f"❌ Error: {local} vs {visitante} - {e}")
    else:
        print(f"⚠️ No se pudo insertar: {local} vs {visitante} (local_id={local_id}, visitante_id={visitante_id})")

conn.commit()
cur.close()
conn.close()

print(f"\n🎉 {insertados} partidos del Mundial 2026 cargados correctamente.")