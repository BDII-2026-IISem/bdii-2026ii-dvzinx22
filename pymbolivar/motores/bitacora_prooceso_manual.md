# ☕ Creación de Base de Datos - TazaNorte

<p align="center">
  <img src="https://img.shields.io/badge/Project-TazaNorte_Cafetería-6F4E37?style=for-the-badge&logo=coffeescript&logoColor=white" alt="TazaNorte" />
  <img src="https://img.shields.io/badge/MySQL-005C84?style=for-the-badge&logo=mysql&logoColor=white" alt="MySQL" />
  <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL" />
  <img src="https://img.shields.io/badge/MSSQL_Server-CC292B?style=for-the-badge&logo=microsoftsqlserver&logoColor=white" alt="MSSQL Server" />
  <img src="https://img.shields.io/badge/Oracle_Database-F80000?style=for-the-badge&logo=oracle&logoColor=white" alt="Oracle" />
  <img src="https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white" alt="Ubuntu" />
</p>

---

## 🖥️ Apertura de las bases de datos en terminal

Para la inicialización y aprovisionamiento de las bases de datos en cada motor de persistencia relacional, se estableció sesión directa a través de la terminal de **Ubuntu (WSL)** empleando las credenciales de administración previamente configuradas. A continuación, se detallan las instrucciones ejecutadas en la interfaz de línea de comandos (CLI) de cada motor:

### <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/mysql/mysql-original.svg" width="22" height="22" /> MySQL

```sql
CREATE DATABASE TazaNorte;
```

### <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/postgresql/postgresql-original.svg" width="22" height="22" /> PostgreSQL

```postgres
CREATE DATABASE tazanorte;
```

### <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/microsoftsqlserver/microsoftsqlserver-plain.svg" width="22" height="22" /> MSSQL Server

```sql
CREATE DATABASE tazanorte;

GO
```

### <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/oracle/oracle-original.svg" width="22" height="22" /> Oracle Database

```sql
-- En Oracle la organización de datos se realiza a través de usuarios y esquemas:
CREATE USER tazanorte IDENTIFIED BY "TazaNorte2026*";
GRANT CONNECT, RESOURCE, DBA TO tazanorte;
ALTER USER tazanorte QUOTA UNLIMITED ON USERS;
```

---

### 📸 Ejecución

A continuación se documenta el proceso de invocación de los motores de bases de datos y la creación de cada instancia desde la terminal:

![Apertura de las bases de datos](./evidencias_bitacora/creacion_de_base_de_datos.png)

---

### 🔍 Evidencia

Confirmación visual de las bases de datos creadas y disponibles para su gestión y conexión desde herramientas de administración:

![Bases de datos abiertas](./evidencias_bitacora/bds_creadas.png)

---

## 📋 Anotaciones y Convenciones de Diseño

Para garantizar uniformidad, escalabilidad y compatibilidad con arquitecturas limpias y Domain-Driven Design (DDD), se aplicaron los siguientes estándares en todas las implementaciones:

- 🏷️ **Entidades de Dominio:** Se estructuran como objetos en lenguaje **inglés**, empleando notación **PascalCase** y en formato **singular** (ejemplo: `Customer`, `Product`, `Order`, `CashShift`).
- 🗄️ **Tablas Físicas:** Se nombran en **inglés**, en **minúsculas** y en formato **plural** utilizando la convención **snake_case** (ejemplo: `customers`, `products`, `orders`, `cash_shifts`).
- 📝 **Atributos y Columnas:** Todos los campos se encuentran definidos en **inglés** bajo el formato **snake_case** (ejemplo: `document_type`, `unit_of_measure`, `created_at`).
- 🔑 **Claves Primarias:** Cada tabla cuenta con una llave primaria unificada e indexada denominada **`id`**, configurada como tipo entero de alta capacidad (**`BIGINT`** o su equivalente nativo).
- 🔗 **Claves Foráneas (FK):** Siguen la regla estricta del nombre de la entidad/tabla relacionada en **singular** acompañado del sufijo **`_id`** (ejemplo: `customer_id`, `product_id`, `employee_id`, `cash_shift_id`).
- ⏱️ **Trazabilidad y Auditoría Temporal:** Todas las tablas registran automáticamente los sellos temporales **`created_at`** y **`updated_at`**, asegurando un histórico cronológico inalterable.
- 🛡️ **Restricciones de Integridad y Unicidad:** Aquellos atributos que no admiten duplicidad (como documentos de identidad, códigos SKU e identificadores de insumos) están resguardados por restricciones **`UNIQUE`**.
- 🚦 **Gestión de Estados (Soft Control):** Se integra una columna de control de ciclo de vida (`status` o `is_active`) para permitir bajas lógicas e inhabilitaciones sin perder trazabilidad transaccional.
- 📐 **Diagramación Relacional:** Una vez completada la persistencia física en cada motor, se genera y valida el respectivo Diagrama Entidad-Relación (ER) mediante DBeaver.

