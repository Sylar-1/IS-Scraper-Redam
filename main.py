from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import pytesseract
from PIL import Image
import time  # Importar el módulo time

# Ruta de instalación de Tesseract en tu contenedor
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

# Configurar Selenium Grid y conectarse al hub
def get_driver(browser_name):
    if browser_name == "chrome":
        options = ChromeOptions()
    elif browser_name == "firefox":
        options = FirefoxOptions()
    else:
        raise ValueError("Navegador no soportado: usa 'chrome' o 'firefox'")

    driver = webdriver.Remote(
        #command_executor='http://localhost:4444/wd/hub',
        command_executor='http://selenium-hub:4444/wd/hub',
        options=options  # Aquí reemplazamos desired_capabilities por options
    )
    return driver


# Función de scraping
def scrape_page(url, browser_name="chrome"):
    driver = get_driver(browser_name)
    try:
        driver.get(url)

        # Extraer el título de la página
        title = driver.title
        print(f"Título de la página: {title}")

        # Esperar 10 segundos después de obtener el título
        time.sleep(3)

        # Hacer clic en el elemento con el XPath proporcionado
        element = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[1]/div/div/div/div[2]/ul/li[2]/a')
        element.click()  # Hacer clic en el elemento

        # Localizar el dropdown list por su XPath
        dropdown = driver.find_element(By.XPATH,'/html/body/div[2]/div/div/div[1]/div/div/div/div[2]/div/div[2]/div/form/div[1]/div/select')

        # Crear un objeto Select para manejar el dropdown
        select = Select(dropdown)

        # Seleccionar el valor del dropdown (value="object:32")
        select.select_by_value('object:32')

        # Esperar unos segundos para ver la selección
        time.sleep(2)

        # Localizar el campo de texto por id y escribir el número "2728282"
        numero_documento = driver.find_element(By.ID, 'numerodocumento')
        numero_documento.send_keys('70838125')  # Escribir en el campo de texto

        # Bucle para intentar resolver el captcha
        success = False
        while not success:
            try:
                # Capturar el captcha
                element = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/table/tbody/tr/td[1]/div/img')
                element.screenshot('element_screenshot.png')  # Guardar el screenshot como un archivo

                # Procesar la imagen con Tesseract
                img = Image.open('element_screenshot.png')  # Abrir la imagen capturada
                text = pytesseract.image_to_string(img)  # Extraer el texto de la imagen

                # Ingresar el texto del captcha
                captcha = driver.find_element(By.ID, 'captcha')
                captcha.clear()  # Limpiar cualquier texto previo
                captcha.send_keys(text)  # Escribir el texto reconocido en el captcha

                # Simular Enter para enviar el formulario
                #captcha.send_keys(Keys.ENTER)
                print(f"Texto reconocido: {text}")

                # Esperar unos segundos para que la página se actualice después del envío del captcha
                time.sleep(5)

                # Verificar si el formulario se ha enviado correctamente y existe el elemento esperado
                # Este es el elemento que aparecerá después de resolver correctamente el captcha
                resultado = driver.find_element(By.XPATH,
                                                    '/html/body/div[2]/div/div[2]/div/div/section/table/tbody/tr/td')

                # Si encontramos el elemento, significa que el captcha fue correcto
                success = True
                print("Captcha resuelto correctamente. Elemento encontrado.")

            except Exception as e:
                # Si no se encuentra el elemento esperado, o hay un error (como un captcha incorrecto),
                # se repetirá el proceso para intentar resolverlo de nuevo.
                print("Intento fallido. Reintentando...")
                time.sleep(2)  # Esperar un par de segundos antes de volver a intentar

        time.sleep(10)


    finally:
        driver.quit()


if __name__ == "__main__":
    # URL de la página que quieres scrapear
    url = "https://casillas.pj.gob.pe/redam/#/"

    # Ejecutar el scraping en Chrome
    scrape_page(url, browser_name="chrome")
