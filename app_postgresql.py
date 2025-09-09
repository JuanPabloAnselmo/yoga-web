#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Asistencia para Clases de Yoga - Versión Web con PostgreSQL
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
import psycopg2
import psycopg2.extras
from datetime import datetime, date
import os
from urllib.parse import urlparse

app = Flask(__name__)

def get_db_connection():
    """Conectar a la base de datos PostgreSQL"""
    try:
        # Obtener URL de la base de datos desde Railway
        database_url = os.environ.get('DATABASE_URL')
        
        if not database_url:
            # Para desarrollo local, usar SQLite como fallback
            import sqlite3
            conn = sqlite3.connect('asistencia_yoga.db')
            conn.row_factory = sqlite3.Row
            return conn
        
        # Parsear la URL de PostgreSQL
        result = urlparse(database_url)
        
        conn = psycopg2.connect(
            database=result.path[1:],  # Remover el '/' inicial
            user=result.username,
            password=result.password,
            host=result.hostname,
            port=result.port
        )
        
        # Configurar para que las consultas devuelvan diccionarios
        conn.autocommit = True
        return conn
        
    except Exception as e:
        print(f"Error conectando a la base de datos: {str(e)}")
        # Fallback a SQLite para desarrollo local
        import sqlite3
        conn = sqlite3.connect('asistencia_yoga.db')
        conn.row_factory = sqlite3.Row
        return conn

def init_db():
    """Inicializar la base de datos"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Crear tabla de alumnos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alumnos (
                id SERIAL PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                apellido VARCHAR(100) NOT NULL,
                telefono VARCHAR(20),
                fecha_registro DATE DEFAULT CURRENT_DATE
            )
        ''')
        
        # Crear tabla de asistencias
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS asistencias (
                id SERIAL PRIMARY KEY,
                alumno_id INTEGER,
                fecha DATE NOT NULL,
                presente BOOLEAN DEFAULT FALSE,
                FOREIGN KEY (alumno_id) REFERENCES alumnos (id)
            )
        ''')
        
        conn.commit()
        print("Base de datos inicializada correctamente")
        
    except Exception as e:
        print(f"Error inicializando base de datos: {str(e)}")
        # Si es PostgreSQL, usar sintaxis correcta
        if 'psycopg2' in str(type(conn)):
            try:
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS alumnos (
                        id SERIAL PRIMARY KEY,
                        nombre VARCHAR(100) NOT NULL,
                        apellido VARCHAR(100) NOT NULL,
                        telefono VARCHAR(20),
                        fecha_registro DATE DEFAULT CURRENT_DATE
                    )
                ''')
                
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS asistencias (
                        id SERIAL PRIMARY KEY,
                        alumno_id INTEGER,
                        fecha DATE NOT NULL,
                        presente BOOLEAN DEFAULT FALSE,
                        FOREIGN KEY (alumno_id) REFERENCES alumnos (id)
                    )
                ''')
                
                conn.commit()
                print("Base de datos PostgreSQL inicializada correctamente")
            except Exception as e2:
                print(f"Error con PostgreSQL: {str(e2)}")
    finally:
        cursor.close()
        conn.close()

def execute_query(query, params=None, fetch=False):
    """Ejecutar consulta de forma segura"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        if fetch:
            if 'psycopg2' in str(type(conn)):
                # Para PostgreSQL, devolver diccionarios
                columns = [desc[0] for desc in cursor.description]
                results = cursor.fetchall()
                return [dict(zip(columns, row)) for row in results]
            else:
                # Para SQLite, ya devuelve diccionarios
                return cursor.fetchall()
        else:
            conn.commit()
            return True
            
    except Exception as e:
        print(f"Error ejecutando consulta: {str(e)}")
        return None
    finally:
        cursor.close()
        conn.close()

@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')

