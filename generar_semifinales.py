import requests
import json

# Simular los cuartos (los cruces que ya tienes)
cuartos = [
    ("Canadá", "México"),
    ("EE.UU.", "Brasil"),
    ("Países Bajos", "Alemania"),
    ("España", "Bélgica"),
    ("Argentina", "Francia"),
    ("Inglaterra", "Portugal")
]

# Diccionario de rankings FIFA (aproximado para este ejemplo)
# (En ARES real, esto se lee de la BD)
rankings = {
    "Canadá": 45, "México": 15,
    "EE.UU.": 11, "Brasil": 1,
    "Países Bajos": 5, "Alemania": 3,
    "España": 7, "Bélgica": 4,
    "Argentina": 6, "Francia": 2,
    "Inglaterra": 9, "Portugal": 8,
}

# Función que simula un partido y devuelve el ganador
def simular_partido(local, visitante):
    rank_local = rankings[local]
    rank_visit = rankings[visitante]
    total = rank_local + rank_visit
    prob_local = (rank_visit / total) * 100
    ganador = local if prob_local > 50 else visitante
    return ganador

# Simular ganadores de cuartos
semifinales = []
resultados_cuartos = []

for local, visitante in cuartos:
    ganador = simular_partido(local, visitante)
    resultados_cuartos.append((local, visitante, ganador))
    semifinales.append(ganador)
    print(f"🏆 {local} vs {visitante} -> Gana: {ganador}")

# Construir cruces de semifinales
semis = [(semifinales[0], semifinales[1]), (semifinales[2], semifinales[3]), (semifinales[4], semifinales[5])]

# Simular semifinales
finalistas = []
resultados_semis = []

for local, visitante in semis:
    ganador = simular_partido(local, visitante)
    finalistas.append(ganador)
    resultados_semis.append((local, visitante, ganador))
    print(f"🏆 SEMIFINAL: {local} vs {visitante} -> Gana: {ganador}")

# Simular la final
final_local, final_visitante = finalistas[0], finalistas[1]
campeon = simular_partido(final_local, final_visitante)

print("\n" + "="*50)
print(f"🏆 LA GRAN FINAL: {final_local} vs {final_visitante}")
print(f"🏆 EL CAMPEÓN DEL MUNDO SEGÚN ARES ES: {campeon} 🏆")
print("="*50)