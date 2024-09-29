from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
import time
from main import scrape_page  # Importamos la función scrape_page desde main.py

app = Flask(__name__)

@app.route('/run-scraper', methods=['POST'])
def run_scraper():
    data = request.get_json()
    dni = data.get('dni')
    url = "https://casillas.pj.gob.pe/redam/#/"  # La URL de la página que quieres scrapear

    if not dni:
        return jsonify({'status': 'error', 'message': 'DNI no proporcionado'}), 400

    try:
        # Llamamos a la función scrape_page y pasamos la URL y el DNI
        scrape_page(url, dni)
        return jsonify({'status': 'success', 'message': 'Scraping ejecutado correctamente.'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
