import tkinter as tk
from tkinter import messagebox
import random
import mysql.connector
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Conexión a la base de datos
conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database="dev_testeos"
)
cursor = conn.cursor()

# Crear la interfaz
def insertar_cliente():
    nombre = entry_nombre.get()
    email = entry_email.get()
    telefono = entry_telefono.get()
    direccion = entry_direccion.get()

    if not nombre or not email or not telefono or not direccion:
        messagebox.showwarning("Campos incompletos", "Por favor, completa todos los campos")
        return

    id_cliente = str(random.randint(10000000, 99999999))

    try:
        cursor.execute(
            "INSERT INTO clientes (id_cliente, nombre_completo, email, telefono, direccion) VALUES (%s, %s, %s, %s, %s)",
            (id_cliente, nombre, email, telefono, direccion)
        )
        conn.commit()
        messagebox.showinfo("Éxito", f"Cliente insertado con ID: {id_cliente}")
        entry_nombre.delete(0, tk.END)
        entry_email.delete(0, tk.END)
        entry_telefono.delete(0, tk.END)
        entry_direccion.delete(0, tk.END)
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al insertar cliente: {err}")

root = tk.Tk()
root.title("Registro de Clientes")
root.geometry("400x300")
root.configure(bg="#f0f0f0")

# Etiquetas y campos de entrada
tk.Label(root, text="Nombre Completo:", bg="#f0f0f0").pack(pady=(10, 0))
entry_nombre = tk.Entry(root, width=40)
entry_nombre.pack()

tk.Label(root, text="Email:", bg="#f0f0f0").pack(pady=(10, 0))
entry_email = tk.Entry(root, width=40)
entry_email.pack()

tk.Label(root, text="Teléfono:", bg="#f0f0f0").pack(pady=(10, 0))
entry_telefono = tk.Entry(root, width=40)
entry_telefono.pack()

tk.Label(root, text="Dirección:", bg="#f0f0f0").pack(pady=(10, 0))
entry_direccion = tk.Entry(root, width=40)
entry_direccion.pack()

# Botón
btn_insertar = tk.Button(root, text="Insertar Cliente", command=insertar_cliente, bg="#4CAF50", fg="white", padx=10, pady=5)
btn_insertar.pack(pady=20)

root.mainloop()

# Cierre de conexión al cerrar la app
cursor.close()
conn.close()