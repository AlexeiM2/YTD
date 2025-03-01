# Dockerfile
FROM python:3.9-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar dependencias
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente
COPY . .

# Exponer el puerto
EXPOSE 8080

# Comando para iniciar el servidor Flask
CMD ["flask", "--app", "app:create_app", "run", "--host=0.0.0.0", "--port=8080"]