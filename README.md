# 🗄️ Trazabilidad y Despliegue de Motores de Bases de Datos con Docker

[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)](https://ubuntu.com/)
[![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)](https://www.mysql.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Microsoft SQL Server](https://img.shields.io/badge/Microsoft%20SQL%20Server-CC292B?style=for-the-badge&logo=microsoftsqlserver&logoColor=white)](https://www.microsoft.com/sql-server)
[![Oracle](https://img.shields.io/badge/Oracle-F80000?style=for-the-badge&logo=oracle&logoColor=white)](https://www.oracle.com/database/)

Repositorio del proyecto e informe de laboratorio enfocado en la **instalación, configuración, trazabilidad y gestión de 4 motores de bases de datos relacionales** containerizados mediante Docker sobre entorno Linux (Ubuntu / WSL2).

---

## 📋 Tabla de Contenidos
1. [Descripción del Proyecto](#-descripción-del-proyecto)
2. [Requisitos Previos](#-requisitos-previos)
3. [Estructura del Repositorio](#-estructura-del-repositorio)
4. [Guía de Despliegue](#-guía-de-despliegue)
5. [Credenciales y Puertos de Conexión](#-credenciales-y-puertos-de-conexión)
6. [Operaciones y Pruebas en Motores](#-operaciones-y-pruebas-en-motores)
7. [Documentación e Informes](#-documentación-e-informes)
8. [Autor](#-autor)

---

## 📖 Descripción del Proyecto

El objetivo de este proyecto es documentar la trazabilidad completa en la creación, administración e interacción con diversos Sistemas Gestores de Bases de Datos (SGBD) utilizando contenedores Docker. 

**Capacidades abordadas:**
* Aislamiento de entornos y configuración de volúmenes persistentes.
* Despliegue y administración de instancias (MySQL 8.0, PostgreSQL 17, MSSQL 2022, Oracle XE 21c).
* Ejecución de scripts DDL (definición de esquemas) y DML (manipulación y consulta de datos).
* Pruebas de conectividad local y remota (DBeaver).
* Generación y verificación de respaldos (backups).

---

## 🛠️ Requisitos Previos

Asegúrate de contar con el siguiente entorno configurado:

* **Sistema Operativo:** Ubuntu 22.04+ / WSL2 (Windows Subsystem for Linux).
* **Docker Engine & CLI:** Versión 24.0 o superior.
* **Docker Compose:** Plugin v2+.
* **Cliente de Base de Datos:** DBeaver Community.

---

## 📂 Estructura del Repositorio

```text
├── README.md                                    # Documentación principal del repositorio
├── .gitignore                                   # Archivos y carpetas ignorados por git
├── services/
│   └── motores-bd/                              # Servicios Docker Compose por motor
│       ├── mysql/                               # Configuración y compose de MySQL 8.0
│       ├── postgres/                            # Configuración y compose de PostgreSQL 17
│       ├── mssql/                               # Configuración y compose de SQL Server 2022
│       └── oracle/                              # Configuración y compose de Oracle XE 21c
└── projects/
    └── base de datos 2/
        ├── informe_trazabilidad_motores_bd.md    # Informe técnico detallado de la práctica
        └── Reguistro visual/                     # Evidencias y capturas de pantalla del paso a paso
```

---

## 🚀 Guía de Despliegue

### 1. Crear la red compartida de Docker
```bash
sudo docker network create ia-lab-network
```

### 2. Iniciar los contenedores con Docker Compose
Puedes levantar cada servicio desde su respectiva carpeta en `services/motores-bd/`:

```bash
# Levantar MySQL
cd services/motores-bd/mysql
sudo docker compose up -d

# Levantar PostgreSQL
cd ../postgres
sudo docker compose up -d

# Levantar Microsoft SQL Server
cd ../mssql
sudo docker compose up -d

# Levantar Oracle XE
cd ../oracle
sudo docker compose up -d
```

### 3. Verificar el estado de los servicios
```bash
sudo docker ps
```

---

## 🔑 Credenciales y Puertos de Conexión

| Motor | Contenedor | Puerto Host | Usuario | Contraseña | Base de Datos por Defecto |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **MySQL 8.0** | `mysql-server` | `3306` | `root` | `123456` | `bd_clase1` / `tecnogua` |
| **PostgreSQL 17** | `postgres-server` | `5432` | `postgres` | `123456` | `postgres` / `tecnogua` |
| **Microsoft SQL Server 2022** | `mssql-server` | `1433` | `sa` | `Abc123456**` | `master` / `tecnogua` |
| **Oracle Database 21c XE** | `oracle-server` | `1521` | `system` / `SYS` | `MiNiCo57**` | `tecnogua` / `XEPDB1` |

---

## 💻 Operaciones y Pruebas en Motores

### Acceso a la consola de MySQL
```bash
sudo docker exec -it mysql-server mysql -u root -p
```
*(Contraseña: `123456`)*

### Acceso a la consola de PostgreSQL
```bash
sudo docker exec -it postgres-server psql -U postgres -d tecnogua
```
*(Contraseña: `123456`)*

### Acceso a la consola de Microsoft SQL Server
```bash
sudo docker exec -it mssql-server /opt/mssql-tools18/bin/sqlcmd -S localhost -U SA -P "Abc123456**" -C
```

### Acceso a la consola de Oracle Database
```bash
sudo docker exec -it oracle-server sqlplus system/MiNiCo57**@//localhost:1521/tecnogua
```

---

## 📑 Documentación e Informes

Para consultar el paso a paso detallado con todas las evidencias, comandos ejecutados y resultados de las pruebas, revisa el archivo principal:
👉 **[informe_trazabilidad_motores_bd.md](projects/base%20de%20datos%202/informe_trazabilidad_motores_bd.md)**

---

## 👤 Autor

* **Estudiante:** Moises Bolivar
* **Programa:** Ingeniería de Sistemas - Universidad de La Guajira
* **Docente:** Ing. Jaider Quintero M.
* **Fecha:** 2026
