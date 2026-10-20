gimport os
import json
import time
import requests
from dotenv import load_dotenv
from flask import Flask, render_template, jsonify

# Carrega variáveis do arquivo .env
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'art-odonto-secret-key-2026'

# Chaves do Google Places API
GOOGLE_API_KEY = os.getenv('GOOGLE_PLACES_API_KEY', '').strip()
GOOGLE_PLACE_ID = os.getenv('GOOGLE_PLACE_ID', '').strip()

# Cache em memória para não consumir cota do Google desnecessariamente (1 hora)
REVIEWS_CACHE = {
    "timestamp": 0,
    "data": None
}
CACHE_TIMEOUT = 3600

def get_status_label(rating):
    if rating >= 4.8:
        return "EXCELENTE"
    elif rating >= 4.0:
        return "MUITO BOM"
    elif rating >= 3.0:
        return "BOM"
    return "REGULAR"

def fetch_google_reviews():
    """Busca diretamente na API oficial do Google Places os dados reais do consultório."""
    now = time.time()
    if REVIEWS_CACHE["data"] and (now - REVIEWS_CACHE["timestamp"] < CACHE_TIMEOUT):
        return REVIEWS_CACHE["data"]

    # Se as chaves do Google estiverem configuradas
    if GOOGLE_API_KEY and GOOGLE_PLACE_ID:
        try:
            url = "https://maps.googleapis.com/maps/api/place/details/json"
            params = {
                "place_id": GOOGLE_PLACE_ID,
                "fields": "name,rating,user_ratings_total,reviews",
                "key": GOOGLE_API_KEY,
                "language": "pt-BR"
            }
            resp = requests.get(url, params=params, timeout=7)
            data_json = resp.json()

            if resp.status_code == 200 and data_json.get("status") == "OK":
                result = data_json.get("result", {})
                raw_reviews = result.get("reviews", [])
                
                rating = float(result.get("rating", 5.0))
                total_reviews = int(result.get("user_ratings_total", 0))

                reviews_list = []
                for idx, r in enumerate(raw_reviews):
                    reviews_list.append({
                        "id": idx + 1,
                        "author_name": r.get("author_name", "Paciente"),
                        "relative_time_description": r.get("relative_time_description", ""),
                        "rating": int(r.get("rating", 5)),
                        "verified": True,
                        "text": r.get("text", "")
                    })

                data = {
                    "configured": True,
                    "overall": {
                        "status": get_status_label(rating),
                        "rating": rating,
                        "total_reviews": total_reviews
                    },
                    "reviews": reviews_list,
                    "error": None
                }
                REVIEWS_CACHE["timestamp"] = now
                REVIEWS_CACHE["data"] = data
                return data
            else:
                err_msg = data_json.get("error_message", data_json.get("status", "Erro desconhecido na API"))
                print(f"[Google Places API Erro]: {err_msg}")
                return {
                    "configured": False,
                    "overall": {"status": "CONFIGURAÇÃO NECESSÁRIA", "rating": 5.0, "total_reviews": 0},
                    "reviews": [],
                    "error": f"Erro do Google: {err_msg}"
                }
        except Exception as e:
            print(f"[Google Places API Falha]: {e}")
            return {
                "configured": False,
                "overall": {"status": "ERRO DE CONEXÃO", "rating": 5.0, "total_reviews": 0},
                "reviews": [],
                "error": str(e)
            }

    # Caso ainda não tenha inserido a Chave e o Place ID
    return {
        "configured": False,
        "overall": {
            "status": "AGUARDANDO GOOGLE PLACE ID",
            "rating": 5.0,
            "total_reviews": 0
        },
        "reviews": [],
        "error": "Informe sua GOOGLE_PLACES_API_KEY e GOOGLE_PLACE_ID no arquivo .env para carregar as avaliações reais."
    }

@app.route('/')
def index():
    reviews_data = fetch_google_reviews()
    return render_template('index.html', reviews_data=reviews_data)

@app.route('/sw.js')
def service_worker():
    return app.send_static_file('sw.js')

@app.route('/manifest.json')
def manifest():
    return app.send_static_file('manifest.json')

@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('images/favicon.ico')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
