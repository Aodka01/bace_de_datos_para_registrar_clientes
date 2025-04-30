import sqlite3
import tkinter as tk
from tkinter import messagebox

def conectar_bd():
    return sqlite3.connect('agencia_servicios.db')

def crear_tablas():
    with conectar_bd() as conexion:
        cursor = conexion.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Clientes (
                ID_Cliente INTEGER PRIMARY KEY,
                Nombre TEXT NOT NULL,
                Direccion TEXT NOT NULL,
                Telefono TEXT NOT NULL,
                Email TEXT NOT NULL,
                Plan_ID INTEGER
            )
        ''')
        conexion.commit()

def insertar_cliente():
    id_cliente = entry_id.get()
    nombre = entry_nombre.get()
    direccion = entry_direccion.get()
    telefono = entry_telefono.get()
    email = entry_email.get()
    plan_id = entry_plan.get()
    
    if not (id_cliente and nombre and direccion and telefono and email and plan_id):
        messagebox.showwarning("Advertencia", "Todos los campos son obligatorios")
        return
    
    try:
        with conectar_bd() as conexion:
            cursor = conexion.cursor()
            cursor.execute('''
                INSERT INTO Clientes (ID_Cliente, Nombre, Direccion, Telefono, Email, Plan_ID)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (id_cliente, nombre, direccion, telefono, email, plan_id))
            conexion.commit()
            messagebox.showinfo("Éxito", "Cliente agregado correctamente")
            listar_clientes()
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "ID de cliente ya existente")

def listar_clientes():
    with conectar_bd() as conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM Clientes")
        clientes = cursor.fetchall()
    lista.delete(0, tk.END)
    for cliente in clientes:
        lista.insert(tk.END, cliente)

def eliminar_cliente():
    seleccionado = lista.curselection()
    if not seleccionado:
        messagebox.showwarning("Advertencia", "Seleccione un cliente para eliminar")
        return
    id_cliente = lista.get(seleccionado)[0]
    with conectar_bd() as conexion:
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM Clientes WHERE ID_Cliente = ?", (id_cliente,))
        conexion.commit()
        messagebox.showinfo("Éxito", "Cliente eliminado correctamente")
        listar_clientes()

def actualizar_cliente():
    seleccionado = lista.curselection()
    if not seleccionado:
        messagebox.showwarning("Advertencia", "Seleccione un cliente para actualizar")
        return
    id_cliente = lista.get(seleccionado)[0]
    nuevo_nombre = entry_nombre.get()
    nueva_direccion = entry_direccion.get()
    nuevo_telefono = entry_telefono.get()
    nuevo_email = entry_email.get()
    nuevo_plan = entry_plan.get()
    
    with conectar_bd() as conexion:
        cursor = conexion.cursor()
        cursor.execute('''
            UPDATE Clientes
            SET Nombre = ?, Direccion = ?, Telefono = ?, Email = ?, Plan_ID = ?
            WHERE ID_Cliente = ?
        ''', (nuevo_nombre, nueva_direccion, nuevo_telefono, nuevo_email, nuevo_plan, id_cliente))
        conexion.commit()
        messagebox.showinfo("Éxito", "Cliente actualizado correctamente")
        listar_clientes()

# Interfaz gráfica
crear_tablas()
root = tk.Tk()
root.title("Gestión de Clientes")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

tk.Label(frame, text="ID Cliente:").grid(row=0, column=0)
tk.Label(frame, text="Nombre:").grid(row=1, column=0)
tk.Label(frame, text="Dirección:").grid(row=2, column=0)
tk.Label(frame, text="Teléfono:").grid(row=3, column=0)
tk.Label(frame, text="Email:").grid(row=4, column=0)
tk.Label(frame, text="Plan ID:").grid(row=5, column=0)

entry_id = tk.Entry(frame)
entry_nombre = tk.Entry(frame)
entry_direccion = tk.Entry(frame)
entry_telefono = tk.Entry(frame)
entry_email = tk.Entry(frame)
entry_plan = tk.Entry(frame)

entry_id.grid(row=0, column=1)
entry_nombre.grid(row=1, column=1)
entry_direccion.grid(row=2, column=1)
entry_telefono.grid(row=3, column=1)
entry_email.grid(row=4, column=1)
entry_plan.grid(row=5, column=1)

tk.Button(frame, text="Agregar Cliente", command=insertar_cliente).grid(row=6, column=0, columnspan=2, pady=5)
tk.Button(frame, text="Actualizar Cliente", command=actualizar_cliente).grid(row=7, column=0, columnspan=2, pady=5)
tk.Button(frame, text="Eliminar Cliente", command=eliminar_cliente).grid(row=8, column=0, columnspan=2, pady=5)

lista = tk.Listbox(root, width=70, height=10)
lista.pack(padx=10, pady=10)

listar_clientes()
root.mainloop()
