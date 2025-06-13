#!/bin/bash

echo "🚀 Configurando SparkyRoll API para Práctica Calificada"
echo "=================================================="

# Verificar si Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker no está instalado. Por favor instala Docker primero."
    echo "   Visita: https://www.docker.com/get-started"
    exit 1
fi

# Verificar si Docker Compose está instalado
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose no está instalado. Por favor instala Docker Compose primero."
    echo "   Visita: https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✅ Docker y Docker Compose están instalados"

# Crear archivo .env si no existe
if [ ! -f .env ]; then
    echo "📝 Creando archivo .env..."
    cp env.example .env
    echo "✅ Archivo .env creado. Puedes modificar las variables según sea necesario."
else
    echo "✅ Archivo .env ya existe"
fi

# Construir y ejecutar los contenedores
echo "🐳 Construyendo y ejecutando los contenedores..."
docker-compose up --build -d

echo ""
echo "🎉 ¡Configuración completada!"
echo ""
echo "📋 Información importante:"
echo "   • API disponible en: http://localhost:8000"
echo "   • Documentación Swagger: http://localhost:8000/docs"
echo "   • Base de datos PostgreSQL en puerto 5432"
echo ""
echo "🔧 Comandos útiles:"
echo "   • Ver logs: docker-compose logs -f"
echo "   • Detener servicios: docker-compose down"
echo "   • Reiniciar servicios: docker-compose restart"
echo ""
echo "📚 Para más información, consulta el README.md" 