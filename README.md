# 🛒 API Tienda - FastAPI

Bienvenido a la API de gestión de tienda, desarrollada con **FastAPI**, **SQLAlchemy** y **MySQL**.  
Este proyecto permite gestionar productos, clientes, compras y stock de una tienda.  

📌 **Incluye**:  
✅ Gestión de productos, clientes y proveedores  
✅ Registro de compras y actualización de stock  
✅ Base de datos MySQL replicable (archivos en `mysql/`)  
✅ Configuración segura con variables de entorno (`.env`)

---

## 🚀 Instalación y Configuración

### 1️⃣ Clona el repositorio
```bash
git clone https://github.com/tu-usuario/api-tienda.git
cd api-tienda
```

### 2️⃣ Instala las dependencias  
Si usas `poetry`:
```bash
poetry install
```

### 3️⃣ Configura las variables de entorno  
Crea un archivo `.env` en la raíz del proyecto:
```ini
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=tucontraseña
DB_NAME=dev_testeos
```

### 4️⃣ Ejecuta el servidor  
```bash
uvicorn main:app --reload
```
La API estará disponible en:  
📌 **http://127.0.0.1:8000**

Puedes ver la documentación interactiva en **Swagger UI**:  
📌 **http://127.0.0.1:8000/docs**

---

## 📂 Replicando la Base de Datos  
En la carpeta **`mysql/`** encontrarás los archivos `.sql` para crear y poblar la base de datos.  

1. **Importa el archivo SQL en MySQL**  
```bash
mysql -u root -p dev_testeos < mysql/tiendas_api.sql
```
2. **Verifica que las tablas existen**  
```sql
USE dev_testeos;
SHOW TABLES;
```

---

## 🛠️ Endpoints Principales

### 📌 **Productos**
| Método | Endpoint           | Descripción |
|--------|-------------------|-------------|
| GET    | `/productos/`      | Listar todos los productos |
| GET    | `/productos/{id}`  | Obtener un producto por ID |

### 📌 **Clientes**
| Método | Endpoint           | Descripción |
|--------|-------------------|-------------|
| GET    | `/clientes/`      | Listar todos los clientes |
| GET    | `/clientes/{id}`  | Obtener un cliente por ID |

### 📌 **Compras**
| Método | Endpoint           | Descripción |
|--------|-------------------|-------------|
| GET    | `/compras/`       | Listar todas las compras |
| GET    | `/compras/{id}`   | Obtener una compra por ID |

### 📌 **Stock**
| Método | Endpoint           | Descripción |
|--------|-------------------|-------------|
| GET    | `/stock/`         | Listar stock disponible |
| GET    | `/stock/{id}`     | Ver stock de un producto |

---

## 🛠️ Tecnologías Utilizadas
- **FastAPI** → Framework web rápido para APIs  
- **SQLAlchemy** → ORM para manejar la base de datos  
- **PyMySQL** → Conector de MySQL en Python  
- **Uvicorn** → Servidor ASGI para FastAPI  
- **dotenv** → Gestión de variables de entorno  

---


---

### 📕 **FASE 2**


Creacion de las aplicaciones en `Python` de `app_caja.py` y `app_clientes.py`. Así podrás realizar tus simulaciones de compras con `app_caja.py` y tus registros de clientes con `app_clientes.py`

## 📜 Licencia  
Este proyecto es de código abierto y puedes modificarlo según tus necesidades.  

🚀 **¡Disfruta desarrollando con FastAPI!** 🔥
