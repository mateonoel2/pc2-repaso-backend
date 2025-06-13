# SparkyRoll API - Backend para Práctica Calificada

## Descripción

SparkyRoll API es un backend desarrollado en FastAPI que proporciona servicios para una aplicación de anime. Este proyecto incluye funcionalidades de autenticación, gestión de favoritos e historial de visualización.

## Características

- 🔐 **Autenticación**: Sistema de registro y login de usuarios
- 📺 **Gestión de Anime**: Endpoints para manejar información de anime
- ⭐ **Favoritos**: Sistema para marcar anime como favoritos
- 📚 **Historial**: Seguimiento del historial de visualización
- 🐳 **Docker**: Aplicación completamente containerizada
- 🗄️ **PostgreSQL**: Base de datos relacional

## Tecnologías Utilizadas

- **FastAPI**: Framework web moderno y rápido para Python
- **SQLAlchemy**: ORM para Python
- **PostgreSQL**: Base de datos relacional
- **Docker**: Containerización
- **Alembic**: Migraciones de base de datos
- **JWT**: Autenticación basada en tokens
- **Uvicorn**: Servidor ASGI

## 🚀 Inicio Rápido

¿Tienes prisa? Ejecuta estos comandos para tener la API funcionando en minutos:

```bash
git clone https://github.com/TU_USUARIO/NOMBRE_DEL_REPOSITORIO.git
cd NOMBRE_DEL_REPOSITORIO
./setup.sh
```

¡Listo! La API estará disponible en http://localhost:8000

## Requisitos Previos

Antes de ejecutar este proyecto, asegúrate de tener instalado:

- [Python 3.12+](https://www.python.org/downloads/)
- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Git](https://git-scm.com/downloads)

## Instalación y Configuración

### Opción 1: Ejecución con Docker (Recomendado)

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/TU_USUARIO/sparkyroll-api.git
   cd sparkyroll-api
   ```

2. **Configurar variables de entorno (Opcional)**
   
   El proyecto ya incluye configuración por defecto, pero puedes personalizar creando un archivo `.env`:
   ```bash
   cp env.example .env
   # Edita el archivo .env si necesitas cambiar alguna configuración
   ```

3. **Ejecutar la aplicación**
   ```bash
   docker-compose up --build
   ```

### Opción 2: Ejecución Local

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/TU_USUARIO/sparkyroll-api.git
   cd sparkyroll-api
   ```

2. **Crear entorno virtual**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar PostgreSQL**
   
   Instala PostgreSQL y crea una base de datos:
   ```sql
   CREATE DATABASE sparkyroll_db;
   ```

5. **Configurar variables de entorno**
   
   Exporta las variables de entorno o crea un archivo `.env`:
   ```bash
   export DATABASE_URL="postgresql://usuario:contraseña@localhost:5432/sparkyroll_db"
   export SECRET_KEY="tu_clave_secreta_super_segura_aqui"
   export ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

6. **Ejecutar migraciones**
   ```bash
   alembic upgrade head
   ```

7. **Iniciar la aplicación**
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

## Uso de la API

Una vez que la aplicación esté ejecutándose, puedes acceder a:

- **API**: http://localhost:8000
- **Documentación Swagger**: http://localhost:8000/docs
- **Documentación ReDoc**: http://localhost:8000/redoc

### Endpoints Principales

#### Autenticación
- `POST /register` - Registrar nuevo usuario
- `POST /login` - Iniciar sesión
- `GET /me` - Obtener información del usuario actual

#### Anime
- `GET /anime` - Listar anime
- `GET /anime/{id}` - Obtener anime por ID
- `POST /anime` - Crear nuevo anime (requiere autenticación)

#### Favoritos
- `GET /favorites` - Obtener favoritos del usuario
- `POST /favorites` - Agregar anime a favoritos
- `DELETE /favorites/{anime_id}` - Eliminar de favoritos

#### Historial
- `GET /history` - Obtener historial del usuario
- `POST /history` - Agregar entrada al historial

## Estructura del Proyecto

```
sparkyroll-api/
├── app/
│   ├── api/                 # Endpoints de la API
│   │   ├── auth.py         # Autenticación
│   │   ├── anime.py        # Gestión de anime
│   │   ├── favorites.py    # Sistema de favoritos
│   │   └── history.py      # Historial de visualización
│   ├── models/             # Modelos de base de datos
│   ├── schemas/            # Esquemas Pydantic
│   ├── services/           # Lógica de negocio
│   ├── config.py          # Configuración
│   └── main.py            # Aplicación principal
├── Dockerfile             # Configuración Docker
├── docker-compose.yml     # Orquestación de servicios
├── requirements.txt       # Dependencias Python
├── entrypoint.sh         # Script de inicio
├── init_data.sql         # Datos iniciales
└── README.md             # Este archivo
```

## Desarrollo

### Agregar Nuevas Migraciones

```bash
alembic revision --autogenerate -m "Descripción del cambio"
alembic upgrade head
```

### Ejecutar Tests

```bash
pytest
```

### Formateo de Código

```bash
black app/
isort app/
```

## Variables de Entorno

| Variable | Descripción | Valor por Defecto |
|----------|-------------|-------------------|
| `DATABASE_URL` | URL de conexión a PostgreSQL | - |
| `SECRET_KEY` | Clave secreta para JWT | - |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Tiempo de expiración del token | 30 |

## Solución de Problemas

### Error de Conexión a Base de Datos

1. Verifica que PostgreSQL esté ejecutándose
2. Confirma que las credenciales en `DATABASE_URL` sean correctas
3. Asegúrate de que la base de datos exista

### Error de Permisos en entrypoint.sh

```bash
chmod +x entrypoint.sh
```

### Problemas con Docker

```bash
docker-compose down
docker-compose up --build --force-recreate
```

## Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## Contacto

Para preguntas sobre esta práctica calificada, contacta a tu profesor.

---

**Nota para Estudiantes**: Este backend está diseñado para ser utilizado en prácticas de desarrollo frontend. Puedes conectar cualquier aplicación cliente (React, Vue, Angular, etc.) a estos endpoints para crear una aplicación completa de gestión de anime.