@app.route('/alumnos')
def ver_alumnos():
    """Ver lista de alumnos"""
    try:
        # Asegurar que la base de datos esté inicializada
        init_db()
        
        alumnos = execute_query('''
            SELECT * FROM alumnos ORDER BY apellido, nombre
        ''', fetch=True)
        
        if not alumnos:
            return render_template('alumnos.html', alumnos=[], registrados_hoy=0)
        
        # Contar alumnos registrados hoy
        hoy = date.today().strftime('%Y-%m-%d')
        registrados_hoy = len([alumno for alumno in alumnos if alumno['fecha_registro'] == hoy])
        
        return render_template('alumnos.html', alumnos=alumnos, registrados_hoy=registrados_hoy)
    except Exception as e:
        print(f"Error en ver_alumnos: {str(e)}")
        return f"Error: {str(e)}", 500

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
            # Asegurar que la base de datos esté inicializada
            init_db()
            
            result = execute_query('''
                INSERT INTO alumnos (nombre, apellido, telefono)
                VALUES (%s, %s, %s)
            ''', (nombre, apellido, telefono))
            
            if result:
                return jsonify({'success': True, 'message': 'Alumno registrado correctamente'})
            else:
                return jsonify({'success': False, 'message': 'Error al registrar alumno'})
                
        except Exception as e:
            return jsonify({'success': False, 'message': f'Error al registrar: {str(e)}'})
    
    return render_template('registrar_alumno.html')

@app.route('/asistencia')
def marcar_asistencia():
    """Página para marcar asistencia"""
    try:
        init_db()
        
        alumnos = execute_query('''
            SELECT a.id, a.nombre, a.apellido, 
                   COALESCE(ast.presente, NULL) as presente
            FROM alumnos a
            LEFT JOIN asistencias ast ON a.id = ast.alumno_id AND ast.fecha = %s
            ORDER BY a.apellido, a.nombre
        ''', (date.today(),), fetch=True)
        
        return render_template('asistencia.html', alumnos=alumnos, fecha_hoy=date.today().strftime("%d/%m/%Y"))
    except Exception as e:
        print(f"Error en marcar_asistencia: {str(e)}")
        return f"Error: {str(e)}", 500

@app.route('/toggle_asistencia', methods=['POST'])
def toggle_asistencia():
    """Cambiar estado de asistencia de un alumno"""
    data = request.get_json()
    alumno_id = data['alumno_id']
    presente = data['presente']
    
    try:
        init_db()
        
        result = execute_query('''
            INSERT INTO asistencias (alumno_id, fecha, presente)
            VALUES (%s, %s, %s)
            ON CONFLICT (alumno_id, fecha) 
            DO UPDATE SET presente = EXCLUDED.presente
        ''', (alumno_id, date.today(), presente))
        
        if result:
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'message': 'Error al actualizar asistencia'})
            
    except Exception as e:
        print(f"Error en toggle_asistencia: {str(e)}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/asistencias_hoy')
def ver_asistencias_hoy():
    """Ver asistencias del día actual"""
    try:
        init_db()
        
        asistencias = execute_query('''
            SELECT a.nombre, a.apellido, 
                   CASE 
                       WHEN ast.presente = TRUE THEN 'Presente'
                       WHEN ast.presente = FALSE THEN 'Ausente'
                       ELSE 'Sin marcar'
                   END as estado
            FROM alumnos a
            LEFT JOIN asistencias ast ON a.id = ast.alumno_id AND ast.fecha = %s
            ORDER BY a.apellido, a.nombre
        ''', (date.today(),), fetch=True)
        
        return render_template('asistencias_hoy.html', asistencias=asistencias, fecha_hoy=date.today().strftime("%d/%m/%Y"))
    except Exception as e:
        print(f"Error en ver_asistencias_hoy: {str(e)}")
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    init_db()
    
    # Obtener puerto del entorno (para Railway) o usar 5000 por defecto
    port = int(os.environ.get('PORT', 5000))
    
    print("=" * 50)
    print("Sistema de Asistencia Yoga - Versión Web con PostgreSQL")
    print("=" * 50)
    print(f"Servidor ejecutándose en puerto: {port}")
    print("=" * 50)
    
    # Ejecutar en modo debug para desarrollo local, producción para Railway
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
