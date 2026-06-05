from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

API_KEY = os.getenv("API_FOOTBALL_KEY")
API_HOST = "v3.football.api-sports.io"

@app.route('/api/predict', methods=['GET'])
def predict():
    """Predicción de partido"""
    local = request.args.get('local')
    visitante = request.args.get('visitante')
    
    if not local or not visitante:
        return jsonify({"error": "Faltan parámetros"}), 400
    
    # Llamar a tu motor de predicción
    prediccion = predecir_partido(local, visitante)
    
    return jsonify(prediccion)

@app.route('/api/team/<team_name>', methods=['GET'])
def team_stats(team_name):
    """Estadísticas de un equipo"""
    stats = obtener_estadisticas_reales(team_name)
    if stats:
        return jsonify(stats)
    return jsonify({"error": "Equipo no encontrado"}), 404

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "online", "version": "1.0"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)