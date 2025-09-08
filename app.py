#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Asistencia para Clases de Yoga - Versión Web
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3
from datetime import datetime, date
import os

app = Flask(__name__)

def get_db_connection():
    """Conectar a la base de datos"""
    conn = sqlite3.connect('asistencia_yoga.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Inicializar la base de datos"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Crear tabla de alumnos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alumnos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            telefono TEXT,
            fecha_registro DATE DEFAULT CURRENT_DATE
        )
    ''')
    
    # Crear tabla de asistencias
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS asistencias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            alumno_id INTEGER,
            fecha DATE NOT NULL,
            presente BOOLEAN DEFAULT 0,
            FOREIGN KEY (alumno_id) REFERENCES alumnos (id)
        )
    ''')
    
    conn.commit()
    conn.close()

@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')

@app.route('/alumnos')
def ver_alumnos():
    """Ver lista de alumnos"""
    conn = get_db_connection()
    alumnos = conn.execute('''
        SELECT * FROM alumnos ORDER BY apellido, nombre
    ''').fetchall()
    
    # Contar alumnos registrados hoy
    hoy = date.today().strftime('%Y-%m-%d')
    registrados_hoy = len([alumno for alumno in alumnos if alumno['fecha_registro'] == hoy])
    
    conn.close()
    return render_template('alumnos.html', alumnos=alumnos, registrados_hoy=registrados_hoy)

@app.route('/registrar_alumno', methods=['GET', 'POST'])
def registrar_alumno():
    """Registrar nuevo alumno"""
    if request.method == 'POST':
        nombre = request.form['nombre'].strip()
        apellido = request.form['apellido'].strip()
        telefono = request.form['telefono'].strip()
        
        if not nombre or not apellido:
            return jsonify({'success': False, 'message': 'Nombre y apellido son obligatorios'})
        
        try:
            conn = get_db_connection()
            conn.execute('''
                INSERT INTO alumnos (nombre, apellido, telefono)
                VALUES (?, ?, ?)
            ''', (nombre, apellido, telefono))
            conn.commit()
            conn.close()
            return jsonify({'success': True, 'message': 'Alumno registrado correctamente'})
        except Exception as e:
            return jsonify({'success': False, 'message': f'Error al registrar: {str(e)}'})
    
    return render_template('registrar_alumno.html')

@app.route('/asistencia')
def marcar_asistencia():
    """Página para marcar asistencia"""
    conn = get_db_connection()
    
    # Obtener alumnos con su estado de asistencia de hoy
    alumnos = conn.execute('''
        SELECT a.id, a.nombre, a.apellido, 
               COALESCE(ast.presente, NULL) as presente
        FROM alumnos a
        LEFT JOIN asistencias ast ON a.id = ast.alumno_id AND ast.fecha = ?
        ORDER BY a.apellido, a.nombre
    ''', (date.today(),)).fetchall()
    
    conn.close()
    return render_template('asistencia.html', alumnos=alumnos, fecha_hoy=date.today().strftime("%d/%m/%Y"))

@app.route('/toggle_asistencia', methods=['POST'])
def toggle_asistencia():
    """Cambiar estado de asistencia de un alumno"""
    data = request.get_json()
    alumno_id = data['alumno_id']
    presente = data['presente']
    
    try:
        conn = get_db_connection()
        conn.execute('''
            INSERT OR REPLACE INTO asistencias (alumno_id, fecha, presente)
            VALUES (?, ?, ?)
        ''', (alumno_id, date.today(), presente))
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/asistencias_hoy')
def ver_asistencias_hoy():
    """Ver asistencias del día actual"""
    conn = get_db_connection()
    asistencias = conn.execute('''
        SELECT a.nombre, a.apellido, 
               CASE 
                   WHEN ast.presente = 1 THEN 'Presente'
                   WHEN ast.presente = 0 THEN 'Ausente'
                   ELSE 'Sin marcar'
               END as estado
        FROM alumnos a
        LEFT JOIN asistencias ast ON a.id = ast.alumno_id AND ast.fecha = ?
        ORDER BY a.apellido, a.nombre
    ''', (date.today(),)).fetchall()
    
    conn.close()
    return render_template('asistencias_hoy.html', asistencias=asistencias, fecha_hoy=date.today().strftime("%d/%m/%Y"))

if __name__ == '__main__':
    init_db()
    
    # Obtener puerto del entorno (para Railway) o usar 5000 por defecto
    port = int(os.environ.get('PORT', 5000))
    
    print("=" * 50)
    print("Sistema de Asistencia Yoga - Versión Web")
    print("=" * 50)
    print(f"Servidor ejecutándose en puerto: {port}")
    print("=" * 50)
    
    # Ejecutar en modo debug para desarrollo local, producción para Railway
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
