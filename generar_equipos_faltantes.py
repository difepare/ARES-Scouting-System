import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="ares_db",
    user="postgres",
    password="Sarita2017"
)
cur = conn.cursor()

# Equipos del fixture
equipos_fixture = [
    "México", "Sudáfrica", "Corea del Sur", "República Checa",
    "Canadá", "Bosnia", "Catar", "Suiza",
    "Brasil", "Marruecos", "Haití", "Escocia",
    "EE.UU.", "Paraguay", "Australia", "Turquía",
    "Alemania", "Curazao", "Costa de Marfil", "Ecuador",
    "Países Bajos", "Japón", "Suecia", "Túnez",
    "Bélgica", "Egipto", "Irán", "Nueva Zelanda",
    "España", "Cabo Verde", "Arabia Saudita", "Uruguay",
    "Francia", "Senegal", "Irak", "Noruega",
    "Argentina", "Argelia", "Austria", "Jordania",
    "Portugal", "RD Congo", "Uzbekistán", "Colombia",
    "Inglaterra", "Croacia", "Ghana", "Panamá"
]

print("🔍 Verificando equipos en la base de datos...\n")
for equipo in equipos_fixture:
    cur.execute("SELECT id FROM national_teams WHERE nombre = %s", (equipo,))
    if cur.fetchone():
        print(f"✅ {equipo} - OK")
    else:
        print(f"❌ {equipo} - NO ENCONTRADO")

cur.close()
conn.close()