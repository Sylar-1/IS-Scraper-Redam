from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
import time

app = Flask(__name__)

@app.route('/run-scraper', methods=['POST'])
def run_scraper():
    data = request.get_json()

    # Configurar Selenium Grid
    options = ChromeOptions()
    driver = webdriver.Remote(
        command_executor='http://localhost:4444/wd/hub',
        options=options
    )

    try:
        # Ejecutar el scraper en la URL recibida en el JSON
        driver.get(data['url'])
        title = driver.title
        time.sleep(10)  # Esperar 10 segundos como se pidió
        return jsonify({'status': 'success', 'title': title}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        driver.quit()

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
