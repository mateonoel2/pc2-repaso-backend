# Usa una imagen base con Python
FROM python:3.12-slim

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el archivo requirements.txt y realiza la instalación de dependencias
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de los archivos de la aplicación
COPY . .

# Establece las variables de entorno para la base de datos
# Estas se pueden configurar externamente en el entorno de producción
ENV DATABASE_URL="postgresql://usuario:contraseña@host_rds:5432/nombre_base_datos"
ENV SECRET_KEY="secret_kkey"
ENV ACCESS_TOKEN_EXPIRE_MINUTES=30

# Expon el puerto en el que corre FastAPI
EXPOSE 8000

# Ejecuta el script de entrada que ejecutará migraciones y datos iniciales
ENTRYPOINT ["./entrypoint.sh"]
