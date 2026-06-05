import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="ares_db",
    user="postgres",
    password="Sarita2017"
)
cursor = conn.cursor()

nombres_a_buscar = [
    "Jude Bellingham", "Vinicius Jr", "Vinicius Junior",
    "Bukayo Saka", "Phil Foden", "Jamal Musiala", "Rodri", "Ruben Dias"
]

for nombre in nombres_a_buscar:
    cursor.execute("SELECT id, nombre FROM players WHERE nombre ILIKE %s", (f"%{nombre}%",))
    resultados = cursor.fetchall()
    if resultados:
        for r in resultados:
            print(f"✅ '{nombre}' -> '{r[1]}' (ID {r[0]})")
    else:
        print(f"❌ '{nombre}' no encontrado en BD")

cursor.close()
conn.close()