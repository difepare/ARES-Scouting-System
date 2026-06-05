import asyncio
from tmkt import TMKT
import psycopg2
from datetime import datetime

DB_CONFIG = {
    "host": "localhost",
    "database": "ares_db",
    "user": "postgres",
    "password": "Sarita2017"
}

async def get_market_value(player_name: str):
    async with TMKT() as tmkt:
        try:
            search_results = await tmkt.player_search(player_name)
            if not search_results:
                return None, None
            
            player_id = search_results[0]['id']
            player_data = await tmkt.get_player(player_id)
            
            if player_data and 'data' in player_data:
                data = player_data['data']
                market_data = data.get('marketValueDetails', {})
                current = market_data.get('current', {})
                compact = current.get('compact', {})
                if compact and 'content' in compact:
                    try:
                        value = float(compact['content'])
                        url = f"https://www.transfermarkt.com{data.get('relativeUrl', '')}"
                        return value, url
                    except:
                        return None, None
            return None, None
        except Exception as e:
            print(f"   ⚠️ Error con {player_name}: {e}")
            return None, None

async def main():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    
    # Obtener jugadores jóvenes sin valor de mercado
    cur.execute("""
        SELECT id, nombre FROM players 
        WHERE edad <= 22 AND (market_value IS NULL OR market_value = 0)
        ORDER BY id
        LIMIT 50
    """)
    jugadores = cur.fetchall()
    
    print(f"📊 Actualizando {len(jugadores)} jugadores...\n")
    
    for jugador_id, nombre in jugadores:
        print(f"🔍 Procesando: {nombre}")
        valor, url = await get_market_value(nombre)
        
        if valor:
            cur.execute("""
                UPDATE players 
                SET market_value = %s, transfermarkt_url = %s, updated_at = %s
                WHERE id = %s
            """, (valor, url, datetime.now(), jugador_id))
            print(f"   ✅ Valor: {valor}M€")
        else:
            print(f"   ⚠️ No encontrado en Transfermarkt")
        
        conn.commit()
    
    cur.close()
    conn.close()
    print("\n🎉 Actualización completada.")

if __name__ == "__main__":
    asyncio.run(main())