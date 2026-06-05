import asyncio
from tmkt import TMKT
import psycopg2
from datetime import datetime
import re

DB_CONFIG = {
    "host": "localhost",
    "database": "ares_db",
    "user": "postgres",
    "password": "Sarita2017"
}

async def get_transfermarkt_data(player_name: str):
    async with TMKT() as tmkt:
        print(f"🔍 Buscando a '{player_name}' en Transfermarkt...")
        search_results = await tmkt.player_search(player_name)
        
        if not search_results:
            print(f"❌ No se encontró a '{player_name}'.")
            return None
        
        player_id = search_results[0]['id']
        print(f"   ✅ Encontrado (ID: {player_id}). Obteniendo detalles...")
        
        player_data = await tmkt.get_player(player_id)
        
        # La información real está dentro de 'data'
        if player_data and 'data' in player_data:
            return player_data['data']
        return None

def update_player_in_db(player_data: dict, search_name: str):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    
    # Extraer nombre (está en 'name' directamente dentro de data)
    nombre = player_data.get('name', search_name)
    
    # Extraer valor de mercado (estructura anidada)
    market_value = None
    market_data = player_data.get('marketValueDetails', {})
    current = market_data.get('current', {})
    compact = current.get('compact', {})
    if compact and 'content' in compact:
        try:
            # El contenido viene como "200.00" (ya limpio)
            market_value = float(compact['content'])
        except (ValueError, TypeError):
            market_value = None
    
    # Extraer URL
    url = player_data.get('relativeUrl', '')
    if url and not url.startswith('http'):
        url = f"https://www.transfermarkt.com{url}"
    
    print(f"\n📊 DATOS A ACTUALIZAR:")
    print(f"   Nombre: {nombre}")
    print(f"   Valor de mercado: {market_value}M€")
    print(f"   URL: {url}")
    
    # Actualizar la base de datos
    sql = """
        UPDATE players 
        SET market_value = %s, 
            transfermarkt_url = %s,
            updated_at = %s
        WHERE nombre ILIKE %s
    """
    cur.execute(sql, (market_value, url, datetime.now(), f"%{search_name}%"))
    conn.commit()
    
    print(f"💾 Actualizado el registro que coincida con '{search_name}'")

    cur.close()
    conn.close()

async def main():
    # Puedes cambiar el nombre aquí para probar con otros jugadores
    jugadores_a_buscar = ["Lamine Yamal", "Endrick", "Alejandro Garnacho"]
    
    for nombre in jugadores_a_buscar:
        player_info = await get_transfermarkt_data(nombre)
        if player_info:
            update_player_in_db(player_info, nombre)
        else:
            print(f"No se pudo obtener la información de {nombre}.")
        print("-" * 50)

if __name__ == "__main__":
    asyncio.run(main())