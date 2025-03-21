# pip install fastapi uvicorn sqlalchemy pymysql
# Ejecutar con: python -m uvicorn main:app --reload

from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import os
from dotenv import load_dotenv


print("🔥 Iniciando APU...")

# Cargar variables de entorno
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# Configurar conexión a MySQL
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:3306/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- MODELOS DE BASE DE DATOS ---

class Producto(Base):
    __tablename__ = 'productos'
    id_producto = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(80), nullable=False)
    descripcion = Column(String(99), nullable=False)
    precio = Column(Float, nullable=False, default=0)
    id_categoria = Column(Integer, ForeignKey("categorias.id_categoria"), nullable=False)
    tiempo_disponible = Column(Float, nullable=False, default=0)
    id_proveedor = Column(Integer, ForeignKey("proveedores.id_proveedor"), nullable=False)

    categoria = relationship("Categoria", back_populates="productos")
    proveedor = relationship("Proveedor", back_populates="productos")

class Categoria(Base):
    __tablename__ = 'categorias'
    id_categoria = Column(Integer, primary_key=True)
    nombre = Column(String(80), nullable=False)
    productos = relationship("Producto", back_populates="categoria")

class Proveedor(Base):
    __tablename__ = 'proveedores'
    id_proveedor = Column(Integer, primary_key=True)
    nombre = Column(String(50), nullable=False)
    contacto = Column(String(80))
    direccion = Column(String(80), nullable=False)
    productos = relationship("Producto", back_populates="proveedor")

class Cliente(Base):
    __tablename__ = 'clientes'
    id_cliente = Column(Integer, primary_key=True)
    nombre_completo = Column(String(80), nullable=False)
    email = Column(String(80), nullable=False)
    telefono = Column(Integer, nullable=False)
    direccion = Column(String(80))

class Compra(Base):
    __tablename__ = 'compras'
    id_pedido = Column(Integer, primary_key=True)
    id_cliente = Column(Integer, ForeignKey("clientes.id_cliente"), nullable=False)
    fecha_pedido = Column(TIMESTAMP, nullable=False)
    importe_total = Column(Float, nullable=False, default=1)

    cliente = relationship("Cliente")

class DetalleCompra(Base):
    __tablename__ = 'detalles_compras'
    id_producto = Column(Integer, ForeignKey("productos.id_producto"), primary_key=True)
    id_pedido = Column(Integer, ForeignKey("compras.id_pedido"), primary_key=True)
    cantidad = Column(Float, nullable=False, default=0)
    unidad = Column(String(10), nullable=False, default="1")
    precio = Column(Float, nullable=False)
    metodo_Pago = Column(String(10), nullable=False)

class Stock(Base):
    __tablename__ = 'stock'
    id_producto = Column(Integer, ForeignKey("productos.id_producto"), primary_key=True)
    fecha_stock = Column(TIMESTAMP, nullable=False)
    cantidad = Column(Float, nullable=False, default=0)
    unidad = Column(String(15))

# --- CREAR LA APP ---

app = FastAPI()

# --- ENDPOINTS ---

# 📌 PRODUCTOS
@app.get("/productos/")
def leer_productos():
    db = SessionLocal()
    productos = db.query(Producto).all()
    db.close()
    return productos

@app.get("/productos/{id_producto}")
def leer_producto(id_producto: int):
    db = SessionLocal()
    producto = db.query(Producto).filter(Producto.id_producto == id_producto).first()
    db.close()
    if producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

# 📌 CATEGORÍAS
@app.get("/categorias/")
def leer_categorias():
    db = SessionLocal()
    categorias = db.query(Categoria).all()
    db.close()
    return categorias

@app.get("/categorias/{id_categoria}")
def leer_categoria(id_categoria: int):
    db = SessionLocal()
    categoria = db.query(Categoria).filter(Categoria.id_categoria == id_categoria).first()
    db.close()
    if categoria is None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return categoria

# 📌 PROVEEDORES
@app.get("/proveedores/")
def leer_proveedores():
    db = SessionLocal()
    proveedores = db.query(Proveedor).all()
    db.close()
    return proveedores

@app.get("/proveedores/{id_proveedor}")
def leer_proveedor(id_proveedor: int):
    db = SessionLocal()
    proveedor = db.query(Proveedor).filter(Proveedor.id_proveedor == id_proveedor).first()
    db.close()
    if proveedor is None:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    return proveedor

# 📌 CLIENTES
@app.get("/clientes/")
def leer_clientes():
    db = SessionLocal()
    clientes = db.query(Cliente).all()
    db.close()
    return clientes

@app.get("/clientes/{id_cliente}")
def leer_cliente(id_cliente: int):
    db = SessionLocal()
    cliente = db.query(Cliente).filter(Cliente.id_cliente == id_cliente).first()
    db.close()
    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente

# 📌 COMPRAS
@app.get("/compras/")
def leer_compras():
    db = SessionLocal()
    compras = db.query(Compra).all()
    db.close()
    return compras

@app.get("/compras/{id_pedido}")
def leer_compra(id_pedido: int):
    db = SessionLocal()
    compra = db.query(Compra).filter(Compra.id_pedido == id_pedido).first()
    db.close()
    if compra is None:
        raise HTTPException(status_code=404, detail="Compra no encontrada")
    return compra

# 📌 STOCK
@app.get("/stock/")
def leer_stock():
    db = SessionLocal()
    stock = db.query(Stock).all()
    db.close()
    return stock

@app.get("/stock/{id_producto}")
def leer_stock_producto(id_producto: int):
    db = SessionLocal()
    stock = db.query(Stock).filter(Stock.id_producto == id_producto).first()
    db.close()
    if stock is None:
        raise HTTPException(status_code=404, detail="Stock no encontrado")
    return stock

# 📌 DETALLES DE COMPRA
@app.get("/detalles_compras/")
def leer_detalles_compras():
    db = SessionLocal()
    detalles = db.query(DetalleCompra).all()
    db.close()
    return detalles

# --- INICIO DEL SERVIDOR ---
@app.on_event("startup")
def listar_rutas():
    print("📋 RUTAS DISPONIBLES:")
    for route in app.routes:
        print(f"➡️ {route.path} -> {route.endpoint.__name__}")

