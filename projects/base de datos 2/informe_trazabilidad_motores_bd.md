# Informe de Trazabilidad: Despliegue y Configuracion de 4 Motores de Bases de Datos con Docker Compose

## Informacion del Estudiante

| Campo          | Detalle                                                                                                     |
|----------------|-------------------------------------------------------------------------------------------------------------|
| **Nombre**     | Moises Bolivar                                                                                              |
| **Programa**   | Ingenieria de Sistemas                                                                                      |
| **Facultad**   | Facultad de Ingenieria, Universidad de La Guajira                                                          |
| **Docente**    | Ing. Jaider Quintero M.                                                                                     |
| **Referencia** | [https://tecnogua.com/academic/site/bd/introduccion/](https://tecnogua.com/academic/site/bd/introduccion/) |
| **Fecha**      | 25 de agosto de 2026                                                                                        |

---

## Tabla de Contenido

- [Informacion del Estudiante](#informacion-del-estudiante)
- [1. Introduccion](#1-introduccion)
- [2. Requisitos Previos y Verificacion del Entorno](#2-requisitos-previos-y-verificacion-del-entorno)
  - [2.1 Verificacion de Docker y Docker Compose en WSL](#21-verificacion-de-docker-y-docker-compose-en-wsl)
  - [2.2 Instalacion de Docker (En caso de requerirse)](#22-instalacion-de-docker-en-caso-de-requerirse)
- [3. Paso 1: Creacion de la Estructura de Carpetas](#3-paso-1-creacion-de-la-estructura-de-carpetas)
- [4. Paso 2: Creacion de la Red Docker Compartida](#4-paso-2-creacion-de-la-red-docker-compartida)
- [5. MySQL 8.0 - Motor de Base de Datos](#5-mysql-80---motor-de-base-de-datos)
  - [5.1 Crear el archivo docker-compose.yml](#51-crear-el-archivo-docker-composeyml)
  - [5.2 Crear el archivo .env](#52-crear-el-archivo-env)
  - [5.3 Crear el archivo README.md](#53-crear-el-archivo-readmemd)
  - [5.4 Levantar el contenedor de MySQL](#54-levantar-el-contenedor-de-mysql)
  - [5.5 Conectar Localmente y Operaciones Basicas en MySQL](#55-conectar-localmente-y-operaciones-basicas-en-mysql)
  - [5.6 Crear Usuario con Privilegios de Acceso Remoto](#56-crear-usuario-con-privilegios-de-acceso-remoto)
  - [5.7 Conexion Remota con DBeaver](#57-conexion-remota-con-dbeaver)
  - [5.8 Respaldo (Backup) de la Base de Datos](#58-respaldo-backup-de-la-base-de-datos)
  - [5.9 Tabla Resumen de Variables .env](#59-tabla-resumen-de-variables-env)
- [6. PostgreSQL 17 - Motor de Base de Datos](#6-postgresql-17---motor-de-base-de-datos)
  - [6.1 Crear el archivo docker-compose.yml](#61-crear-el-archivo-docker-composeyml)
  - [6.2 Crear el archivo .env](#62-crear-el-archivo-env)
  - [6.3 Crear el archivo README.md](#63-crear-el-archivo-readmemd)
  - [6.4 Levantar el contenedor de PostgreSQL](#64-levantar-el-contenedor-de-postgresql)
  - [6.5 Conectar Localmente y Operaciones Basicas en PostgreSQL](#65-conectar-localmente-y-operaciones-basicas-en-postgresql)
  - [6.6 Crear Usuario con Privilegios de Acceso Remoto](#66-crear-usuario-con-privilegios-de-acceso-remoto)
  - [6.7 Conexion Remota con DBeaver](#67-conexion-remota-con-dbeaver)
  - [6.8 Respaldo (Backup) de la Base de Datos](#68-respaldo-backup-de-la-base-de-datos)
  - [6.9 Tabla Resumen de Variables .env](#69-tabla-resumen-de-variables-env)
- [7. Microsoft SQL Server 2022 - Motor de Base de Datos](#7-microsoft-sql-server-2022---motor-de-base-de-datos)
  - [7.1 Crear el archivo docker-compose.yml](#71-crear-el-archivo-docker-composeyml)
  - [7.2 Crear el archivo .env](#72-crear-el-archivo-env)
  - [7.3 Crear el archivo README.md](#73-crear-el-archivo-readmemd)
  - [7.4 Levantar el contenedor de SQL Server](#74-levantar-el-contenedor-de-sql-server)
  - [7.5 Instalar mssql-tools18 en WSL](#75-instalar-mssql-tools18-en-wsl)
  - [7.6 Conectar Localmente y Operaciones Basicas en SQL Server](#76-conectar-localmente-y-operaciones-basicas-en-sql-server)
  - [7.7 Crear Usuario con Privilegios de Acceso Remoto](#77-crear-usuario-con-privilegios-de-acceso-remoto)
  - [7.8 Conexion Remota con DBeaver](#78-conexion-remota-con-dbeaver)
  - [7.9 Respaldo (Backup) de la Base de Datos](#79-respaldo-backup-de-la-base-de-datos)
  - [7.10 Tabla Resumen de Variables .env](#710-tabla-resumen-de-variables-env)
- [8. Oracle XE 21c - Motor de Base de Datos](#8-oracle-xe-21c---motor-de-base-de-datos)
  - [8.1 Crear el archivo docker-compose.yml](#81-crear-el-archivo-docker-composeyml)
  - [8.2 Crear el archivo .env](#82-crear-el-archivo-env)
  - [8.3 Crear el archivo README.md](#83-crear-el-archivo-readmemd)
  - [8.4 Levantar el contenedor de Oracle](#84-levantar-el-contenedor-de-oracle)
  - [8.5 Conectar Localmente y Operaciones Basicas en Oracle](#85-conectar-localmente-y-operaciones-basicas-en-oracle)
  - [8.6 Crear Usuario con Privilegios de Acceso Remoto](#86-crear-usuario-con-privilegios-de-acceso-remoto)
  - [8.7 Conexion Remota con DBeaver](#87-conexion-remota-con-dbeaver)
  - [8.8 Respaldo (Backup) de la Base de Datos](#88-respaldo-backup-de-la-base-de-datos)
  - [8.9 Tabla Resumen de Variables .env](#89-tabla-resumen-de-variables-env)
- [Resumen General del Laboratorio](#resumen-general-del-laboratorio)

---

## 1. Introduccion

En este informe documento todo el proceso que segui para desplegar, configurar y verificar cuatro motores de bases de datos (**MySQL 8.0**, **PostgreSQL 17**, **Microsoft SQL Server 2022** y **Oracle XE 21c**) usando contenedores con **Docker Compose** desde mi entorno **WSL2 (Ubuntu)** en Windows.

La idea fue armar un laboratorio local organizado en la ruta `~/ia-lab/services/motores-bd/`, donde cada motor tiene su propia carpeta de configuracion y su propio volumen de datos. Los tres ejes que guiaron el trabajo fueron:

1. **Aislamiento e interoperabilidad:** Cada motor tiene su propio volumen persistente en `~/ia-lab/data/` y todos se comunican a traves de una red compartida llamada `ia-lab-network`.
2. **Seguridad y acceso remoto:** Abri los puertos necesarios con UFW, use archivos `.env` para manejar credenciales y cree usuarios con acceso desde cualquier IP.
3. **Administracion grafica y respaldo:** Conecte DBeaver desde Windows usando la IP del host WSL y genere backups en un volumen montado en `D:\academia\bd`.

---

## 2. Requisitos Previos y Verificacion del Entorno

### 2.1 Verificacion de Docker y Docker Compose en WSL

Lo primero que hice fue verificar que Docker estuviera activo en mi terminal de WSL antes de comenzar cualquier cosa:

```bash
sudo systemctl is-active docker
docker --version
docker compose version
```

**Que observe:**
Execute los tres comandos y confirme que el servicio Docker estaba en estado `active`, y tanto Docker Engine como el plugin de Docker Compose estaban disponibles y listos para usar.

**Evidencia:**

![Verificacion de Docker](Reguistro%20visual/01_verificacion_docker.png.png)

---

### 2.2 Instalacion de Docker (En caso de requerirse)

Este bloque solo se ejecuta si Docker no esta instalado. Lo documente como referencia por si alguien necesita hacerlo desde cero:

```bash
sudo apt update && sudo apt-get update
sudo apt-get install -y ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo systemctl stop unattended-upgrades
sudo apt install -y docker-compose-plugin docker-ce docker-ce-cli containerd.io
```

---

## 3. Paso 1: Creacion de la Estructura de Carpetas

Antes de levantar cualquier contenedor, cree el arbol de directorios completo para tener todo organizado desde el inicio:

```bash
mkdir -p ~/ia-lab/services/motores-bd/{mysql,postgres,mssql,oracle}
mkdir -p ~/ia-lab/data/{mysql,postgres,mssql,oracle}
mkdir -p /mnt/d/academia/bd
```

Luego verifique que la estructura quedara correcta:

```bash
cd ~/ia-lab
tree
```

El resultado que obtuve fue:

```plaintext
~/ia-lab/
+-- services/
|   +-- motores-bd/
|       +-- mysql/
|       +-- postgres/
|       +-- mssql/
|       +-- oracle/
+-- data/
    +-- mysql/
    +-- postgres/
    +-- mssql/
    +-- oracle/
```

**Que observe:**
El comando `tree` mostro exactamente la estructura que necesitaba. Cada motor tiene su carpeta de configuracion en `services/` y su carpeta de datos persistentes en `data/`, completamente separados entre si.

**Evidencia:**

![Estructura de carpetas](Reguistro%20visual/02_estructura_carpetas.png.png)

---

## 4. Paso 2: Creacion de la Red Docker Compartida

Para que todos los contenedores pudieran comunicarse entre si, cree una red de tipo bridge llamada `ia-lab-network`:

```bash
docker network inspect ia-lab-network >/dev/null 2>&1 || docker network create ia-lab-network
```

Luego confirme que quedo registrada:

```bash
docker network ls | grep ia-lab
```

**Que observe:**
La red `ia-lab-network` aparecio listada en modo `bridge`. Todos los contenedores que levante usando esta red pueden verse entre si por nombre.

**Evidencia:**

![Red Docker ia-lab-network](Reguistro%20visual/03_red_docker.png.png)

---

## Instalacion de Motores de Bases de Datos

---

## 5. MySQL 8.0 - Motor de Base de Datos

### 5.1 Crear el archivo `docker-compose.yml`

Entre a la carpeta de MySQL y cree el archivo de orquestacion con la siguiente configuracion:

```bash
cat > ~/ia-lab/services/motores-bd/mysql/docker-compose.yml << 'EOF'
services:
  mysql:
    image: mysql:8.0
    container_name: mysql-server
    restart: unless-stopped
    env_file:
      - .env
    ports:
      - "3306:3306"
    volumes:
      - ../../../data/mysql:/var/lib/mysql
      - /mnt/d/academia/bd:/backups
    command: >
      --character-set-server=utf8mb4
      --collation-server=utf8mb4_unicode_ci
      --bind-address=0.0.0.0
    networks:
      - ia-lab-network
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s

networks:
  ia-lab-network:
    external: true
EOF
```

Despues abri el puerto 3306 en el firewall UFW:

```bash
sudo ufw allow 3306/tcp
sudo ufw enable
sudo ufw status
```

**Que observe:**
El archivo `docker-compose.yml` quedo creado con codificacion `utf8mb4`, escuchando en `0.0.0.0`, con el volumen de datos en `~/ia-lab/data/mysql` y los backups montados en `/backups`. UFW confirmo el puerto `3306/tcp` autorizado.

**Evidencia:**

![MySQL compose y UFW](Reguistro%20visual/04_mysql_compose_ufw.png.png)

---

### 5.2 Crear el archivo `.env`

Cree el archivo de variables de entorno para no poner credenciales directamente en el compose:

```bash
cat > ~/ia-lab/services/motores-bd/mysql/.env << 'EOF'
TZ=America/Bogota
MYSQL_ROOT_PASSWORD=123456
MYSQL_DATABASE=tecnogua
EOF
```

Verifique el contenido del archivo:

```bash
cat ~/ia-lab/services/motores-bd/mysql/.env
```

**Que observe:**
El archivo `.env` mostro correctamente las tres variables: zona horaria `America/Bogota`, contrasena de root `123456` y base de datos inicial `tecnogua` que el contenedor crea automaticamente al arrancar.

**Evidencia:**

![Archivo .env de MySQL](Reguistro%20visual/05_mysql_env.png.png)

---

### 5.3 Crear el archivo `README.md`

Genere un archivo de referencia rapida dentro de la carpeta del servicio:

```bash
cat > ~/ia-lab/services/motores-bd/mysql/README.md << 'EOF'
# MySQL 8.0 - Motor de Base de Datos

> **Acceso remoto habilitado:** Puerto expuesto en `0.0.0.0:3306`.
> **Usuario por defecto:** `root`
> **Base de datos inicial:** `tecnogua`
> **Password:** `123456`

---

## Conectar desde WSL (local)

```bash
sudo docker exec -it mysql-server mysql -u root -p
# Password: 123456
```
EOF
```

**Que observe:**
El archivo `README.md` quedo creado dentro de `~/ia-lab/services/motores-bd/mysql/` con las credenciales y el comando de conexion rapida documentados.

**Evidencia:**

<!-- CAPTURA: Insertar aqui captura de pantalla 06_mysql_readme.png -->
<!-- Sintaxis: ![README de MySQL](Reguistro%20visual/06_mysql_readme.png) -->

&nbsp;

---

### 5.4 Levantar el contenedor de MySQL

Con todo listo, ingrese a la carpeta de MySQL y levante el contenedor en segundo plano:

```bash
cd ~/ia-lab/services/motores-bd/mysql
sudo docker compose up -d
```

Luego verifique que estuviera corriendo y revise los logs iniciales:

```bash
sudo docker ps | grep mysql-server
sudo docker logs mysql-server --tail 20
```

**Que observe:**
El contenedor `mysql-server` aparecio en estado `healthy`, publicando el puerto `0.0.0.0:3306->3306/tcp` y conectado a la red `ia-lab-network`. Los logs confirmaron que MySQL inicializo correctamente la base de datos `tecnogua`.

**Evidencia:**

![Contenedor MySQL activo](Reguistro%20visual/07_mysql_contenedor_activo.png.png)

---

### 5.5 Conectar Localmente y Operaciones Basicas en MySQL

Me conecte directamente a la CLI de MySQL dentro del contenedor:

```bash
sudo docker exec -it mysql-server mysql -u root -p
```

> Ingrese la contrasena: `123456`

Una vez dentro, ejecute las siguientes operaciones:

```sql
CREATE DATABASE bd_clase1 CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
SHOW DATABASES;
USE bd_clase1;
CREATE TABLE estudiante (
  id INT PRIMARY KEY AUTO_INCREMENT,
  nombre VARCHAR(100) NOT NULL,
  programa VARCHAR(100) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
SHOW TABLES;
DESCRIBE estudiante;
EXIT;
```

**Que observe:**
La conexion fue exitosa. `SHOW DATABASES` listo tanto `tecnogua` como `bd_clase1`. La tabla `estudiante` se creo correctamente y `DESCRIBE` mostro todos sus campos con sus tipos de datos.

**Evidencia:**

![Operaciones SQL en MySQL](Reguistro%20visual/08_mysql_operaciones_sql.png.png)

---

### 5.6 Crear Usuario con Privilegios de Acceso Remoto

Para poder conectarme desde DBeaver en Windows, necesitaba un usuario que aceptara conexiones desde cualquier IP. Lo cree asi:

```bash
sudo docker exec -it mysql-server mysql -u root -p123456 -e "
CREATE USER 'admin'@'%' IDENTIFIED BY '123456';
GRANT ALL PRIVILEGES ON *.* TO 'admin'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;
"
```

Verifique los permisos:

```bash
sudo docker exec -it mysql-server mysql -u root -p123456 -e "SELECT User, Host, plugin FROM mysql.user WHERE User = 'admin';"
sudo docker exec -it mysql-server mysql -u root -p123456 -e "SHOW GRANTS FOR 'admin'@'%';"
```

**Que observe:**
El usuario `admin` aparece con `Host = %`, confirmando conexion desde cualquier IP. Los `SHOW GRANTS` mostraron `GRANT ALL PRIVILEGES ON *.* ... WITH GRANT OPTION`.

**Evidencia:**

![Usuario admin MySQL](Reguistro%20visual/09_mysql_usuario_admin.png.png)

---

### 5.7 Conexion Remota con DBeaver

**Paso 1 - Obtuve la IP de WSL:**

```bash
ip a
```

La direccion IPv4 de la interfaz `eth0` que obtuve fue: **`172.30.137.66`**

**Paso 2 - Configure la conexion en DBeaver:**

| Campo             | Valor           |
|-------------------|-----------------|
| Controlador       | MySQL           |
| Host (Servidor)   | `172.30.137.66` |
| Puerto            | `3306`          |
| Base de Datos     | `tecnogua`      |
| Nombre de Usuario | `root`          |
| Contrasena        | `123456`        |

**Que observe:**
DBeaver se conecto exitosamente al motor MySQL 8.0. La prueba de conexion mostro estado verde confirmando comunicacion activa por el puerto 3306.

**Evidencia:**

![IP de WSL obtenida con ip a](Reguistro%20visual/10_mysql_dbeaver_ip.png.png)

![Conexion DBeaver a MySQL exitosa](Reguistro%20visual/11_mysql_dbeaver_conexion.png.png)

---

### 5.8 Respaldo (Backup) de la Base de Datos

Genere un volcado logico de la base de datos `tecnogua` usando `mysqldump`:

```bash
sudo docker exec mysql-server mysqldump -u root -p123456 tecnogua > /mnt/d/academia/bd/backup_tecnogua_$(date +%Y%m%d).sql
```

Verifique que el archivo se genero correctamente:

```bash
ls -lh /mnt/d/academia/bd/backup_tecnogua_*.sql
```

**Que observe:**
El archivo `backup_tecnogua_20260825.sql` aparece en el directorio con su tamano correspondiente. El archivo es accesible directamente desde Windows en `D:\academia\bd\`.

**Evidencia:**

![Backup MySQL generado con mysqldump](Reguistro%20visual/12_mysql_backup.png.png)

---

### 5.9 Tabla Resumen de Variables `.env`

| Variable              | Descripcion                         | Valor Configurado |
|-----------------------|-------------------------------------|-------------------|
| `TZ`                  | Zona horaria del contenedor         | `America/Bogota`  |
| `MYSQL_ROOT_PASSWORD` | Contrasena del superusuario root    | `123456`          |
| `MYSQL_DATABASE`      | Base de datos creada en el arranque | `tecnogua`        |

---

## 6. PostgreSQL 17 - Motor de Base de Datos

### 6.1 Crear el archivo `docker-compose.yml`

Siguiendo el mismo patron que con MySQL, cree el archivo de orquestacion para PostgreSQL:

```bash
cat > ~/ia-lab/services/motores-bd/postgres/docker-compose.yml << 'EOF'
services:
  postgres:
    image: postgres:17
    container_name: postgres-server
    restart: unless-stopped
    env_file:
      - .env
    ports:
      - "5432:5432"
    volumes:
      - ../../../data/postgres:/var/lib/postgresql/data
      - /mnt/d/academia/bd:/backups
    command:
      - postgres
      - -c
      - "listen_addresses=*"
    networks:
      - ia-lab-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U $$POSTGRES_USER -d $$POSTGRES_DB"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 20s

networks:
  ia-lab-network:
    external: true
EOF
```

Abri el puerto 5432 en UFW:

```bash
sudo ufw allow 5432/tcp
sudo ufw enable
sudo ufw status
```

**Que observe:**
El archivo quedo configurado con `listen_addresses=*` para aceptar conexiones remotas. UFW confirmo el puerto `5432/tcp` autorizado.

**Evidencia:**

![PostgreSQL compose y UFW](Reguistro%20visual/13_pg_compose_ufw.png)

---

### 6.2 Crear el archivo `.env`

Cree el archivo de variables de entorno para PostgreSQL y en clase edite la contrasena con `nano`:

```bash
cat > ~/ia-lab/services/motores-bd/postgres/.env << 'EOF'
TZ=America/Bogota
POSTGRES_USER=postgres
POSTGRES_PASSWORD=123456
POSTGRES_DB=tecnogua
EOF
```

**Que observe:**
El archivo `.env` quedo con usuario `postgres`, contrasena `123456` y base de datos inicial `tecnogua`.

**Evidencia:**

![Archivo .env de PostgreSQL](Reguistro%20visual/14_pg_env.png)

---

### 6.3 Crear el archivo `README.md`

Documente las credenciales y comandos de conexion rapida para PostgreSQL:

```bash
cat > ~/ia-lab/services/motores-bd/postgres/README.md << 'EOF'
# PostgreSQL 17 - Motor de Base de Datos

> Puerto: 0.0.0.0:5432 | Usuario: postgres | BD: tecnogua | Password: 123456
EOF
```

**Evidencia:**

![README de PostgreSQL](Reguistro%20visual/15_pg_readme.png)

---

### 6.4 Levantar el contenedor de PostgreSQL

Con la configuracion lista, levante el contenedor:

```bash
cd ~/ia-lab/services/motores-bd/postgres
sudo docker compose up -d
sudo docker ps | grep postgres-server
sudo docker logs postgres-server --tail 20
```

**Que observe:**
El contenedor `postgres-server` arranco en estado `healthy`, publicando el puerto `0.0.0.0:5432->5432/tcp`. Los logs mostraron que PostgreSQL inicializo correctamente la base de datos `tecnogua`.

**Evidencia:**

![Contenedor PostgreSQL activo](Reguistro%20visual/16_pg_contenedor_activo.png)

---

### 6.5 Conectar Localmente y Operaciones Basicas en PostgreSQL

Me conecte a la CLI `psql` dentro del contenedor:

```bash
sudo docker exec -it postgres-server psql -U postgres -d tecnogua
```

Una vez dentro, ejecute las operaciones de practica:

```sql
CREATE DATABASE bd_clase1;
\l
\c bd_clase1
\dt
CREATE TABLE estudiante (
  id SERIAL PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  programa VARCHAR(100) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
\dt
\d estudiante
\q
```

> **Comandos psql utiles:** `\l` lista BDs | `\c nombre` cambia BD | `\dt` lista tablas | `\d tabla` describe campos | `\q` salir

**Que observe:**
La conexion fue exitosa. `\l` listo `tecnogua` y `bd_clase1`. La tabla `estudiante` se creo con `SERIAL` (autoincremental de PostgreSQL) y `\d` mostro todos sus campos.

**Evidencia:**

![Operaciones SQL en PostgreSQL](Reguistro%20visual/17_pg_operaciones_sql.png)

---

### 6.6 Crear Usuario con Privilegios de Acceso Remoto

Desde `psql` como `postgres`, cree el usuario `admin` con rol de superusuario:

```sql
CREATE USER admin WITH PASSWORD '123456';
ALTER USER admin WITH SUPERUSER;
\du
```

**Que observe:**
El comando `\du` mostro la lista de roles. El usuario `admin` aparece con el atributo `Superuser`.

**Evidencia:**

![Usuario admin en PostgreSQL](Reguistro%20visual/18_pg_usuario_admin.png)

---

### 6.7 Conexion Remota con DBeaver

Use la misma IP de WSL (`172.30.137.66`) para conectar DBeaver al servidor PostgreSQL.

| Campo             | Valor           |
|-------------------|-----------------|
| Controlador       | PostgreSQL      |
| Host (Servidor)   | `172.30.137.66` |
| Puerto            | `5432`          |
| Base de Datos     | `tecnogua`      |
| Nombre de Usuario | `postgres`      |
| Contrasena        | `123456`        |

**Que observe:**
DBeaver se conecto correctamente al motor PostgreSQL 17. La prueba de conexion mostro exito y pude ver las bases de datos desde el explorador grafico.

**Evidencia:**

![Conexion DBeaver a PostgreSQL exitosa](Reguistro%20visual/19_pg_dbeaver_conexion.png)

---

### 6.8 Respaldo (Backup) de la Base de Datos

Genere el backup de `tecnogua` usando `pg_dump`:

```bash
sudo docker exec postgres-server pg_dump -U postgres -d tecnogua > /mnt/d/academia/bd/backup_tecnogua_$(date +%Y%m%d).sql
ls -lh /mnt/d/academia/bd/backup_tecnogua_*.sql
```

**Que observe:**
El archivo de backup de PostgreSQL se genero exitosamente en `D:\academia\bd\`.

**Evidencia:**

![Backup PostgreSQL generado con pg_dump](Reguistro%20visual/20_pg_backup.png)

---

### 6.9 Tabla Resumen de Variables `.env`

| Variable            | Descripcion                         | Valor Configurado |
|---------------------|-------------------------------------|-------------------|
| `TZ`                | Zona horaria del contenedor         | `America/Bogota`  |
| `POSTGRES_USER`     | Usuario administrador               | `postgres`        |
| `POSTGRES_PASSWORD` | Contrasena del administrador        | `123456`          |
| `POSTGRES_DB`       | Base de datos creada en el arranque | `tecnogua`        |

> **Nota sobre permisos:** Si el directorio `~/ia-lab/data/postgres/` parece inaccesible ejecuta: `sudo chmod -R 755 ~/ia-lab/data/postgres/`

---

## 7. Microsoft SQL Server 2022 - Motor de Base de Datos

### 7.1 Crear el archivo `docker-compose.yml`

Para SQL Server la configuracion tiene una diferencia importante: hay que agregar `user: root` para que el contenedor pueda escribir en el volumen sin problemas de permisos:

```bash
cat > ~/ia-lab/services/motores-bd/mssql/docker-compose.yml << 'EOF'
services:
  mssql:
    image: mcr.microsoft.com/mssql/server:2022-latest
    container_name: mssql-server
    restart: unless-stopped
    user: root
    env_file:
      - .env
    ports:
      - "0.0.0.0:1433:1433"
    volumes:
      - ../../../data/mssql:/var/opt/mssql
      - /mnt/d/academia/bd:/backups
    networks:
      - ia-lab-network
    healthcheck:
      test: ["CMD-SHELL", "/opt/mssql-tools18/bin/sqlcmd -S localhost -U SA -P $$MSSQL_SA_PASSWORD -C -Q 'SELECT 1' || exit 1"]
      interval: 10s
      timeout: 5s
      retries: 10
      start_period: 40s

networks:
  ia-lab-network:
    external: true
EOF
```

Luego abri el puerto 1433 en el firewall UFW:

```bash
sudo ufw allow 1433/tcp
sudo ufw enable
sudo ufw status
```

**Que observe:**
El archivo `docker-compose.yml` quedo configurado con la imagen oficial de Microsoft, publicando el puerto `1433` en todas las interfaces. UFW confirmo el puerto `1433/tcp` autorizado.

**Evidencia:**

![SQL Server compose y UFW](Reguistro%20visual/21_mssql_compose_ufw.png)

---

### 7.2 Crear el archivo `.env`

El archivo `.env` de SQL Server tiene una estructura diferente. El usuario administrador siempre se llama **SA** (System Administrator). Lo que se configura es la edicion del motor con `MSSQL_PID`:

```bash
cat > ~/ia-lab/services/motores-bd/mssql/.env << 'EOF'
TZ=America/Bogota
ACCEPT_EULA=Y
MSSQL_SA_PASSWORD=MiNiCo57**
MSSQL_PID=Developer
EOF
```

> **Aclaracion importante:** `MSSQL_PID` **no es un usuario**, es la edicion de SQL Server. El usuario administrador siempre es `SA`. Si se escribe `MSSQL_PID=SA`, el contenedor falla.

| Variable | Que es | Valor |
|---|---|---|
| `MSSQL_PID` | Edicion / licencia del motor | `Developer` |
| `MSSQL_SA_PASSWORD` | Contrasena del usuario `SA` | `MiNiCo57**` |

Luego en clase edite la contrasena con `nano` para que cumpla la politica de complejidad de SQL Server (mayuscula, minuscula, numero y simbolo):

```bash
cd ~/ia-lab/services/motores-bd/mssql
sudo nano .env
```

Deje la contrasena como `Abc123456**` y guarde con `Ctrl+O` -> `Ctrl+X`.

**Que observe:**
El archivo `.env` quedo con `ACCEPT_EULA=Y` (obligatorio para iniciar SQL Server), la contrasena de `SA` configurada con caracteres complejos y la edicion `Developer` gratuita para laboratorio.

**Evidencia:**

![Archivo .env de SQL Server](Reguistro%20visual/22_mssql_env.png)

---

### 7.3 Crear el archivo `README.md`

Documente las instrucciones de conexion rapida para SQL Server:

```bash
cat > ~/ia-lab/services/motores-bd/mssql/README.md << 'EOF'
# SQL Server 2022 - Motor de Base de Datos

> Puerto: 0.0.0.0:1433 | Edicion: Developer | Usuario: SA | Password: Abc123456**
EOF
```

**Evidencia:**

![README de SQL Server](Reguistro%20visual/23_mssql_readme.png)

---

### 7.4 Levantar el contenedor de SQL Server

Con todo listo, levante el contenedor:

```bash
cd ~/ia-lab/services/motores-bd/mssql
sudo docker compose up -d
sudo docker ps | grep mssql-server
sudo docker logs mssql-server --tail 20
```

**Que observe:**
El contenedor `mssql-server` arranco y comenzo el proceso de inicializacion. SQL Server tarda mas que MySQL o PostgreSQL (el healthcheck tiene `start_period: 40s`), pero despues aparece en estado `healthy` publicando `0.0.0.0:1433->1433/tcp`.

**Evidencia:**

![Contenedor SQL Server activo](Reguistro%20visual/24_mssql_contenedor_activo.png)

---

### 7.5 Instalar `mssql-tools18` en WSL

A diferencia de MySQL y PostgreSQL, el cliente `sqlcmd` no viene preinstalado en Ubuntu. Lo instale desde el repositorio oficial de Microsoft:

```bash
# 1. Instalar dependencias
sudo apt update && sudo apt install -y curl ca-certificates gnupg

# 2. Eliminar repositorios viejos para evitar conflictos
sudo rm -f /etc/apt/sources.list.d/mssql-release.list
sudo rm -f /etc/apt/sources.list.d/microsoft-prod.list

# 3. Descargar el repositorio de Microsoft para Ubuntu 24.04
cd /tmp
curl -sSL -O https://packages.microsoft.com/config/ubuntu/24.04/packages-microsoft-prod.deb

# 4. Instalar el repositorio
sudo dpkg -i packages-microsoft-prod.deb

# 5. Actualizar e instalar mssql-tools18
sudo apt update
sudo ACCEPT_EULA=Y apt install -y mssql-tools18 unixodbc-dev

# 6. Agregar sqlcmd al PATH
echo 'export PATH="$PATH:/opt/mssql-tools18/bin"' >> ~/.bashrc
source ~/.bashrc

# 7. Verificar instalacion
which sqlcmd
```

El resultado esperado es: `/opt/mssql-tools18/bin/sqlcmd`

**Que observe:**
El comando `which sqlcmd` devolvio la ruta correcta confirmando que `mssql-tools18` quedo instalado y disponible en el PATH de mi sesion de WSL.

**Evidencia:**

![mssql-tools18 instalado en WSL](Reguistro%20visual/25_mssql_tools_instalados.png)

---

### 7.6 Conectar Localmente y Operaciones Basicas en SQL Server

Me conecte a `sqlcmd` directamente desde el contenedor:

```bash
sudo docker exec -it mssql-server /opt/mssql-tools18/bin/sqlcmd -S localhost -U SA -P 'Abc123456**' -C
```

Una vez dentro, ejecute las operaciones de practica. En SQL Server cada bloque termina con `GO`:

```sql
CREATE DATABASE bd_clase1;
GO

SELECT name FROM sys.databases;
GO

USE bd_clase1;
GO

CREATE TABLE estudiante (
  id INT PRIMARY KEY IDENTITY(1,1),
  nombre VARCHAR(100) NOT NULL,
  programa VARCHAR(100) NOT NULL,
  created_at DATETIME DEFAULT GETDATE()
);
GO

SELECT name FROM sys.tables;
GO

SELECT COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'estudiante';
GO

QUIT
```

> **Diferencia clave con MySQL/PostgreSQL:** Cada bloque se ejecuta con `GO`. El autoincremental es `IDENTITY(1,1)` y la fecha por defecto es `GETDATE()`.

**Que observe:**
La conexion fue exitosa. `sys.databases` listo las BDs del sistema mas `bd_clase1`. La tabla `estudiante` se creo con `IDENTITY` como clave primaria.

**Evidencia:**

![Operaciones SQL en SQL Server](Reguistro%20visual/26_mssql_operaciones_sql.png)

---

### 7.7 Crear Usuario con Privilegios de Acceso Remoto

En SQL Server la creacion de usuarios tiene dos niveles: primero un **LOGIN** (acceso al servidor) y luego **privilegios de rol**:

```sql
CREATE LOGIN admin WITH PASSWORD = '123456', CHECK_POLICY = OFF;
GO

ALTER SERVER ROLE sysadmin ADD MEMBER admin;
GO

ALTER LOGIN admin ENABLE;
GO
```

> **Por que `CHECK_POLICY = OFF`?** SQL Server exige contrasenas complejas por defecto. Esta opcion desactiva esa politica solo para este login de practica, permitiendo usar `123456`. La contrasena de `SA` sigue exigiendo complejidad.

**Que observe:**
Los tres comandos ejecutaron sin errores. El usuario `admin` quedo con rol `sysadmin`.

**Evidencia:**

![Usuario admin en SQL Server](Reguistro%20visual/27_mssql_usuario_admin.png)

---

### 7.8 Conexion Remota con DBeaver

Use la misma IP de WSL (`172.30.137.66`). SQL Server tiene dos configuraciones adicionales: el **tipo de autenticacion** y el **cifrado**.

| Campo                    | Valor             |
|--------------------------|-------------------|
| Controlador              | SQL Server        |
| Host (Servidor)          | `172.30.137.66`   |
| Puerto                   | `1433`            |
| Base de Datos            | `tecnogua`        |
| Nombre de Usuario        | `SA`              |
| Contrasena               | `Abc123456**`     |
| Authentication           | SQL Server        |
| Trust server certificate | Activado (true)   |

> **Importante:** Seleccionar **SQL Server Authentication** (no Windows) y activar **Trust server certificate** --- sin esto DBeaver rechaza la conexion porque el contenedor no tiene certificado SSL firmado.

**Que observe:**
DBeaver se conecto exitosamente al motor SQL Server 2022. Al expandir la conexion aparecieron las bases del sistema (`master`, `tempdb`, `model`, `msdb`) mas `bd_clase1`.

**Evidencia:**

![Conexion DBeaver a SQL Server](Reguistro%20visual/28_mssql_dbeaver_conexion.png)

---

### 7.9 Respaldo (Backup) de la Base de Datos

En SQL Server el backup se hace con `BACKUP DATABASE` de T-SQL. El archivo tiene extension `.bak`:

```bash
sudo docker exec mssql-server /opt/mssql-tools18/bin/sqlcmd \
  -S localhost -U SA -P 'Abc123456**' -C \
  -Q "BACKUP DATABASE [tecnogua] TO DISK = N'/backups/backup_tecnogua.bak' WITH INIT"

ls -lh /mnt/d/academia/bd/backup_tecnogua.bak
```

**Que observe:**
SQL Server ejecuto el `BACKUP DATABASE` y genero el archivo `backup_tecnogua.bak` en `D:\academia\bd\`. El archivo `.bak` es el formato nativo de SQL Server y puede restaurarse con `RESTORE DATABASE`.

**Evidencia:**

![Backup SQL Server con BACKUP DATABASE](Reguistro%20visual/29_mssql_backup.png)

---

### 7.10 Tabla Resumen de Variables `.env`

| Variable             | Descripcion                                           | Valor Configurado |
|----------------------|-------------------------------------------------------|-------------------|
| `TZ`                 | Zona horaria del contenedor                           | `America/Bogota`  |
| `ACCEPT_EULA`        | Aceptacion de la licencia de SQL Server (obligatorio) | `Y`               |
| `MSSQL_SA_PASSWORD`  | Contrasena del usuario administrador `SA`             | `Abc123456**`     |
| `MSSQL_PID`          | Edicion del motor (no es usuario, es licencia)        | `Developer`       |



---

## 8. Oracle XE 21c - Motor de Base de Datos

Oracle es el motor mas diferente de los cuatro. La mayor diferencia conceptual es que en Oracle **el usuario ES la base de datos (esquema)** — no se crea un DATABASE separado como en MySQL o PostgreSQL. Crear un usuario es equivalente a crear una base de datos con todo dentro.

### 8.1 Crear el archivo `docker-compose.yml`

Cree el archivo de orquestacion para Oracle en su directorio correspondiente:

```bash
cat > ~/ia-lab/services/motores-bd/oracle/docker-compose.yml << 'EOF'
services:
  oracle:
    image: gvenzl/oracle-xe:21-slim
    container_name: oracle-server
    restart: unless-stopped
    env_file:
      - .env
    ports:
      - "0.0.0.0:1521:1521"
    volumes:
      - ../../../data/oracle:/opt/oracle/oradata
      - /mnt/d/academia/bd:/backups
    networks:
      - ia-lab-network
    healthcheck:
      test: ["CMD", "healthcheck.sh"]
      interval: 10s
      timeout: 5s
      retries: 10
      start_period: 120s

networks:
  ia-lab-network:
    external: true
EOF
```

Luego abri el puerto 1521 en el firewall UFW:

```bash
sudo ufw allow 1521/tcp
sudo ufw enable
sudo ufw status
```

> **Nota tecnica:** El listener de Oracle XE en la imagen `gvenzl/oracle-xe` ya acepta conexiones remotas por defecto. No se usa `command:` aqui porque sustituiria el entrypoint y el contenedor no arrancaria. Los usuarios `SYSTEM` y `admin` no se atan a un host (`@'%'` no existe en Oracle) --- con el puerto 1521 publicado y UFW abierto, DBeaver puede conectarse usando el **Service Name** `tecnogua`.

**Que observe:**
El archivo `docker-compose.yml` quedo configurado con la imagen ligera `gvenzl/oracle-xe:21-slim`, publicando el puerto `1521` en todas las interfaces, datos persistentes en `~/ia-lab/data/oracle` y el directorio de backups montado. UFW confirmo el puerto `1521/tcp` autorizado.

**Evidencia:**

![Oracle compose y UFW](Reguistro%20visual/30_oracle_compose_ufw.png)

&nbsp;

---

### 8.2 Crear el archivo `.env`

El `.env` de Oracle tiene su propia logica. `ORACLE_DATABASE` NO es un usuario --- es el nombre del **PDB (Pluggable Database)** que crea el contenedor. El usuario administrador siempre es **SYSTEM** (o SYS):

```bash
cat > ~/ia-lab/services/motores-bd/oracle/.env << 'EOF'
TZ=America/Bogota
ORACLE_PASSWORD=MiNiCo57**
ORACLE_DATABASE=tecnogua
EOF
```

| Variable | Que es | Valor |
|---|---|---|
| `ORACLE_DATABASE` | PDB / servicio de conexion | `tecnogua` |
| `ORACLE_PASSWORD` | Contrasena de SYSTEM y SYS | `MiNiCo57**` |

Luego en clase intente cambiar la contrasena a `123456` con `nano`:

```bash
cd ~/ia-lab/services/motores-bd/oracle
sudo nano .env
```

> **Advertencia:** Si Oracle rechaza `123456` al arrancar por politica de claves, vuelve a `MiNiCo57**`. El primer arranque puede tardar varios minutos.

**Que observe:**
El archivo `.env` quedo con la zona horaria `America/Bogota`, la contrasena del usuario administrador `SYSTEM` y el nombre del PDB `tecnogua` que el contenedor crea automaticamente.

**Evidencia:**

![Archivo .env de Oracle](Reguistro%20visual/31_oracle_env.png)

&nbsp;

---

### 8.3 Crear el archivo `README.md`

Documente las instrucciones de conexion rapida para Oracle:

```bash
cat > ~/ia-lab/services/motores-bd/oracle/README.md << 'EOF'
# Oracle XE 21c - Motor de Base de Datos

> **Acceso remoto habilitado.** Puerto expuesto en `0.0.0.0:1521`.
> **Usuario por defecto:** `SYSTEM`
> **PDB / Service Name:** `tecnogua`
> **Password:** `MiNiCo57**`

---

## Conectar desde WSL (local)

```bash
sudo docker exec -it oracle-server sqlplus system/MiNiCo57**@tecnogua
```
EOF
```

**Que observe:**
El `README.md` quedo creado con las credenciales de acceso, puerto expuesto y el comando exacto de conexion con `sqlplus`.

**Evidencia:**

![README de Oracle](Reguistro%20visual/32_oracle_readme.png)

&nbsp;

---

### 8.4 Levantar el contenedor de Oracle

Oracle es el mas lento de los cuatro en arrancar. El healthcheck tiene `start_period: 120s`, lo que significa que puede tardar hasta 2 minutos en estar listo:

```bash
cd ~/ia-lab/services/motores-bd/oracle
sudo docker compose up -d
```

Verifique el estado y los logs:

```bash
sudo docker ps | grep oracle-server
sudo docker logs oracle-server --tail 20
```

**Que observe:**
El contenedor `oracle-server` aparecio en la lista. A diferencia de los otros motores, los logs de Oracle muestran varias fases de inicializacion del PDB `tecnogua` antes de quedar en estado `healthy`. Espere hasta que el log mostrara el mensaje de "DATABASE IS READY TO USE".

**Evidencia:**

![Contenedor Oracle activo](Reguistro%20visual/contenedororacle.png)

&nbsp;

---

### 8.5 Conectar Localmente y Operaciones Basicas en Oracle

Me conecte al shell del contenedor y desde ahi entre a `sqlplus` como `SYS` en modo `SYSDBA` (el equivalente a root/SA en Oracle):

```bash
docker exec -it oracle-server bash

sqlplus sys/MiNiCo57** as sysdba
```

Una vez dentro, ejecute las operaciones. En Oracle, **crear un usuario ES crear una base de datos (esquema)**:

```sql
-- Crear un usuario/esquema de practica (equivalente a CREATE DATABASE)
CREATE USER almacendb_admin IDENTIFIED BY "MiNiCo57**"
  DEFAULT TABLESPACE USERS
  QUOTA UNLIMITED ON USERS;

-- Dar cuota y permisos de conexion
ALTER USER almacendb_admin QUOTA UNLIMITED ON USERS;
GRANT CONNECT, RESOURCE TO almacendb_admin;

-- Listar todos los esquemas/usuarios del sistema
SELECT username FROM all_users ORDER BY username;

-- Entrar al usuario creado (equivalente a USE database)
CONN almacendb_admin/MiNiCo57**

-- Listar tablas del usuario actual
SELECT table_name FROM user_tables;

-- Crear tabla de prueba
CREATE TABLE estudiante (
  id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  nombre VARCHAR2(100) NOT NULL,
  programa VARCHAR2(100) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Describir estructura de la tabla
DESC estudiante;

-- Salir
EXIT;
```

> **Diferencias clave con los otros motores:**
> | Concepto | MySQL/PostgreSQL | Oracle |
> |---|---|---|
> | Crear BD | `CREATE DATABASE` | `CREATE USER` |
> | Cambiar BD | `USE nombre` / `\c nombre` | `CONN usuario/pass` |
> | Ver tablas | `SHOW TABLES` / `\dt` | `SELECT table_name FROM user_tables` |
> | Describir tabla | `DESCRIBE` / `\d` | `DESC nombre_tabla` |
> | Autoincremental | `AUTO_INCREMENT` / `SERIAL` | `GENERATED ALWAYS AS IDENTITY` |

**Que observe:**
La conexion como `SYS SYSDBA` fue exitosa. Cree el usuario `almacendb_admin`, le di permisos con `GRANT CONNECT, RESOURCE` y entre a su esquema con `CONN`. La tabla `estudiante` se creo usando la sintaxis propia de Oracle (`VARCHAR2`, `NUMBER`, `IDENTITY`).

**Evidencia:**

![Operaciones SQL en Oracle](Reguistro%20visual/34_oracle_operaciones_sql.png)

&nbsp;

---

### 8.6 Crear Usuario con Privilegios de Acceso Remoto

Conectado como `SYS` en modo `SYSDBA`, cree el usuario `admin` para administracion remota desde DBeaver:

```sql
-- Crear usuario admin con contrasena simple
-- Si Oracle rechaza 123456, primero deshabilitar la politica de complejidad:
ALTER PROFILE DEFAULT LIMIT PASSWORD_VERIFY_FUNCTION NULL;

-- Crear el usuario admin
CREATE USER admin IDENTIFIED BY "123456"
  DEFAULT TABLESPACE USERS
  QUOTA UNLIMITED ON USERS;

-- Dar permisos de conexion y recursos
ALTER USER admin QUOTA UNLIMITED ON USERS;
GRANT CONNECT, RESOURCE TO admin;
```

Luego entre al usuario admin para verificar:

```sql
CONN admin/"123456"

SELECT username FROM all_users ORDER BY username;
SELECT table_name FROM user_tables;
EXIT;
```

**Que observe:**
El usuario `admin` se creo exitosamente con contrasena `123456`. Al entrar con `CONN admin/"123456"` pude ver los objetos del esquema. El `SELECT username FROM all_users` confirmo que `ADMIN` aparece listado entre los usuarios del sistema.

**Evidencia:**

![Usuario admin en Oracle](Reguistro%20visual/35_oracle_usuario_admin.png)

&nbsp;

---

### 8.7 Conexion Remota con DBeaver

Para conectar DBeaver desde Windows a Oracle en WSL use la misma IP (`172.30.137.66`). Oracle usa **Service Name** en lugar de nombre de base de datos:

**Parametros configurados en DBeaver:**

| Campo          | Valor           |
|----------------|-----------------|
| Controlador    | Oracle          |
| Host           | `172.30.137.66` |
| Puerto         | `1521`          |
| Database / Service Name | `tecnogua` |
| Connection Type | Service Name (NO SID) |
| Nombre de Usuario | `SYSTEM`     |
| Contrasena     | `MiNiCo57**`   |
| Role           | Default         |

> **Importante:** Seleccionar **Service Name** (no SID). El nombre del servicio es `tecnogua` que es el PDB configurado en el `.env`. Si se usa `XE` como SID, se conecta al contenedor raiz y no al PDB. El usuario de conexion es `SYSTEM` --- nunca `tecnogua`.

**Que observe:**
DBeaver se conecto al motor Oracle XE 21c usando el Service Name `tecnogua`. Al expandir la conexion aparecio el esquema de `SYSTEM` con las tablas del sistema y pude navegar por los otros esquemas creados.

**Evidencia:**

![Conexion DBeaver a Oracle](Reguistro%20visual/36_oracle_dbeaver_conexion.png)

&nbsp;

---

### 8.8 Respaldo (Backup) de la Base de Datos

En Oracle el backup se hace con `expdp` (Data Pump Export), la herramienta nativa para exportar esquemas y bases de datos. Genera un archivo `.dmp`:

```bash
sudo docker exec oracle-server expdp system/MiNiCo57**@tecnogua \
  directory=DATA_PUMP_DIR \
  dumpfile=backup_tecnogua.dmp \
  logfile=backup_tecnogua.log
```

Verifique que el archivo se genero:

```bash
sudo docker exec oracle-server ls -lh /opt/oracle/oradata/
ls -lh /mnt/d/academia/bd/
```

**Que observe:**
`expdp` ejecuto el proceso de exportacion mostrando el progreso en consola. El archivo `backup_tecnogua.dmp` quedo generado dentro del contenedor en el directorio `DATA_PUMP_DIR`. A diferencia de los otros motores, el backup de Oracle se genera dentro del contenedor y puede copiarse al exterior con `docker cp`.

**Evidencia:**

![Backup Oracle con expdp](Reguistro%20visual/37_oracle_backup.png)

&nbsp;

---

### 8.9 Tabla Resumen de Variables `.env`

| Variable          | Descripcion                                      | Valor Configurado |
|-------------------|--------------------------------------------------|-------------------|
| `TZ`              | Zona horaria del contenedor                      | `America/Bogota`  |
| `ORACLE_PASSWORD` | Contrasena de los usuarios SYSTEM y SYS          | `MiNiCo57**`      |
| `ORACLE_DATABASE` | Nombre del PDB / Service Name (no es un usuario) | `tecnogua`        |

> **Recordatorio final:** `ORACLE_DATABASE=tecnogua` es el PDB. Al conectar desde DBeaver o `sqlplus`, el usuario es `SYSTEM` --- nunca `tecnogua`. Usar **Service Name**, no SID.

---

## Resumen General del Laboratorio

Con los cuatro motores desplegados y verificados, el laboratorio quedo completamente operativo. A continuacion el resumen de acceso a cada motor:

| Motor           | Puerto | Usuario Admin | Contrasena    | BD / Servicio |
|-----------------|--------|---------------|---------------|---------------|
| MySQL 8.0       | `3306` | `root`        | `123456`      | `tecnogua`    |
| PostgreSQL 17   | `5432` | `postgres`    | `123456`      | `tecnogua`    |
| SQL Server 2022 | `1433` | `SA`          | `Abc123456**` | `tecnogua`    |
| Oracle XE 21c   | `1521` | `SYSTEM`      | `MiNiCo57**`  | `tecnogua` (Service Name) |

Todos los contenedores estan conectados a la red `ia-lab-network`, con volúmenes persistentes en `~/ia-lab/data/` y backups accesibles desde Windows en `D:\academia\bd\`.