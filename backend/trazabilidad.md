# Informe de Trazabilidad: Desarrollo y Arquitectura del Backend - TazaNorte

<p align="center">
  <img src="https://img.shields.io/badge/Project-TazaNorte_Backend-6F4E37?style=for-the-badge&logo=coffeescript&logoColor=white" alt="TazaNorte Backend" />
  <img src="https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Django-5.2.17-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django" />
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker" />
  <img src="https://img.shields.io/badge/MySQL-005C84?style=for-the-badge&logo=mysql&logoColor=white" alt="MySQL" />
  <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL" />
  <img src="https://img.shields.io/badge/MSSQL_Server-CC292B?style=for-the-badge&logo=microsoftsqlserver&logoColor=white" alt="MSSQL Server" />
  <img src="https://img.shields.io/badge/Oracle_Database-F80000?style=for-the-badge&logo=oracle&logoColor=white" alt="Oracle" />
</p>

---

## Información del Estudiante

| Campo          | Detalle                                                                                                     |
|----------------|-------------------------------------------------------------------------------------------------------------|
| **Nombre**     | Moises Bolivar                                                                                              |
| **Programa**   | Ingeniería de Sistemas                                                                                      |
| **Facultad**   | Facultad de Ingeniería, Universidad de La Guajira                                                          |
| **Docente**    | Ing. Jaider Quintero M.                                                                                     |
| **Referencia** | [https://tecnogua.com/academic/site/backend2026/django/](https://tecnogua.com/academic/site/backend2026/django/) |
| **Proyecto**   | Sistema de Gestión Integral de Cafetería TazaNorte - Módulo Backend Django                                   |
| **Fecha**      | Octubre de 2026                                                                                             |

---

## Tabla de Contenido

- [Información del Estudiante](#información-del-estudiante)
- [1. Introducción y Contexto del Backend](#1-introducción-y-contexto-del-backend)
- [2. Estructura del Repositorio y Módulo Backend](#2-estructura-del-repositorio-y-módulo-backend)
- [3. Unidad ISS-00 · Entorno y Proyecto Django — Capa 🛠 CONSTRUIR](#3-unidad-iss-00--entorno-y-proyecto-django--capa--construir)
  - [3.1 Objetivo](#31-objetivo)
  - [3.2 Requisitos Previos y Entorno](#32-requisitos-previos-y-entorno)
  - [3.3 Comandos de Construcción Ejecutados](#33-comandos-de-construcción-ejecutados)
  - [3.4 Estructura Generada por la CLI](#34-estructura-generada-por-la-cli)
  - [3.5 Configuración de .gitignore](#35-configuración-de-gitignore)
  - [3.6 Criterios de Aceptación (AC)](#36-criterios-de-aceptación-ac)
  - [3.7 Verificación del Sistema](#37-verificación-del-sistema)
  - [3.8 Matriz GATE de la Unidad ISS-00](#38-matriz-gate-de-la-unidad-iss-00)
  - [3.9 Evidencias Visuales (EVI)](#39-evidencias-visuales-evi)
- [4. Bitácora de Issues y Commits Realizados](#4-bitácora-de-issues-y-commits-realizados)

---

## 1. Introducción y Contexto del Backend

El presente documento constituye el **informe técnico y bitácora de trazabilidad** del desarrollo del backend del proyecto **TazaNorte**, articulado mediante el marco de trabajo **Django** en su versión **5.2.17** bajo un enfoque incremental guiado por unidades de trabajo (**Issues / ISS**).

El backend se conecta e interactúa con los 4 motores de bases de datos aprovisionados en contenedores Docker (`MySQL 8.0`, `PostgreSQL 17`, `Microsoft SQL Server 2022` y `Oracle Database XE 21c`), garantizando integridad referencial, persistencia distribuida y auditoría transaccional.

---

## 2. Estructura del Repositorio y Módulo Backend

El proyecto backend se aloja en el directorio `backend/` dentro de la raíz del laboratorio (`~/ia-lab/backend/`), asegurando una separación modular respecto a los servicios de infraestructura y datos:

```text
backend/
├── .gitignore                    # Reglas de exclusión para Git (.venv, pycache, env, sqlite)
├── .venv/                        # Entorno virtual aislado con Python 3.12 y Django 5.2.17
├── config/                       # Paquete principal de configuración del proyecto Django
│   ├── __init__.py
│   ├── asgi.py                   # Entrada para servidores asíncronos ASGI
│   ├── settings.py               # Configuración centralizada de Django
│   ├── urls.py                   # URLconf raíz del proyecto
│   └── wsgi.py                   # Entrada para servidores síncronos WSGI
├── manage.py                     # CLI de administración del proyecto Django
├── requirements.txt              # Congelamiento exacto de dependencias instaladas
├── capturas/                     # Almacén de evidencias visuales del laboratorio
│   ├── .gitkeep
│   ├── ISS-00_EVI-01_django_instalado.png
│   └── ISS-00_EVI-02_arbol_config.png
├── caps/                         # Enlace directo para material fotográfico
└── trazabilidad.md               # Informe de trazabilidad técnica (este documento)
```

---

## 3. Unidad ISS-00 · Entorno y Proyecto Django — Capa 🛠 CONSTRUIR

- **Guía de estudio:** [ISS-00 · 🧠 Aprender](https://tecnogua.com/academic/site/backend2026/django/aprendizaje/ISS-00-aprendizaje/)
- **Manual de construcción:** [ISS-00 · 🛠 Construir](https://tecnogua.com/academic/site/backend2026/django/manual/01-ISS-00-entorno-y-proyecto-django/)

### 3.1 Objetivo

Crear el entorno virtual aislado (`.venv`) y el proyecto Django `config` mediante herramientas CLI oficiales, garantizando un punto de partida limpio y sin modelos de negocio iniciales.

### 3.2 Requisitos Previos y Entorno

- **Intérprete Python:** Python 3.12 (`Python 3.12.3` sobre Ubuntu 24.04 LTS / WSL2).
- **Directorio de trabajo:** `~/ia-lab/backend`
- **Versión de Framework requerida:** `Django==5.2.17`

### 3.3 Comandos de Construcción Ejecutados

Se ejecutó la secuencia oficial en el directorio del proyecto con el Python del sistema para inicializar el entorno y posteriormente con el intérprete del entorno activo:

```bash
# 1. Creación del entorno virtual aislado
python3 -m venv .venv

# 2. Activación del entorno
source .venv/bin/activate

# 3. Instalación de la versión específica de Django
python -m pip install "Django==5.2.17"

# 4. Creación del proyecto Django con nombre config en la raíz del módulo
django-admin startproject config .

# 5. Congelamiento de las dependencias
python -m pip freeze > requirements.txt

# 6. Comprobación de la versión instalada
python -m django --version
```

**Resultado de la versión:**
```text
5.2.17
```

**Dependencias congeladas en `requirements.txt`:**
```text
asgiref==3.12.1
Django==5.2.17
sqlparse==0.6.0
```

### 3.4 Estructura Generada por la CLI

El comando `django-admin startproject config .` generó la arquitectura base sin anidamientos innecesarios:
- `manage.py`: Script de gestión que establece `DJANGO_SETTINGS_MODULE="config.settings"`.
- `config/settings.py`: Archivo de configuración generado por la plantilla base.
- `config/urls.py`: URLconf raíz con la ruta de administración `path('admin/', admin.site.urls)`.
- `config/wsgi.py` y `config/asgi.py`: Puntos de entrada para servidores de aplicaciones web.

### 3.5 Configuración de .gitignore

Se creó el archivo `.gitignore` para evitar que el entorno virtual, caché de Python y bases de datos locales se incluyan en el control de versiones:

```bash
cat > .gitignore <<'EOF'
.venv/
__pycache__/
*.py[cod]
.env
db.sqlite3
*.log
.idea/
.vscode/
staticfiles/
media/
.pytest_cache/
htmlcov/
.coverage
EOF
```

### 3.6 Criterios de Aceptación (AC)

| Código | Criterio de Aceptación | Estado |
|--------|------------------------|--------|
| **AC-00-01** | `python -m django --version` imprime exactamente `5.2.17`. | **CUMPLIDO** |
| **AC-00-02** | Existen en la raíz del backend los archivos `manage.py` y `config/urls.py`. | **CUMPLIDO** |
| **AC-00-03** | No existen modelos de negocio definidos en esta unidad inicial. | **CUMPLIDO** |

### 3.7 Verificación del Sistema

Se ejecutaron las instrucciones de verificación estipuladas en la guía técnica del ISS-00:

```bash
python -m django --version
python manage.py check
```

**Salida obtenida:**
```text
5.2.17
System check identified no issues (0 silenced).
```

**Evidencia de Verificación:**

![Verificación de Django y Check del Proyecto](capturas/ISS-00_verificacion_check.png)

### 3.8 Matriz GATE de la Unidad ISS-00

| AC | Verificación | Evidencia | Resultado |
|----|--------------|-----------|-----------|
| **AC-00-01** | Versión de Django en entorno activo | `EVI-00-01` | **PASS** |
| **AC-00-02** | Archivos del proyecto generados (`manage.py`, `config/urls.py`) | `EVI-00-02` | **PASS** |
| **AC-00-03** | Ausencia de modelos de negocio (inspección de árbol) | Inspección del árbol | **PASS** |

> **Condición GATE:** Todas las condiciones de aceptación se encuentran en **PASS**. La unidad **ISS-00** queda formalmente cerrada y el entorno habilitado para avanzar a la unidad **ISS-01**.

---

### 3.9 Evidencias Visuales (EVI)

#### 📸 Evidencia 1 (`EVI-00-01`): Instalación de Django 5.2.17 en `.venv`

- **Archivo de captura:** `capturas/ISS-00_EVI-01_django_instalado.png`
- **Descripción:** Captura de pantalla de la terminal en WSL2 mostrando el prompt con el entorno virtual activo `(.venv)`, la ejecución de `python -m django --version` con salida `5.2.17` y el contenido de `requirements.txt`.
- **Criterio que valida:** AC-00-01.

![EVI-00-01: Django 5.2.17 instalado en .venv](capturas/ISS-00_EVI-01_django_instalado.png)

---

#### 📸 Evidencia 2 (`EVI-00-02`): Árbol del proyecto `config/` generado por la CLI y chequeo del sistema

- **Archivo de captura:** `capturas/ISS-00_EVI-02_arbol_config.png`
- **Descripción:** Captura de pantalla de la terminal en WSL2 mostrando la ejecución exitosa de `python manage.py check` (`System check identified no issues`) y el listado de archivos en `config/` y `manage.py`.
- **Criterio que valida:** AC-00-02 y AC-00-03.

![EVI-00-02: Árbol config generado y manage.py check](capturas/ISS-00_EVI-02_arbol_config.png)

---

## 4. Bitácora de Issues y Commits Realizados

| Issue | Descripción del Cambio | Hash Commit | Estado |
|-------|------------------------|-------------|--------|
| **ISS-00** | Entorno y proyecto Django: `.venv`, Django 5.2.17, `config/`, `.gitignore` y `requirements.txt` | *(pendiente de commit)* | **COMPLETADO** |
