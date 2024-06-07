# Usa una imagen base oficial de Python
FROM python:3.12-slim

# Establece el directorio de trabajo
WORKDIR /

# Copia el archivo requirements.txt y lo instala
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copia todo el contenido de la carpeta actual a /app
COPY . .

# Expone el puerto 5000 para la aplicación
EXPOSE 5000

# Define el comando por defecto para ejecutar la aplicación
CMD ["python", "app.py"]

