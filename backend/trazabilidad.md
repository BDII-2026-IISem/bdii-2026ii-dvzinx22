# Informe de Trazabilidad: Desarrollo y Arquitectura del Backend - TazaNorte

<p align="center">
  <img src="https://img.shields.io/badge/Project-TazaNorte_Backend-6F4E37?style=for-the-badge&logo=coffeescript&logoColor=white" alt="TazaNorte Backend" />
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
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
| **Proyecto**   | Sistema de Gestión Integral de Cafetería TazaNorte - Módulo Backend                                         |
| **Fecha**      | Octubre de 2026                                                                                             |

---

## Tabla de Contenido

- [Información del Estudiante](#información-del-estudiante)
- [1. Introducción y Objetivos](#1-introducción-y-objetivos)
- [2. Arquitectura de Software y Patrón de Diseño](#2-arquitectura-de-software-y-patrón-de-diseño)
  - [2.1 Enfoque Arquitectónico por Capas](#21-enfoque-arquitectónico-por-capas)
  - [2.2 Interoperabilidad Multimotor de Base de Datos](#22-interoperabilidad-multimotor-de-base-de-datos)
- [3. Estructura de Directorios del Backend](#3-estructura-de-directorios-del-backend)
- [4. Requisitos del Entorno y Dependencias](#4-requisitos-del-entorno-y-dependencias)
  - [4.1 Creación del Entorno Virtual](#41-creación-del-entorno-virtual)
  - [4.2 Configuración de Variables de Entorno (.env)](#42-configuración-de-variables-de-entorno-env)
- [5. Modelado del Dominio y Entidades del Negocio](#5-modelado-del-dominio-y-entidades-del-negocio)
- [6. Registro de Trazabilidad y Evidencias Visuales](#6-registro-de-trazabilidad-y-evidencias-visuales)
  - [6.1 Evidencia 1: Creación de la Estructura de Directorios del Backend](#61-evidencia-1-creación-de-la-estructura-de-directorios-del-backend)
  - [6.2 Evidencia 2: Inicialización del Entorno Virtual e Instalación de Dependencias](#62-evidencia-2-inicialización-del-entorno-virtual-e-instalación-de-dependencias)
  - [6.3 Evidencia 3: Configuración de Variables de Entorno y Pool de Conexiones](#63-evidencia-3-configuración-de-variables-de-entorno-y-pool-de-conexiones)
  - [6.4 Evidencia 4: Verificación de Conectividad con Motores de Bases de Datos](#64-evidencia-4-verificación-de-conectividad-con-motores-de-bases-de-datos)
  - [6.5 Evidencia 5: Implementación y Levantamiento del Servidor Backend](#65-evidencia-5-implementación-y-levantamiento-del-servidor-backend)
  - [6.6 Evidencia 6: Documentación Interactiva de APIs (Swagger / OpenAPI)](#66-evidencia-6-documentación-interactiva-de-apis-swagger--openapi)
  - [6.7 Evidencia 7: Pruebas Funcionales de Endpoints y Operaciones CRUD](#67-evidencia-7-pruebas-funcionales-de-endpoints-y-operaciones-crud)
  - [6.8 Evidencia 8: Verificación de Persistencia y Auditoría](#68-evidencia-8-verificación-de-persistencia-y-auditoría)
- [7. Conclusiones y Próximos Pasos](#7-conclusiones-y-próximos-pasos)

---

## 1. Introducción y Objetivos

El presente documento registra la **trazabilidad completa del desarrollo, configuración y despliegue del módulo Backend** para la cafetería **TazaNorte**. Este componente actúa como el núcleo lógico del sistema, encargado de procesar las reglas de negocio, coordinar la persistencia de datos relacionales y proveer interfaces de comunicación mediante APIs REST para los clientes consumidores.

### Objetivos Principales:
1. **Desacoplamiento y Modularidad:** Implementar una arquitectura limpia y estructurada por capas que separe la capa de presentación/enrutamiento, la capa de servicios y la capa de acceso a datos.
2. **Conectividad Multimotor:** Mantener compatibilidad e integración con los 4 motores relacionales configurados en el laboratorio (**MySQL 8.0**, **PostgreSQL 17**, **SQL Server 2022** y **Oracle XE 21c**).
3. **Control y Auditoría:** Garantizar que todas las operaciones críticas (pedidos, pagos, movimientos de stock) preserven la integridad referencial y las reglas de inmutabilidad establecidas en los triggers de base de datos.
4. **Documentación y Trazabilidad:** Registrar paso a paso cada fase de implementación respaldada por evidencias visuales de terminal y herramientas de prueba.

---

## 2. Arquitectura de Software y Patrón de Diseño

### 2.1 Enfoque Arquitectónico por Capas

El backend adopta un diseño en capas (*Layered Architecture*) con inversión de dependencias:

```text
┌─────────────────────────────────────────────────────────────┐
│                       Clientes / Frontend                   │
└──────────────────────────────┬──────────────────────────────┘
                               │ HTTP / JSON
┌──────────────────────────────▼──────────────────────────────┐
│                    Capa de Controladores / Routers          │
│               (Validación de esquemas, HTTP DTOs)           │
└──────────────────────────────┬──────────────────────────────┘
                               │ Inyección de Servicios
┌──────────────────────────────▼──────────────────────────────┐
│                      Capa de Servicios                      │
│            (Lógica de negocio, reglas de cafetería)         │
└──────────────────────────────┬──────────────────────────────┘
                               │ Repositorios / DAOs
┌──────────────────────────────▼──────────────────────────────┐
│                  Capa de Persistencia / Modelos             │
│            (ORM / Conectores DB, Mapeo Relacional)          │
└──────────────────────────────┬──────────────────────────────┘
                               │ Drivers / SQL Native
┌──────────────────────────────▼──────────────────────────────┐
│              SGBD (MySQL / PostgreSQL / MSSQL / Oracle)     │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 Interoperabilidad Multimotor de Base de Datos

El diseño permite configurar de forma dinámica o configurable mediante variables de entorno cuál motor utilizar para la persistencia, respetando el modelo relacional unificado de **TazaNorte**:
- `customers` (Clientes y fidelización)
- `employees` (Personal y roles)
- `supplies` (Insumos de cafetería)
- `products` (Productos terminados)
- `recipe_supplies` (Recetas y consumo de insumos)
- `cash_shifts` (Turnos y arqueos de caja)
- `orders` (Pedidos y estados)
- `order_details` (Detalles de pedidos)
- `payments` (Transacciones y métodos de pago)
- `point_movements` (Puntos y recompensas de clientes)

---

## 3. Estructura de Directorios del Backend

La estructura del directorio `backend/` ha sido organizada de manera modular para facilitar el mantenimiento y escalabilidad:

```text
backend/
├── capturas/                     # Evidencias visuales y capturas de pantalla del desarrollo
│   ├── .gitkeep
│   ├── 01_inicializacion_backend.png
│   ├── 02_estructura_backend.png
│   ├── 03_dependencias_instaladas.png
│   ├── 04_conexion_db_activa.png
│   ├── 05_servidor_backend_activo.png
│   ├── 06_prueba_endpoints_api.png
│   └── 07_validacion_operaciones.png
├── caps/                         # Acceso directo a carpeta de capturas
│   └── .gitkeep
├── trazabilidad.md               # Documentación y bitácora técnica del backend (este archivo)
├── requirements.txt              # Especificación de dependencias del proyecto
├── .env.example                  # Plantilla de variables de entorno para los 4 motores
├── app/
│   ├── __init__.py
│   ├── main.py                   # Punto de entrada de la aplicación API
│   ├── config.py                 # Carga de configuraciones y credenciales
│   ├── database/                 # Sesiones de conexión y configuración multimotor
│   │   ├── __init__.py
│   │   ├── session.py
│   │   └── base.py
│   ├── models/                   # Definición de entidades relacionales del dominio
│   │   ├── __init__.py
│   │   ├── customer.py
│   │   ├── order.py
│   │   └── product.py
│   ├── schemas/                  # Esquemas Pydantic / DTOs de entrada y salida
│   │   ├── __init__.py
│   │   ├── customer.py
│   │   ├── order.py
│   │   └── product.py
│   ├── repositories/             # Abstracción de acceso a datos (CRUD)
│   │   ├── __init__.py
│   │   └── base_repository.py
│   ├── services/                 # Reglas de negocio del sistema de cafetería
│   │   ├── __init__.py
│   │   └── order_service.py
│   └── routers/                  # Endpoints REST clasificados por entidad
│       ├── __init__.py
│       ├── health.py
│       ├── customers.py
│       ├── products.py
│       └── orders.py
```

---

## 4. Requisitos del Entorno y Dependencias

### 4.1 Creación del Entorno Virtual

Se recomienda el uso de un entorno virtual aislado en Python 3.10+ sobre el entorno WSL2 Ubuntu:

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
```

### 4.2 Configuración de Variables de Entorno (.env)

El archivo `.env` concentra los parámetros de conexión hacia los contenedores de Docker en ejecución:

```env
# Configuración del Servidor Backend
APP_NAME=TazaNorte Backend API
APP_PORT=8000
APP_ENV=development

# Motor Activo (mysql | postgres | mssql | oracle)
ACTIVE_DB_ENGINE=postgres

# Credenciales de Conexión a Motores Docker (Red ia-lab-network / localhost)
MYSQL_URL=mysql+pymysql://admin_user:AdminPassword123*@localhost:3306/TazaNorte
POSTGRES_URL=postgresql+psycopg2://admin_user:AdminPassword123*@localhost:5432/tazanorte
MSSQL_URL=mssql+pyodbc://sa:AdminPassword123*@localhost:1433/tazanorte?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes
ORACLE_URL=oracle+oracledb://ADMIN_USER:AdminPassword123*@localhost:1521/?service_name=XEPDB1
```

---

## 5. Modelado del Dominio y Entidades del Negocio

El esquema del backend mapea directamente las 10 tablas diseñadas y aprovisionadas en los motores relacionales:

| Tabla             | Propósito en el Backend                                                                 |
|-------------------|-----------------------------------------------------------------------------------------|
| `customers`       | Gestión de clientes, saldo de puntos de fidelización y datos de contacto.              |
| `employees`       | Control de accesos, roles (Barista, Cajero, Administrador) y auditoría de operaciones. |
| `supplies`        | Monitoreo de insumos base (café en grano, leche, jarabes, vasos) y stock mínimo.       |
| `products`        | Catálogo de bebidas, alimentos y combos disponibles para venta al público.              |
| `recipe_supplies` | Deducción automática de insumos por cada preparación registrada.                       |
| `cash_shifts`     | Control de apertura y cierre de caja por turno laboral.                                |
| `orders`          | Registro de órdenes de compra, totales, estados (Pendiente, Entregado, Cancelado).     |
| `order_details`   | Detalle granular de ítems, cantidades unitarias y precios aplicados.                   |
| `payments`        | Transacciones monetarias con verificación de inmutabilidad (Efectivo, Tarjeta, Puntos). |
| `point_movements` | Historial inmutable de acumulación y canje de puntos de fidelidad.                     |

---

## 6. Registro de Trazabilidad y Evidencias Visuales

En esta sección se documenta la ejecución sistemática de cada hito de desarrollo del backend, incluyendo el comando ejecutado, la descripción del resultado observado y la captura de pantalla correspondiente.

### 6.1 Evidencia 1: Creación de la Estructura de Directorios del Backend

Se procedió con la creación de la carpeta raíz del backend, la carpeta destinada a las capturas de pantalla de evidencia y la inicialización de los archivos de documentación.

```bash
mkdir -p backend/capturas backend/caps
touch backend/capturas/.gitkeep backend/caps/.gitkeep
```

**Qué se observa:**
Se generó el directorio `backend` en la raíz del espacio de trabajo con la jerarquía correspondiente y el directorio `capturas/` listo para alojar el material fotográfico de auditoría.

**Evidencia:**

![Creación de la Estructura de Directorios](capturas/01_inicializacion_backend.png)

---

### 6.2 Evidencia 2: Inicialización del Entorno Virtual e Instalación de Dependencias

Se preparó el entorno virtual en WSL2 para aislar los paquetes de Python requeridos por el servicio.

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Qué se observa:**
Instalación exitosa de los paquetes base (FastAPI, Uvicorn, SQLAlchemy, Pydantic, y drivers de conexión para MySQL, PostgreSQL, SQL Server y Oracle).

**Evidencia:**

![Instalación de Dependencias](capturas/02_dependencias_instaladas.png)

---

### 6.3 Evidencia 3: Configuración de Variables de Entorno y Pool de Conexiones

Verificación de la carga dinámica de variables desde el archivo `.env` hacia el módulo de configuración centralizado.

```bash
python3 -c "from app.config import settings; print('Motor configurado:', settings.ACTIVE_DB_ENGINE)"
```

**Qué se observa:**
Lectura correcta de parámetros y comprobación de cadenas de conexión seguras sin exponer credenciales en el código fuente.

**Evidencia:**

![Carga de Variables de Entorno](capturas/03_variables_entorno.png)

---

### 6.4 Evidencia 4: Verificación de Conectividad con Motores de Bases de Datos

Prueba de conexión activa desde el backend hacia los contenedores Docker en ejecución (`mysql-server`, `postgres-server`, `mssql-server`, `oracle-server`).

```bash
python3 -m app.database.test_connection
```

**Qué se observa:**
Respuesta exitosa de prueba de *ping/select 1* en el motor activo, confirmando que la red y los puertos mapeados son accesibles.

**Evidencia:**

![Prueba de Conectividad a Base de Datos](capturas/04_conexion_db_activa.png)

---

### 6.5 Evidencia 5: Implementación y Levantamiento del Servidor Backend

Puesta en marcha del servidor de desarrollo ASGI Uvicorn en el puerto 8000.

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Qué se observa:**
El servidor arranca sin errores de sintaxis, montando los routers correspondientes y escuchando peticiones entrantes.

**Evidencia:**

![Servidor Backend Activo](capturas/05_servidor_backend_activo.png)

---

### 6.6 Evidencia 6: Documentación Interactiva de APIs (Swagger / OpenAPI)

Acceso a la interfaz interactiva autogenerada de Swagger UI en `http://localhost:8000/docs`.

```bash
curl -I http://localhost:8000/docs
```

**Qué se observa:**
Carga visual completa de los esquemas, rutas y operaciones documentadas para el sistema TazaNorte.

**Evidencia:**

![Swagger UI Documentación Interactiva](capturas/06_prueba_endpoints_api.png)

---

### 6.7 Evidencia 7: Pruebas Funcionales de Endpoints y Operaciones CRUD

Envío de solicitudes HTTP GET y POST para verificar el flujo de negocio (creación y consulta de clientes, productos y órdenes).

```bash
curl -X GET http://localhost:8000/api/v1/health
curl -X GET http://localhost:8000/api/v1/products/
```

**Qué se observa:**
Respuestas con código de estado HTTP 200 OK y payloads JSON estructurados conforme a los esquemas definidos.

**Evidencia:**

![Pruebas de Endpoints](capturas/07_validacion_operaciones.png)

---

### 6.8 Evidencia 8: Verificación de Persistencia y Auditoría

Confirmación de que los registros insertados a través del backend activan los triggers de auditoría e inmutabilidad configurados previamente en los motores relacionales.

```bash
curl -X POST http://localhost:8000/api/v1/orders/ -H 'Content-Type: application/json' -d '{...}'
```

**Qué se observa:**
Persistencia exitosa en la tabla principal y reflejo automático en las tablas de auditoría (`orders_audit`, `payments_audit`, etc.).

**Evidencia:**

![Verificación de Persistencia y Auditoría](capturas/08_auditoria_persistencia.png)

---

## 7. Conclusiones y Próximos Pasos

1. **Estructura Escalable:** El backend queda articulado bajo principios de arquitectura limpia, facilitando la incorporación de nuevas reglas o clientes front-end.
2. **Compatibilidad Asegurada:** La separación de capas garantiza que la lógica de negocio permanezca desacoplada del motor de base de datos específico.
3. **Trazabilidad Continua:** Cada avance técnico se encuentra registrado con su correspondiente evidencia visual en el directorio `capturas/`, manteniendo el estándar de calidad académica y profesional del proyecto.