---

# 📊 Tablas del Dominio

**TazaNorte** es una plataforma de software diseñada para la operación omnicanal de cafeterías y puntos de venta especializados. El sistema centraliza la gestión de pedidos tanto en caja como para llevar, capturando especificaciones personalizadas (variantes de leche, endulzantes, extras y observaciones de baristas), coordinando el envío de comandas a la zona de preparación, controlando el inventario crítico de insumos mediante recetas predefinidas y auditando la apertura y cierre de turnos de caja. Asimismo, administra un programa de fidelización por puntos que acredita saldos auditables únicamente sobre ventas liquidadas y autoriza redenciones controladas.

A continuación, se presenta la matriz de entidades y tablas físicas del dominio:

| Entidad | Tabla | Atributos / Claves sugeridos |
|---|---|---|
| **Customer** | `customers` | `id (PK)`, `document_type`, `document_number (UQ)`, `name`, `phone`, `email`, `status / is_active`, `created_at`, `updated_at` |
| **Employee** | `employees` | `id (PK)`, `name`, `description`, `status / is_active`, `created_at`, `updated_at` |
| **Supply** | `supplies` | `id (PK)`, `code (UQ)`, `name`, `unit_of_measure`, `min_stock`, `status / is_active`, `created_at`, `updated_at` |
| **Product** | `products` | `id (PK)`, `sku (UQ)`, `name`, `description`, `price`, `status / is_active`, `created_at`, `updated_at` |
| **RecipeSupply** | `recipe_supplies` | `id (PK)`, `product_id (FK)`, `supply_id (FK)`, `quantity`, `status / is_active`, `created_at`, `updated_at` |
| **CashShift** | `cash_shifts` | `id (PK)`, `employee_id (FK)`, `name`, `description`, `opened_at`, `closed_at`, `initial_balance`, `final_balance`, `status`, `created_at`, `updated_at` |
| **Order** | `orders` | `id (PK)`, `customer_id (FK)`, `cash_shift_id (FK)`, `channel`, `order_date`, `subtotal`, `total`, `status`, `created_at`, `updated_at` |
| **OrderDetail** | `order_details` | `id (PK)`, `order_id (FK)`, `product_id (FK)`, `quantity`, `unit_price`, `total`, `observations`, `created_at`, `updated_at` |
| **Payment** | `payments` | `id (PK)`, `reference_type`, `reference_id`, `method`, `amount`, `payment_date`, `status`, `created_at`, `updated_at` |
| **PointMovement** | `point_movements` | `id (PK)`, `customer_id (FK)`, `order_id (FK)`, `reference_type`, `reference_id`, `movement_type`, `points`, `movement_date`, `observations`, `status`, `created_at`, `updated_at` |

> [!NOTE]
> **Consideraciones de Modelo y Trazabilidad:**
> 1. En la guía del proyecto, el atributo `origen_id` del Pedido corresponde conceptualmente al turno de caja o punto de origen de venta (`cash_shift_id`), materializando la relación `TurnoCaja 1:N Pedido`.
> 2. La relación N:M entre `Product` e `Supply` se resuelve a través de la entidad asociativa `RecipeSupply` (`recipe_supplies`), lo que permite el descuento automático de inventario según las porciones formuladas en cada bebida.
> 3. La entidad `PointMovement` garantiza la auditoría estricta de fidelización, almacenando tanto la acumulación por compras pagadas como la redención de beneficios, preservando la integridad histórica de los balances del cliente.


---

# 🐬 Base de datos en MySQL - Scripts DBeaver

## 1. Creación de la tabla Customers

La tabla `customers` almacena la información de los clientes registrados en la cafetería para su identificación, historial de pedidos y acumulación de puntos en el programa de fidelización.

### Código SQL

