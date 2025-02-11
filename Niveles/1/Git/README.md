# Clase de Git y GitHub: Guía Completa


## 1. Introducción a Git y GitHub

**Git** es un sistema de control de versiones distribuido que permite gestionar el historial de cambios en proyectos de software. **GitHub** es una plataforma basada en la nube que facilita la colaboración usando Git.

### Componentes Clave

- **Repositorio:** Contenedor que almacena el código y su historial de versiones.
- **Commit:** Registro de cambios realizados en el código.
- **Branch:** Rama de desarrollo paralela al código principal.
- **Pull Request:** Solicitud para fusionar cambios de una rama a otra, permitiendo revisiones colaborativas.

---

## 2. Configuración de Llaves SSH

### 🌐 **Generar Llave SSH en Linux**

```bash
# Generar una nueva llave SSH
ssh-keygen -t ed25519 -C "tu_email@example.com"

# Presiona Enter para aceptar la ubicación por defecto
# Opcional: ingresa una contraseña para mayor seguridad

# Iniciar el agente SSH y agregar la llave
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# Copiar la llave pública al portapapeles
cat ~/.ssh/id_ed25519.pub
```

### 💻 **Generar Llave SSH en Windows (Git Bash)**

```bash
# Generar la llave SSH
ssh-keygen -t ed25519 -C "tu_email@example.com"

# Acepta la ubicación por defecto y configura una contraseña si deseas

# Iniciar el agente SSH
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# Copiar la llave pública al portapapeles (Git Bash)
cat ~/.ssh/id_ed25519.pub | clip
```

### 📢 **Agregar la Llave SSH en GitHub**

1. Inicia sesión en GitHub.
2. Ve a **Settings > SSH and GPG keys**.
3. Haz clic en **New SSH key**, asigna un título y pega la llave pública.
4. Guarda los cambios.

### 🚀 **Configurar Git Globalmente**

Antes de clonar repositorios, configura tu nombre y correo electrónico globalmente:

```bash
# Configurar el nombre de usuario
 git config --global user.name "Tu Nombre"

# Configurar el correo electrónico
 git config --global user.email "tu_email@example.com"
```

---

## 3. Creación de un Repositorio en GitHub

### Paso 1: Crear un Repositorio en GitHub

1. Ve a [GitHub](https://github.com).
2. Haz clic en **New repository**.
3. Asigna un nombre y configura las opciones (público o privado).
4. No inicialices con README si deseas clonar un repositorio vacío.

### Paso 2: Clonar el Repositorio

```bash
# Clonar usando SSH (sin necesidad de especificar usuario)
 git clone git@github.com:nombre-repositorio.git

# Acceder al directorio del repositorio
cd nombre-repositorio
```

---

## 4. Trabajo con Git: Commits y Pull Requests

### 📁 **Agregar Archivos y Realizar un Commit**

```bash
# Ver el estado del repositorio
 git status

# Agregar archivos al área de preparación (staging)
 git add archivo.txt

# O agregar todos los archivos
 git add .

# Realizar un commit con un mensaje descriptivo
 git commit -m "Agrega la funcionalidad X"
```

### 📡 **Enviar Cambios a GitHub (Push)**

```bash
# Enviar cambios a la rama principal (main o master)
 git push origin main
```

### 🚀 **Crear una Rama Nueva y Hacer Cambios**

```bash
# Crear y cambiar a una nueva rama
 git checkout -b nueva-rama

# Realizar cambios, agregar y hacer commit
 git add .
 git commit -m "Mejoras en la interfaz de usuario"

# Enviar la rama al repositorio remoto
 git push origin nueva-rama
```

### 📄 **Crear un Pull Request**

1. Ve al repositorio en GitHub.
2. Haz clic en **Compare & pull request**.
3. Agrega un título y una descripción de los cambios.
4. Haz clic en **Create pull request**.

### 📰 **Actualizar tu Rama Local (Pull)**

```bash
# Obtener los últimos cambios del repositorio remoto
 git pull origin main
```

---

## 5. Ejemplo Completo

```bash
# Configurar Git globalmente
 git config --global user.name "Tu Nombre"
 git config --global user.email "tu_email@example.com"

# Clonar un repositorio existente
 git clone git@github.com:proyecto.git
 cd proyecto

# Crear una nueva rama
 git checkout -b feature-login

# Agregar archivos de Python
 echo "print('Hola, Git!')" > app.py
 git add app.py
 git commit -m "Agrega funcionalidad de login"

# Enviar la rama
 git push origin feature-login

# Crear un Pull Request en GitHub
```

---

## 🌟 Buenas Prácticas

- **Commits descriptivos:** Usa mensajes breves y claros.
- **Ramas específicas:** Crea ramas por funcionalidad.
- **Revisiones de código:** Utiliza pull requests para facilitar la revisión de código.
- **Sincronización frecuente:** Haz `pull` regularmente para evitar conflictos.

---

## Recursos Adicionales

- [Documentación oficial de Git](https://git-scm.com/doc)
- [Guía de GitHub](https://docs.github.com/)