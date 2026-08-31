# 🗄️ Trazabilidad y Despliegue de Motores de Bases de Datos con Docker

[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)](https://ubuntu.com/)
[![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)](https://www.mysql.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white)](https://www.mongodb.com/)

Repositorio del proyecto e informe de laboratorio enfocado en la **instalación, configuración, trazabilidad y gestión de motores de bases de datos relacionales y no relacionales** containerizados mediante Docker sobre entorno Linux (Ubuntu / WSL2).

---

## 📋 Tabla de Contenidos
1. [Descripción del Proyecto](#-descripción-del-proyecto)
2. [Requisitos Previos](#-requisitos-previos)
3. [Estructura del Repositorio](#-estructura-del-repositorio)
4. [Guía de Despliegue](#-guía-de-despliegue)
5. [Credenciales y Puertos de Conexión](#-credenciales-y-puertos-de-conexión)
6. [Operaciones y Pruebas en Motores](#-operaciones-y-pruebas-en-motores)
7. [Documentación e Informes](#-documentación-e-informes)
8. [Autores y Créditos](#-autores-y-créditos)

---

## 📖 Descripción del Proyecto

El objetivo de este proyecto es documentar la trazabilidad completa en la creación, administración e interacción con diversos Sistemas Gestores de Bases de Datos (SGBD) utilizando contenedores Docker. 

**Capacidades abordadas:**
* Aislamiento de entornos y configuración de volúmenes persistentes.
* Despliegue y administración de instancias (MySQL, PostgreSQL, MongoDB, entre otros).
* Ejecución de scripts DDL (definición de esquemas) y DML (manipulación y consulta de datos).
* Pruebas de conectividad y verificación de consistencia.

---

## 🛠️ Requisitos Previos

Asegúrate de contar con el siguiente entorno configurado:

* **Sistema Operativo:** Ubuntu 22.04+ / WSL2 (Windows Subsystem for Linux).
* **Docker Engine & CLI:** Versión 24.0 o superior.
* **Docker Compose:** (Opcional pero recomendado).
* **Cliente de Base de Datos (Opcional):** DBeaver, MySQL Workbench, pgAdmin o Compass.

---

## 📂 Estructura del Repositorio

```text
├── informe_trazabilidad_motores_bd.md   # Informe técnico detallado de la práctica
├── docker-compose.yml                  # Orquestación de los contenedores
├── scripts/                            # Scripts de inicialización y pruebas SQL/NoSQL
│   ├── mysql_init.sql
│   └── postgres_init.sql
├── docs/                               # Diagramas, capturas y evidencias
└── README.md                           # Documentación principal del repositorio
```

---

## 🚀 Guía de Despliegue

### 1. Iniciar los contenedores

#### Opción A: Despliegue individual con Docker CLI (Ejemplo MySQL)
```bash
sudo docker run -d \
  --name mysql-server \
  -p 3306:3306 \
  -e MYSQL_ROOT_PASSWORD=123456 \
  -v mysql_data:/var/lib/mysql \
  mysql:latest
```

#### Opción B: Despliegue con Docker Compose
```bash
docker compose up -d
```

### 2. Verificar el estado de los servicios
```bash
sudo docker ps
```

---

## 🔑 Credenciales y Puertos de Conexión

| Motor | Contenedor | Puerto Host | Usuario | Contraseña | Base de Datos por Defecto |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **MySQL** | `mysql-server` | `3306` | `root` | `123456` | `bd_clase1` |
| **PostgreSQL** | `postgres-server` | `5432` | `postgres` | `123456` | `postgres` |
| **MongoDB** | `mongo-server` | `27017` | `root` | `123456` | `admin` |

---

## 💻 Operaciones y Pruebas en Motores

### Acceso a la consola de MySQL
```bash
sudo docker exec -it mysql-server mysql -u root -p
```
*(Ingresar la contraseña: `123456`)*

#### Comandos SQL de verificación:
```sql
-- Creación de la base de datos
CREATE DATABASE bd_clase1 CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
SHOW DATABASES;
USE bd_clase1;

-- Creación de tabla de prueba
CREATE TABLE estudiante (
  id INT PRIMARY KEY AUTO_INCREMENT,
  nombre VARCHAR(100) NOT NULL,
  email VARCHAR(100) UNIQUE,
  fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Inserción y consulta
INSERT INTO estudiante (nombre, email) VALUES ('Juan Perez', 'juan.perez@example.com');
SELECT * FROM estudiante;
```

---

## 📑 Documentación e Informes

Para consultar el paso a paso detallado con todas las evidencias, comandos ejecutados y resultados de las pruebas, revisa el archivo principal:
👉 **[informe_trazabilidad_motores_bd.md](./informe_trazabilidad_motores_bd.md)**

---

## 👤 Autor

* **Desarrollador / Estudiante:** Proyecto de Laboratorio de Bases de Datos
* **Fecha:** 2026
