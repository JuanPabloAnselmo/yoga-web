# 🧘‍♀️ Sistema de Asistencia Yoga - Versión Web

## 📱 Cómo usar la aplicación web

### 1. Instalación y configuración

1. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Ejecutar la aplicación:**
   ```bash
   python app.py
   ```

3. **Encontrar tu IP local:**
   - **Windows:** Abre cmd y ejecuta `ipconfig`
   - **Mac/Linux:** Abre terminal y ejecuta `ifconfig`
   - Busca la dirección IP de tu red WiFi (ejemplo: 192.168.1.100)

### 2. Acceso desde celulares

1. **Conectar todos los dispositivos a la misma red WiFi**
2. **Abrir navegador en el celular**
3. **Ir a:** `http://TU_IP_LOCAL:5000`
   - Ejemplo: `http://192.168.1.100:5000`

### 3. Funcionalidades disponibles

#### 🏠 **Página Principal**
- Vista general del sistema
- Acceso rápido a todas las funciones
- Diseño responsive para móviles

#### 👥 **Registrar Alumnos**
- Agregar nuevos estudiantes
- Campos: Nombre, Apellido, Teléfono
- Validación automática

#### 📋 **Lista de Alumnos**
- Ver todos los alumnos registrados
- Información de contacto
- Estadísticas básicas

#### ✅ **Marcar Asistencia**
- **Toca en cualquier tarjeta** para cambiar estado
- Estados: Presente / Ausente / Sin marcar
- Contador en tiempo real
- Interfaz optimizada para móviles

#### 📊 **Ver Asistencias de Hoy**
- Resumen del día actual
- Estadísticas y porcentajes
- Lista detallada por estado

### 4. Características técnicas

- ✅ **Responsive:** Funciona perfecto en celulares y tablets
- ✅ **Tiempo real:** Los cambios se ven inmediatamente
- ✅ **Sin internet:** Solo necesita WiFi local
- ✅ **Base de datos local:** SQLite (se guarda automáticamente)
- ✅ **Múltiples usuarios:** Hasta 4 personas pueden usar simultáneamente

### 5. Solución de problemas

#### **No puedo acceder desde el celular:**
- Verifica que ambos dispositivos estén en la misma red WiFi
- Confirma que la IP sea correcta
- Prueba desactivar el firewall temporalmente

#### **La página no carga:**
- Verifica que `python app.py` esté ejecutándose
- Revisa que el puerto 5000 esté libre
- Intenta reiniciar la aplicación

#### **Los cambios no se guardan:**
- Verifica la conexión a la base de datos
- Revisa los permisos de escritura en la carpeta

### 6. Próximas mejoras

- 📈 Reportes mensuales
- 📤 Exportar a Excel
- 🔍 Búsqueda de alumnos
- ✏️ Editar información de alumnos
- 📱 Notificaciones push
- 🌐 Acceso desde internet (opcional)

---

## 🚀 ¡Listo para usar!

Tu sistema de asistencia para clases de yoga ya está funcionando. Las 4 personas pueden acceder desde sus celulares y todos verán los mismos datos en tiempo real.

**¿Necesitas ayuda?** Revisa la consola donde ejecutaste `python app.py` para ver mensajes de error o confirmación.
