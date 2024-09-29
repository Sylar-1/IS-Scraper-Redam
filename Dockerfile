# Usar una imagen base de Python
FROM python:3.12.3

# Instalar Tesseract y dependencias
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    libleptonica-dev \
    && apt-get clean

# Instalar las dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación al contenedor
COPY . /app
WORKDIR /app

# Comando para ejecutar el script
CMD ["python", "app.py"]
