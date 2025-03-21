import tkinter as tk
from tkinter import ttk, messagebox
import random
import datetime
import pymysql
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

# Configuración de la conexión a MySQL desde .env
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "dev_testeos")

# Conectar a la base de datos
def conectar_db():
    return pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)

# Obtener lista de productos
def obtener_productos():
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT id_producto, nombre, precio FROM productos")
    productos = cursor.fetchall()
    conexion.close()
    return productos

# Obtener lista de clientes
def obtener_clientes():
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT id_cliente, nombre_completo FROM clientes")
    clientes = cursor.fetchall()
    conexion.close()
    return clientes

# Generar ID de pedido con formato YYYYXXXX
def generar_id_pedido():
    año_actual = datetime.datetime.now().year
    numero_random = random.randint(1000, 9999)
    return f"{año_actual}{numero_random}"

# Función para realizar la compra
def realizar_compra():
    try:
        id_producto = int(combo_productos.get().split(" - ")[0])
        id_cliente = int(combo_clientes.get().split(" - ")[0])
        cantidad = int(entry_cantidad.get())
        metodo_pago = combo_pago.get()

        if cantidad <= 0:
            messagebox.showerror("Error", "La cantidad debe ser un número positivo.")
            return

        if metodo_pago not in ["Efectivo", "Tarjeta", "Bizum"]:
            messagebox.showerror("Error", "Método de pago inválido.")
            return

        # Obtener el precio del producto
        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute("SELECT precio FROM productos WHERE id_producto = %s", (id_producto,))
        resultado = cursor.fetchone()
        conexion.close()

        if not resultado:
            messagebox.showerror("Error", "Producto no encontrado.")
            return

        precio_unitario = resultado[0]
        precio_total = precio_unitario * cantidad
        id_pedido = generar_id_pedido()

        # Insertar en detalles_compras
        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO detalles_compras (id_producto, id_pedido, id_cliente, cantidad, unidad, precio, metodo_Pago)
            VALUES (%s, %s, %s, %s, 'unidades', %s, %s)
        """, (id_producto, id_pedido, id_cliente, cantidad, precio_total, metodo_pago))

        conexion.commit()
        conexion.close()

        messagebox.showinfo("Éxito", f"Compra realizada con éxito.\nID Pedido: {id_pedido}\nTotal: {precio_total}€")

    except ValueError:
        messagebox.showerror("Error", "Ingrese valores válidos.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

# Crear ventana principal
root = tk.Tk()
root.title("Registro de Compras")
root.geometry("400x300")

# Obtener datos
productos = obtener_productos()
clientes = obtener_clientes()

# Etiqueta y combo de productos
tk.Label(root, text="Producto:").pack()
combo_productos = ttk.Combobox(root, values=[f"{p[0]} - {p[1]} ({p[2]}€)" for p in productos], state="readonly")
combo_productos.pack()

# Etiqueta y combo de clientes
tk.Label(root, text="Cliente:").pack()
combo_clientes = ttk.Combobox(root, values=[f"{c[0]} - {c[1]}" for c in clientes], state="readonly")
combo_clientes.pack()

# Etiqueta y campo de cantidad
tk.Label(root, text="Cantidad:").pack()
entry_cantidad = tk.Entry(root)
entry_cantidad.pack()

# Etiqueta y combo de método de pago
tk.Label(root, text="Método de Pago:").pack()
combo_pago = ttk.Combobox(root, values=["Efectivo", "Tarjeta", "Bizum"], state="readonly")
combo_pago.pack()

# Botón de compra
tk.Button(root, text="COMPRA", command=realizar_compra, bg="green", fg="white").pack(pady=10)

# Ejecutar la aplicación
root.mainloop()