```sql
CREATE TABLE customers (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    document_type VARCHAR(30) NOT NULL,
    document_number VARCHAR(50) NOT NULL UNIQUE,
    name VARCHAR(150) NOT NULL,
    phone VARCHAR(30),
    email VARCHAR(150),
    status ENUM('active', 'inactive') DEFAULT 'active',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### Evidencia en DBeaver

![Crear customers en MySQL](./evidencias_bitacora/scripts-mysql/image-1.png)

---

## 2. Creación de la tabla Employees

La tabla `employees` almacena los datos de los baristas, cajeros y supervisores encargados de los turnos y pedidos.

### Código SQL

```sql
CREATE TABLE employees (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    description TEXT,
    status ENUM('active', 'inactive') DEFAULT 'active',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### Evidencia en DBeaver

![Crear employees en MySQL](./evidencias_bitacora/scripts-mysql/image-2.png)

---

## 3. Creación de la tabla Supplies

La tabla `supplies` (Insumos) almacena los ingredientes base (café en grano, leche, jarabes, vasos) y su stock mínimo.

### Código SQL

```sql
CREATE TABLE supplies (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(50) NOT NULL UNIQUE,
    name VARCHAR(150) NOT NULL,
    unit_of_measure VARCHAR(30) NOT NULL,
    min_stock DECIMAL(15,3) NOT NULL DEFAULT 0,
    status ENUM('active', 'inactive') DEFAULT 'active',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### Evidencia en DBeaver

![Crear supplies en MySQL](./evidencias_bitacora/scripts-mysql/image-3.png)

---

## 4. Creación de la tabla Products

La tabla `products` contiene el catálogo de bebidas y alimentos disponibles en la cafetería.

### Código SQL

```sql
CREATE TABLE products (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    sku VARCHAR(100) NOT NULL UNIQUE,
    name VARCHAR(150) NOT NULL,
    description TEXT,
    price DECIMAL(15,2) NOT NULL,
    status ENUM('active', 'inactive') DEFAULT 'active',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### Evidencia en DBeaver

![Crear products en MySQL](./evidencias_bitacora/scripts-mysql/image-4.png)

---

## 5. Creación de la tabla RecipeSupplies

La tabla `recipe_supplies` materializa la relación N:M entre `products` e `supplies`, definiendo qué insumos y en qué cantidad componen cada producto.

### Código SQL

```sql
CREATE TABLE recipe_supplies (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    product_id BIGINT NOT NULL,
    supply_id BIGINT NOT NULL,
    quantity DECIMAL(15,3) NOT NULL,
    status ENUM('active', 'inactive') DEFAULT 'active',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_recipe_supplies_product
        FOREIGN KEY (product_id) REFERENCES products(id),
    CONSTRAINT fk_recipe_supplies_supply
        FOREIGN KEY (supply_id) REFERENCES supplies(id),
    CONSTRAINT uq_product_supply UNIQUE (product_id, supply_id)
);
```

### Evidencia en DBeaver

![Crear recipe_supplies en MySQL](./evidencias_bitacora/scripts-mysql/image-5.png)

---

## 6. Creación de la tabla CashShifts

La tabla `cash_shifts` administra la apertura, control y cierre de turnos de caja asignados a cada empleado.

### Código SQL

```sql
CREATE TABLE cash_shifts (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    employee_id BIGINT NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    opened_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    closed_at DATETIME NULL,
    initial_balance DECIMAL(15,2) NOT NULL DEFAULT 0,
    final_balance DECIMAL(15,2) NULL,
    status ENUM('active', 'inactive') DEFAULT 'active',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_cash_shifts_employee
        FOREIGN KEY (employee_id) REFERENCES employees(id)
);
```

### Evidencia en DBeaver

![Crear cash_shifts en MySQL](./evidencias_bitacora/scripts-mysql/image-6.png)

---

## 7. Creación de la tabla Orders

La tabla `orders` registra los pedidos atendidos en caja o para llevar, vinculados al cliente y al turno de caja activo.

### Código SQL

```sql
CREATE TABLE orders (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    customer_id BIGINT NOT NULL,
    cash_shift_id BIGINT NOT NULL,
    channel VARCHAR(50) NOT NULL,
    order_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    subtotal DECIMAL(15,2) NOT NULL,
    total DECIMAL(15,2) NOT NULL,
    status ENUM('active', 'inactive') DEFAULT 'active',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_orders_customer
        FOREIGN KEY (customer_id) REFERENCES customers(id),
    CONSTRAINT fk_orders_cash_shift
        FOREIGN KEY (cash_shift_id) REFERENCES cash_shifts(id)
);
```

### Evidencia en DBeaver

![Crear orders en MySQL](./evidencias_bitacora/scripts-mysql/image-7.png)

---

## 8. Creación de la tabla OrderDetails

La tabla `order_details` contiene cada ítem del pedido, cantidad, precio, valor total y notas/variantes (leche deslactosada, sin azúcar, etc.).

### Código SQL

```sql
CREATE TABLE order_details (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    order_id BIGINT NOT NULL,
    product_id BIGINT NOT NULL,
    quantity DECIMAL(15,3) NOT NULL,
    unit_price DECIMAL(15,2) NOT NULL,
    total DECIMAL(15,2) NOT NULL,
    observations TEXT,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_order_details_order
        FOREIGN KEY (order_id) REFERENCES orders(id),
    CONSTRAINT fk_order_details_product
        FOREIGN KEY (product_id) REFERENCES products(id)
);
```

### Evidencia en DBeaver

![Crear order_details en MySQL](./evidencias_bitacora/scripts-mysql/image-8.png)

---

## 9. Creación de la tabla Payments

La tabla `payments` gestiona los pagos realizados sobre los pedidos (efectivo, tarjeta, transferencia).

### Código SQL

```sql
CREATE TABLE payments (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    reference_type VARCHAR(50) NOT NULL,
    reference_id BIGINT NOT NULL,
    method VARCHAR(50) NOT NULL,
    amount DECIMAL(15,2) NOT NULL,
    payment_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status ENUM('active', 'inactive') DEFAULT 'active',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### Evidencia en DBeaver

![Crear payments en MySQL](./evidencias_bitacora/scripts-mysql/image-9.png)

---

## 10. Creación de la tabla PointMovements

La tabla `point_movements` almacena el historial auditable de acumulación o redención de puntos del cliente asociado a sus pedidos pagados.

### Código SQL

```sql
CREATE TABLE point_movements (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    customer_id BIGINT NOT NULL,
    order_id BIGINT NULL,
    reference_type VARCHAR(50) NOT NULL,
    reference_id BIGINT NOT NULL,
    movement_type VARCHAR(50) NOT NULL,
    points INT NOT NULL,
    movement_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    observations TEXT,
    status ENUM('active', 'inactive') DEFAULT 'active',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_point_movements_customer
        FOREIGN KEY (customer_id) REFERENCES customers(id),
    CONSTRAINT fk_point_movements_order
        FOREIGN KEY (order_id) REFERENCES orders(id)
);
```

### Evidencia en DBeaver

![Crear point_movements en MySQL](./evidencias_bitacora/scripts-mysql/image-10.png)

---

## 📐 Diagrama de la base de datos en MySQL

Una vez creadas todas las tablas y establecidas las relaciones correspondientes, se procede a visualizar el diagrama de la base de datos en DBeaver.

### Evidencia en DBeaver

![Diagrama MySQL TazaNorte](./evidencias_bitacora/scripts-mysql/image-11.png)


---

# 2. Creación de la base de datos de forma visual por MySQL Workbench

## 2.1 Creación de la base de datos tazanorte_visual

![Schema tazanorte_visual creado](./evidencias_bitacora/workbench/01_schema_tazanorte_visual.png)

**Resultado:** Se creó el schema `tazanorte_visual` dentro del EER Model de MySQL Workbench, como destino separado del `TazaNorte` ya evaluado en la Sección 1, para no sobrescribir esa evidencia y conservar ambos métodos de aprovisionamiento independientes.

---

## 2.2 Creación de la tabla customers

### Columnas de customers configuradas en el editor
![Columnas customers configuradas](./evidencias_bitacora/workbench/02_editor_customers.png)

### Script SQL generado por el modelo:
![Script CREATE TABLE customers generado](./evidencias_bitacora/workbench/02_script_customers.png)

### Evidencia de la creación (Forward Engineer):
![SHOW TABLES tras crear customers](./evidencias_bitacora/workbench/02_show_tables_customers.png)

**Resultado:** Se configuraron las columnas `id` (PK, AI, BIGINT), `document_type` (VARCHAR 30), `document_number` (VARCHAR 50, UQ), `name` (VARCHAR 150), `phone` (VARCHAR 30), `email` (VARCHAR 150), `status` (ENUM 'active','inactive', DEFAULT 'active'), `created_at` y `updated_at`, replicando exactamente la definición de la Sección 1. Se ejecutó el Forward Engineer individual y `SHOW TABLES` confirma la primera tabla creada.

---

## 2.3 Creación de la tabla employees

### Columnas de employees configuradas en el editor
![Columnas employees configuradas](./evidencias_bitacora/workbench/03_editor_employees.png)

### Script SQL generado por el modelo:
![Script CREATE TABLE employees generado](./evidencias_bitacora/workbench/03_script_employees.png)

### Evidencia de la creación (Forward Engineer):
![SHOW TABLES tras crear employees](./evidencias_bitacora/workbench/03_show_tables_employees.png)

**Resultado:** Se cargaron las columnas `id` (PK, AI), `name`, `description`, `status`, `created_at` y `updated_at`. Se ejecutó el Forward Engineer individual para esta tabla, y `SHOW TABLES` sobre `tazanorte_visual` confirma dos tablas creadas (`customers`, `employees`).

---

## 2.4 Creación de la tabla supplies

### Columnas de supplies configuradas en el editor
![Columnas supplies configuradas](./evidencias_bitacora/workbench/04_editor_supplies.png)

### Script SQL generado por el modelo:
![Script CREATE TABLE supplies generado](./evidencias_bitacora/workbench/04_script_supplies.png)

### Evidencia de la creación (Forward Engineer):
![SHOW TABLES tras crear supplies](./evidencias_bitacora/workbench/04_show_tables_supplies.png)

**Resultado:** Se configuraron `id` (PK, AI), `code` (VARCHAR 50, UQ), `name`, `unit_of_measure`, `min_stock` (DECIMAL 15,3, DEFAULT 0), `status`, `created_at` y `updated_at`. `SHOW TABLES` confirma tres tablas creadas (`customers`, `employees`, `supplies`).

---

## 2.5 Creación de la tabla products

### Columnas de products configuradas en el editor
![Columnas products configuradas](./evidencias_bitacora/workbench/05_editor_products.png)

### Script SQL generado por el modelo:
![Script CREATE TABLE products generado](./evidencias_bitacora/workbench/05_script_products.png)

### Evidencia de la creación (Forward Engineer):
![SHOW TABLES tras crear products](./evidencias_bitacora/workbench/05_show_tables_products.png)

**Resultado:** Se configuraron `id` (PK, AI), `sku` (VARCHAR 100, UQ), `name`, `description`, `price` (DECIMAL 15,2), `status`, `created_at` y `updated_at`. `SHOW TABLES` confirma cuatro tablas creadas en `tazanorte_visual`.

---

## 2.6 Creación de la tabla recipe_supplies

### Columnas de recipe_supplies configuradas en el editor
![Columnas recipe_supplies configuradas](./evidencias_bitacora/workbench/06_editor_recipe_supplies.png)

### Script SQL generado por el modelo:
![Script CREATE TABLE recipe_supplies generado](./evidencias_bitacora/workbench/06_script_recipe_supplies.png)

### Evidencia de la creación (Forward Engineer):
![SHOW TABLES tras crear recipe_supplies](./evidencias_bitacora/workbench/06_show_tables_recipe_supplies.png)

**Resultado:** Se cargaron las columnas y se configuraron las dos Foreign Keys (`product_id → products(id)` y `supply_id → supplies(id)`), además de la restricción de unicidad compuesta `uq_product_supply(product_id, supply_id)`. Se ejecutó el Forward Engineer individual y `SHOW TABLES` confirma cinco tablas creadas.

---

## 2.7 Creación de la tabla cash_shifts

### Columnas de cash_shifts configuradas en el editor
![Columnas cash_shifts configuradas](./evidencias_bitacora/workbench/07_editor_cash_shifts.png)

### Script SQL generado por el modelo:
![Script CREATE TABLE cash_shifts generado](./evidencias_bitacora/workbench/07_script_cash_shifts.png)

### Evidencia de la creación (Forward Engineer):
![SHOW TABLES tras crear cash_shifts](./evidencias_bitacora/workbench/07_show_tables_cash_shifts.png)

**Resultado:** Se configuraron las columnas y la Foreign Key `employee_id → employees(id)`, visible como conector en el diagrama EER. `SHOW TABLES` confirma seis tablas creadas hasta el momento.

---

## 2.8 Creación de la tabla orders

### Columnas de orders configuradas en el editor
![Columnas orders configuradas](./evidencias_bitacora/workbench/08_editor_orders.png)

### Script SQL generado por el modelo:
![Script CREATE TABLE orders generado](./evidencias_bitacora/workbench/08_script_orders.png)

### Evidencia de la creación (Forward Engineer):
![SHOW TABLES tras crear orders](./evidencias_bitacora/workbench/08_show_tables_orders.png)

**Resultado:** Se cargaron las columnas y las dos Foreign Keys requeridas: `customer_id → customers(id)` y `cash_shift_id → cash_shifts(id)`. Se ejecutó el Forward Engineer individual y `SHOW TABLES` confirma siete tablas creadas.

---

## 2.9 Creación de la tabla order_details

### Columnas de order_details configuradas en el editor
![Columnas order_details configuradas](./evidencias_bitacora/workbench/09_editor_order_details.png)

### Script SQL generado por el modelo:
![Script CREATE TABLE order_details generado](./evidencias_bitacora/workbench/09_script_order_details.png)

### Evidencia de la creación (Forward Engineer):
![SHOW TABLES tras crear order_details](./evidencias_bitacora/workbench/09_show_tables_order_details.png)

**Resultado:** Se cargaron las columnas y las dos Foreign Keys indispensables para la relación maestro-detalle: `order_id → orders(id)` e `product_id → products(id)`. `SHOW TABLES` confirma ocho tablas creadas.

---

## 2.10 Creación de la tabla payments

### Columnas de payments configuradas en el editor
![Columnas payments configuradas](./evidencias_bitacora/workbench/10_editor_payments.png)

### Script SQL generado por el modelo:
![Script CREATE TABLE payments generado](./evidencias_bitacora/workbench/10_script_payments.png)

### Evidencia de la creación (Forward Engineer):
![SHOW TABLES tras crear payments](./evidencias_bitacora/workbench/10_show_tables_payments.png)

**Resultado:** Se configuraron las columnas sin Foreign Key rígida dado que `reference_id` es de naturaleza polimórfica (puede referenciar a pedidos u otros conceptos según `reference_type`), idéntico al modelo de la Sección 1. `SHOW TABLES` confirma nueve tablas creadas.

---

## 2.11 Creación de la tabla point_movements

### Columnas de point_movements configuradas en el editor
![Columnas point_movements configuradas](./evidencias_bitacora/workbench/11_editor_point_movements.png)

### Script SQL generado por el modelo:
![Script CREATE TABLE point_movements generado](./evidencias_bitacora/workbench/11_script_point_movements.png)

### Evidencia de la creación (Forward Engineer):
![SHOW TABLES tras crear point_movements](./evidencias_bitacora/workbench/11_show_tables_point_movements.png)

**Resultado:** Se cargaron las columnas y las dos Foreign Keys: `customer_id → customers(id)` (obligatoria) y `order_id → orders(id)` (nullable, para movimientos manuales de fidelización o promocionales). Se ejecutó el Forward Engineer individual y `SHOW TABLES` confirma las diez tablas creadas.

---

### Verificación final de las 10 tablas en MySQL:
![SHOW TABLES final sobre tazanorte_visual](./evidencias_bitacora/workbench/12_show_tables_final.png)

### Conclusión de la Sección 2
Con esto se finaliza con éxito la creación y modelado de la base de datos `tazanorte_visual` en MySQL Workbench, habiendo modelado individualmente cada una de las 10 tablas del dominio, configurado sus respectivas columnas y tipos de datos, establecido las relaciones foráneas (Foreign Keys) de negocio y receta, y validado su persistencia efectiva en el motor MySQL tabla a tabla mediante *Forward Engineer* individual, verificado mediante `SHOW TABLES` con las 10 tablas completas creadas en el schema visual.

---

# 3. Base de Datos en PostgreSQL

## 3.1 Limpieza de tablas existentes

Para asegurar una ejecución limpia y reproducible, se eliminan las tablas en el orden inverso estricto de sus dependencias por claves foráneas:

```sql
DROP TABLE IF EXISTS point_movements;
DROP TABLE IF EXISTS payments;
DROP TABLE IF EXISTS order_details;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS cash_shifts;
DROP TABLE IF EXISTS recipe_supplies;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS supplies;
DROP TABLE IF EXISTS employees;
DROP TABLE IF EXISTS customers;
```

### Evidencia:
![Tablas eliminadas correctamente en PostgreSQL](./evidencias_bitacora/scripts-postgres/01_tablas_eliminadas.png)

**Resultado:** Se ejecutó el bloque completo de eliminación en PostgreSQL. Todas las tablas existentes quedaron removidas limpiamente sin errores de integridad referencial.

---

## 3.2 Función actualizar_updated_at

En PostgreSQL no existe la cláusula nativa `ON UPDATE CURRENT_TIMESTAMP` de MySQL. Por ello, se implementa una función disparadora (Trigger Function) reutilizable en lenguaje `plpgsql`:

```sql
CREATE OR REPLACE FUNCTION actualizar_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = CURRENT_TIMESTAMP;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

**Resultado:** Se creó la función `actualizar_updated_at()` que se acoplará mediante triggers `BEFORE UPDATE` a cada una de las tablas del dominio para automatizar el sello de fecha de última actualización.

---

## 3.3 Creación de las tablas en PostgreSQL

### 3.3.1 Creación de la tabla customers

```sql
CREATE TABLE customers (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    document_type VARCHAR(30) NOT NULL,
    document_number VARCHAR(50) NOT NULL UNIQUE,
    name VARCHAR(150) NOT NULL,
    phone VARCHAR(30),
    email VARCHAR(150),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TRIGGER trg_customers_updated_at
BEFORE UPDATE ON customers
FOR EACH ROW
EXECUTE FUNCTION actualizar_updated_at();
```

### Evidencia:
![Crear customers en PostgreSQL](./evidencias_bitacora/scripts-postgres/image-1.png)

---

### 3.3.2 Creación de la tabla employees

```sql
CREATE TABLE employees (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    description TEXT,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TRIGGER trg_employees_updated_at
BEFORE UPDATE ON employees
FOR EACH ROW
EXECUTE FUNCTION actualizar_updated_at();
```

### Evidencia:
![Crear employees en PostgreSQL](./evidencias_bitacora/scripts-postgres/image-2.png)

---

### 3.3.3 Creación de la tabla supplies

```sql
CREATE TABLE supplies (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    code VARCHAR(50) NOT NULL UNIQUE,
    name VARCHAR(150) NOT NULL,
    unit_of_measure VARCHAR(30) NOT NULL,
    min_stock NUMERIC(15,3) NOT NULL DEFAULT 0,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TRIGGER trg_supplies_updated_at
BEFORE UPDATE ON supplies
FOR EACH ROW
EXECUTE FUNCTION actualizar_updated_at();
```

### Evidencia:
![Crear supplies en PostgreSQL](./evidencias_bitacora/scripts-postgres/image-3.png)

---

### 3.3.4 Creación de la tabla products

```sql
CREATE TABLE products (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    sku VARCHAR(100) NOT NULL UNIQUE,
    name VARCHAR(150) NOT NULL,
    description TEXT,
    price NUMERIC(15,2) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TRIGGER trg_products_updated_at
BEFORE UPDATE ON products
FOR EACH ROW
EXECUTE FUNCTION actualizar_updated_at();
```

### Evidencia:
![Crear products en PostgreSQL](./evidencias_bitacora/scripts-postgres/image-4.png)

---

### 3.3.5 Creación de la tabla recipe_supplies

```sql
CREATE TABLE recipe_supplies (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    product_id BIGINT NOT NULL,
    supply_id BIGINT NOT NULL,
    quantity NUMERIC(15,3) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_recipe_supplies_product
        FOREIGN KEY (product_id) REFERENCES products(id),
    CONSTRAINT fk_recipe_supplies_supply
        FOREIGN KEY (supply_id) REFERENCES supplies(id),
    CONSTRAINT uq_pg_product_supply UNIQUE (product_id, supply_id)
);

CREATE TRIGGER trg_recipe_supplies_updated_at
BEFORE UPDATE ON recipe_supplies
FOR EACH ROW
EXECUTE FUNCTION actualizar_updated_at();
```

### Evidencia:
![Crear recipe_supplies en PostgreSQL](./evidencias_bitacora/scripts-postgres/image-5.png)

---

### 3.3.6 Creación de la tabla cash_shifts

```sql
CREATE TABLE cash_shifts (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    employee_id BIGINT NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    opened_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    closed_at TIMESTAMP NULL,
    initial_balance NUMERIC(15,2) NOT NULL DEFAULT 0,
    final_balance NUMERIC(15,2) NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_cash_shifts_employee
        FOREIGN KEY (employee_id) REFERENCES employees(id)
);

CREATE TRIGGER trg_cash_shifts_updated_at
BEFORE UPDATE ON cash_shifts
FOR EACH ROW
EXECUTE FUNCTION actualizar_updated_at();
```

### Evidencia:
![Crear cash_shifts en PostgreSQL](./evidencias_bitacora/scripts-postgres/image-6.png)

---

### 3.3.7 Creación de la tabla orders

```sql
CREATE TABLE orders (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    customer_id BIGINT NOT NULL,
    cash_shift_id BIGINT NOT NULL,
    channel VARCHAR(50) NOT NULL,
    order_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    subtotal NUMERIC(15,2) NOT NULL,
    total NUMERIC(15,2) NOT NULL,
    status VARCHAR(30) NOT NULL DEFAULT 'active',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_orders_customer
        FOREIGN KEY (customer_id) REFERENCES customers(id),
    CONSTRAINT fk_orders_cash_shift
        FOREIGN KEY (cash_shift_id) REFERENCES cash_shifts(id)
);

CREATE TRIGGER trg_orders_updated_at
BEFORE UPDATE ON orders
FOR EACH ROW
EXECUTE FUNCTION actualizar_updated_at();
```

### Evidencia:
![Crear orders en PostgreSQL](./evidencias_bitacora/scripts-postgres/image-7.png)

---

### 3.3.8 Creación de la tabla order_details

```sql
CREATE TABLE order_details (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    order_id BIGINT NOT NULL,
    product_id BIGINT NOT NULL,
    quantity NUMERIC(15,3) NOT NULL,
    unit_price NUMERIC(15,2) NOT NULL,
    total NUMERIC(15,2) NOT NULL,
    observations TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_order_details_order
        FOREIGN KEY (order_id) REFERENCES orders(id),
    CONSTRAINT fk_order_details_product
        FOREIGN KEY (product_id) REFERENCES products(id)
);

CREATE TRIGGER trg_order_details_updated_at
BEFORE UPDATE ON order_details
FOR EACH ROW
EXECUTE FUNCTION actualizar_updated_at();
```

### Evidencia:
![Crear order_details en PostgreSQL](./evidencias_bitacora/scripts-postgres/image-8.png)

---

### 3.3.9 Creación de la tabla payments

```sql
CREATE TABLE payments (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    reference_type VARCHAR(50) NOT NULL,
    reference_id BIGINT NOT NULL,
    method VARCHAR(50) NOT NULL,
    amount NUMERIC(15,2) NOT NULL,
    payment_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(30) NOT NULL DEFAULT 'active',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TRIGGER trg_payments_updated_at
BEFORE UPDATE ON payments
FOR EACH ROW
EXECUTE FUNCTION actualizar_updated_at();
```

### Evidencia:
![Crear payments en PostgreSQL](./evidencias_bitacora/scripts-postgres/image-9.png)

---

### 3.3.10 Creación de la tabla point_movements

```sql
CREATE TABLE point_movements (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    customer_id BIGINT NOT NULL,
    order_id BIGINT NULL,
    reference_type VARCHAR(50) NOT NULL,
    reference_id BIGINT NOT NULL,
    movement_type VARCHAR(50) NOT NULL,
    points INT NOT NULL,
    movement_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    observations TEXT,
    status VARCHAR(30) NOT NULL DEFAULT 'active',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_point_movements_customer
        FOREIGN KEY (customer_id) REFERENCES customers(id),
    CONSTRAINT fk_point_movements_order
        FOREIGN KEY (order_id) REFERENCES orders(id)
);

CREATE TRIGGER trg_point_movements_updated_at
BEFORE UPDATE ON point_movements
FOR EACH ROW
EXECUTE FUNCTION actualizar_updated_at();
```

### Evidencia:
![Crear point_movements en PostgreSQL](./evidencias_bitacora/scripts-postgres/image-10.png)

---

### 3.3.11 Diagrama de la base de datos en PostgreSQL

![Diagrama PostgreSQL TazaNorte](./evidencias_bitacora/scripts-postgres/image-11.png)
