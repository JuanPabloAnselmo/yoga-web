#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Asistencia para Clases de Yoga
Versión Básica
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime, date
import os

class SistemaAsistenciaYoga:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sistema de Asistencia - Clases de Yoga")
        self.root.geometry("800x600")
        
        # Crear base de datos
        self.crear_base_datos()
        
        # Crear interfaz
        self.crear_interfaz()
        
    def crear_base_datos(self):
        """Crear la base de datos SQLite"""
        self.conn = sqlite3.connect('asistencia_yoga.db')
        self.cursor = self.conn.cursor()
        
        # Crear tabla de alumnos
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS alumnos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                apellido TEXT NOT NULL,
                telefono TEXT,
                fecha_registro DATE DEFAULT CURRENT_DATE
            )
        ''')
        
        # Crear tabla de asistencias
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS asistencias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                alumno_id INTEGER,
                fecha DATE NOT NULL,
                presente BOOLEAN DEFAULT 0,
                FOREIGN KEY (alumno_id) REFERENCES alumnos (id)
            )
        ''')
        
        self.conn.commit()
    
    def crear_interfaz(self):
        """Crear la interfaz principal"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Título
        titulo = ttk.Label(main_frame, text="Sistema de Asistencia - Clases de Yoga", 
                          font=("Arial", 16, "bold"))
        titulo.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Botones principales
        btn_registrar = ttk.Button(main_frame, text="Registrar Alumno", 
                                  command=self.abrir_registro_alumno)
        btn_registrar.grid(row=1, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        btn_asistencia = ttk.Button(main_frame, text="Marcar Asistencia", 
                                   command=self.abrir_marcar_asistencia)
        btn_asistencia.grid(row=1, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        btn_ver_alumnos = ttk.Button(main_frame, text="Ver Alumnos", 
                                    command=self.ver_alumnos)
        btn_ver_alumnos.grid(row=2, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        btn_ver_asistencias = ttk.Button(main_frame, text="Ver Asistencias de Hoy", 
                                        command=self.ver_asistencias_hoy)
        btn_ver_asistencias.grid(row=2, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        # Configurar columnas
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
    
    def abrir_registro_alumno(self):
        """Abrir ventana para registrar nuevo alumno"""
        ventana = tk.Toplevel(self.root)
        ventana.title("Registrar Nuevo Alumno")
        ventana.geometry("400x300")
        ventana.grab_set()  # Hacer modal
        
        frame = ttk.Frame(ventana, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Campos del formulario
        ttk.Label(frame, text="Nombre:").grid(row=0, column=0, sticky=tk.W, pady=5)
        entry_nombre = ttk.Entry(frame, width=30)
        entry_nombre.grid(row=0, column=1, pady=5)
        
        ttk.Label(frame, text="Apellido:").grid(row=1, column=0, sticky=tk.W, pady=5)
        entry_apellido = ttk.Entry(frame, width=30)
        entry_apellido.grid(row=1, column=1, pady=5)
        
        ttk.Label(frame, text="Teléfono:").grid(row=2, column=0, sticky=tk.W, pady=5)
        entry_telefono = ttk.Entry(frame, width=30)
        entry_telefono.grid(row=2, column=1, pady=5)
        
        def guardar_alumno():
            nombre = entry_nombre.get().strip()
            apellido = entry_apellido.get().strip()
            telefono = entry_telefono.get().strip()
            
            if not nombre or not apellido:
                messagebox.showerror("Error", "Nombre y apellido son obligatorios")
                return
            
            try:
                self.cursor.execute('''
                    INSERT INTO alumnos (nombre, apellido, telefono)
                    VALUES (?, ?, ?)
                ''', (nombre, apellido, telefono))
                self.conn.commit()
                messagebox.showinfo("Éxito", "Alumno registrado correctamente")
                ventana.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Error al registrar alumno: {str(e)}")
        
        # Botones
        btn_guardar = ttk.Button(frame, text="Guardar", command=guardar_alumno)
        btn_guardar.grid(row=3, column=0, pady=20)
        
        btn_cancelar = ttk.Button(frame, text="Cancelar", command=ventana.destroy)
        btn_cancelar.grid(row=3, column=1, pady=20)
    
    def abrir_marcar_asistencia(self):
        """Abrir ventana para marcar asistencia"""
        ventana = tk.Toplevel(self.root)
        ventana.title("Marcar Asistencia")
        ventana.geometry("600x500")
        ventana.grab_set()
        
        frame = ttk.Frame(ventana, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Título con fecha
        fecha_hoy = date.today().strftime("%d/%m/%Y")
        ttk.Label(frame, text=f"Asistencia del día: {fecha_hoy}", 
                 font=("Arial", 12, "bold")).pack(pady=(0, 20))
        
        # Obtener lista de alumnos
        self.cursor.execute("SELECT id, nombre, apellido FROM alumnos ORDER BY apellido, nombre")
        alumnos = self.cursor.fetchall()
        
        if not alumnos:
            ttk.Label(frame, text="No hay alumnos registrados").pack()
            return
        
        # Frame para la lista de alumnos
        frame_lista = ttk.Frame(frame)
        frame_lista.pack(fill=tk.BOTH, expand=True)
        
        # Crear Treeview para mostrar alumnos
        columns = ("Nombre", "Apellido", "Asistencia")
        tree = ttk.Treeview(frame_lista, columns=columns, show="headings", height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        # Variables para checkboxes
        checkboxes = {}
        
        for alumno in alumnos:
            alumno_id, nombre, apellido = alumno
            
            # Verificar si ya tiene asistencia marcada hoy
            self.cursor.execute('''
                SELECT presente FROM asistencias 
                WHERE alumno_id = ? AND fecha = ?
            ''', (alumno_id, date.today()))
            resultado = self.cursor.fetchone()
            presente = resultado[0] if resultado else False
            
            # Insertar en treeview
            item_id = tree.insert("", "end", values=(nombre, apellido, "✓" if presente else "✗"))
            checkboxes[item_id] = (alumno_id, presente)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_lista, orient=tk.VERTICAL, command=tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.configure(yscrollcommand=scrollbar.set)
        
        def toggle_asistencia(event):
            item = tree.selection()[0]
            alumno_id, estado_actual = checkboxes[item]
            nuevo_estado = not estado_actual
            
            # Actualizar en base de datos
            if nuevo_estado:
                # Marcar como presente
                self.cursor.execute('''
                    INSERT OR REPLACE INTO asistencias (alumno_id, fecha, presente)
                    VALUES (?, ?, 1)
                ''', (alumno_id, date.today()))
            else:
                # Marcar como ausente
                self.cursor.execute('''
                    INSERT OR REPLACE INTO asistencias (alumno_id, fecha, presente)
                    VALUES (?, ?, 0)
                ''', (alumno_id, date.today()))
            
            self.conn.commit()
            
            # Actualizar visualización
            checkboxes[item] = (alumno_id, nuevo_estado)
            tree.item(item, values=(tree.item(item)['values'][0], 
                                   tree.item(item)['values'][1], 
                                   "✓" if nuevo_estado else "✗"))
        
        tree.bind("<Double-1>", toggle_asistencia)
        
        # Botón cerrar
        ttk.Button(frame, text="Cerrar", command=ventana.destroy).pack(pady=20)
    
    def ver_alumnos(self):
        """Mostrar lista de todos los alumnos"""
        ventana = tk.Toplevel(self.root)
        ventana.title("Lista de Alumnos")
        ventana.geometry("600x400")
        
        frame = ttk.Frame(ventana, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        ttk.Label(frame, text="Lista de Alumnos", 
                 font=("Arial", 12, "bold")).pack(pady=(0, 20))
        
        # Obtener alumnos
        self.cursor.execute("SELECT nombre, apellido, telefono, fecha_registro FROM alumnos ORDER BY apellido, nombre")
        alumnos = self.cursor.fetchall()
        
        if not alumnos:
            ttk.Label(frame, text="No hay alumnos registrados").pack()
            return
        
        # Crear Treeview
        columns = ("Nombre", "Apellido", "Teléfono", "Fecha Registro")
        tree = ttk.Treeview(frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        
        for alumno in alumnos:
            tree.insert("", "end", values=alumno)
        
        tree.pack(fill=tk.BOTH, expand=True)
        
        # Botón cerrar
        ttk.Button(frame, text="Cerrar", command=ventana.destroy).pack(pady=20)
    
    def ver_asistencias_hoy(self):
        """Mostrar asistencias del día actual"""
        ventana = tk.Toplevel(self.root)
        ventana.title("Asistencias de Hoy")
        ventana.geometry("500x400")
        
        frame = ttk.Frame(ventana, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        fecha_hoy = date.today().strftime("%d/%m/%Y")
        ttk.Label(frame, text=f"Asistencias del día: {fecha_hoy}", 
                 font=("Arial", 12, "bold")).pack(pady=(0, 20))
        
        # Obtener asistencias de hoy
        self.cursor.execute('''
            SELECT a.nombre, a.apellido, ast.presente
            FROM alumnos a
            LEFT JOIN asistencias ast ON a.id = ast.alumno_id AND ast.fecha = ?
            ORDER BY a.apellido, a.nombre
        ''', (date.today(),))
        
        asistencias = self.cursor.fetchall()
        
        if not asistencias:
            ttk.Label(frame, text="No hay alumnos registrados").pack()
            return
        
        # Crear Treeview
        columns = ("Nombre", "Apellido", "Estado")
        tree = ttk.Treeview(frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        
        for asistencia in asistencias:
            nombre, apellido, presente = asistencia
            estado = "Presente" if presente else "Ausente" if presente is not None else "Sin marcar"
            tree.insert("", "end", values=(nombre, apellido, estado))
        
        tree.pack(fill=tk.BOTH, expand=True)
        
        # Botón cerrar
        ttk.Button(frame, text="Cerrar", command=ventana.destroy).pack(pady=20)
    
    def run(self):
        """Ejecutar la aplicación"""
        self.root.mainloop()
        self.conn.close()

if __name__ == "__main__":
    app = SistemaAsistenciaYoga()
    app.run()
