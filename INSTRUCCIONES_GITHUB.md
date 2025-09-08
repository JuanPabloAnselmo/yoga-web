# 📋 Instrucciones para Subir a GitHub y Railway

## 🎯 Tu aplicación está funcionando perfectamente localmente
- ✅ Servidor ejecutándose en puerto 5000
- ✅ Todas las funcionalidades probadas
- ✅ Acceso desde celular funcionando (192.168.0.193:5000)

## 📤 Paso 1: Subir a GitHub

### 1.1 Crear repositorio en GitHub
1. Ve a [github.com](https://github.com)
2. Haz clic en "New repository" (botón verde)
3. **Nombre del repositorio:** `sistema-asistencia-yoga`
4. **Descripción:** `Sistema web para gestionar asistencias de clases de yoga`
5. **Visibilidad:** Público ✅
6. **NO marques** "Add a README file" (ya tienes uno)
7. Haz clic "Create repository"

### 1.2 Subir archivos desde tu computadora
```bash
# En la carpeta de tu proyecto, ejecuta estos comandos:

git init
git add .
git commit -m "Sistema de asistencia yoga - versión inicial"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/sistema-asistencia-yoga.git
git push -u origin main
```

**Reemplaza `TU_USUARIO` con tu nombre de usuario de GitHub**

## 🌐 Paso 2: Desplegar en Railway

### 2.1 Conectar con Railway
1. Ve a [railway.app](https://railway.app)
2. Haz clic "Login with GitHub"
3. Autoriza Railway a acceder a tu GitHub

### 2.2 Desplegar la aplicación
1. En Railway, haz clic "New Project"
2. Selecciona "Deploy from GitHub repo"
3. Busca y selecciona `sistema-asistencia-yoga`
4. Railway automáticamente:
   - Detecta que es Python
   - Instala las dependencias
   - Ejecuta tu aplicación
   - Te da una URL pública

### 2.3 ¡Listo!
- Tu aplicación estará disponible en una URL como: `https://tu-app.railway.app`
- **Cualquier persona** puede acceder desde cualquier lugar
- **Funciona 24/7** sin que tengas que hacer nada

## 🔗 URLs de acceso

### Local (solo en tu red):
- **Computadora:** http://localhost:5000
- **Celular:** http://192.168.0.193:5000

### Global (después de Railway):
- **Cualquier dispositivo:** https://tu-app.railway.app

## 📱 Prueba final

1. **Accede a la URL de Railway** desde tu celular
2. **Registra algunos alumnos** de prueba
3. **Marca asistencia** tocando en las tarjetas
4. **Verifica que todo funcione** igual que localmente

## 🆘 Si algo no funciona

1. **Revisa los logs** en Railway (hay una pestaña "Logs")
2. **Verifica que todos los archivos** se subieron a GitHub
3. **Confirma que las dependencias** se instalaron correctamente

---

**¡Tu sistema de asistencia para yoga estará online en minutos!** 🧘‍♀️✨
