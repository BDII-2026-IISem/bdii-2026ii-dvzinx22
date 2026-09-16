# Creación de Base de Datos - TazaNorte

## Apertura de las bases de datos en terminal

Para la apertura de las bases de datos en cada motor, se accedió a los motores de bases de datos por medio de la terminal de Ubuntu con las credenciales definidas previamente y se ejecutaron los siguientes comandos:

### MySQL

```sql
CREATE DATABASE TazaNorte;
```

### PostgreSQL

```postgres
CREATE DATABASE tazanorte;
```

### MSSQL Server

```sql
CREATE DATABASE tazanorte;

GO
```

### Oracle

```sql
-- En Oracle se crea y utiliza el esquema / usuario correspondiente:
CREATE USER tazanorte IDENTIFIED BY "TazaNorte2026*";
GRANT CONNECT, RESOURCE, DBA TO tazanorte;
ALTER USER tazanorte QUOTA UNLIMITED ON USERS;
```

### Ejecución

![Apertura de las bases de datos](./evidencias/creacion%20de%20base%20de%20datos.png)

### Evidencia

![Bases de datos abiertas](./evidencias/bds_creadas.png)

---

## Anotaciones

Para la creación de las bases de datos se establecieron las siguientes convenciones:

- Las entidades se representan como objetos utilizando **mayúscula inicial y singular**, por ejemplo: `Customer`, `Product`, `Order` y `CashShift`.
- Las tablas se representan utilizando **minúsculas y plural**, por ejemplo: `customers`, `products`, `orders` y `cash_shifts`.
- Los nombres de las tablas y sus atributos se encuentran en **inglés**.
- Los atributos utilizan la nomenclatura **snake_case**, por ejemplo: `created_at`, `document_number` y `unit_of_measure`.
- La llave primaria de todas las tablas se denomina `id`.
- Los identificadores que pueden almacenar una gran cantidad de registros utilizan el tipo `BIGINT` (o su equivalente en cada motor).
- Las claves foráneas utilizan el nombre de la tabla relacionada en singular seguido de `_id`, por ejemplo: `customer_id`, `product_id`, `employee_id`.
- Los campos `created_at` y `updated_at` se utilizan para registrar la fecha de creación y última actualización de los registros.
- Los campos que deben ser únicos se identifican mediante la restricción `UNIQUE`.
- Al finalizar la creación de las tablas se debe generar y visualizar el diagrama de la base de datos.

---

# Tablas

**TazaNorte** es un sistema de gestión para cafeterías y puntos de venta enfocado en pedidos en caja y para llevar, preparación de bebidas configurables, control de insumos críticos, gestión de turnos de caja y un programa de fidelización por puntos. La plataforma permite administrar clientes, empleados, insumos, recetas, turnos de caja, pedidos, detalles de pedido, pagos y movimientos de puntos (acumulación y redención auditables).

Sus entidades y tablas son:

| Entidad | Tabla | Atributos / claves sugeridos |
|---|---|---|
| Customer | `customers` | `id`, `document_type`, `document_number (UQ)`, `name`, `phone`, `email`, `status / is_active`, `created_at`, `updated_at` |
| Employee | `employees` | `id`, `name`, `description`, `status / is_active`, `created_at`, `updated_at` |
| Supply | `supplies` | `id`, `code (UQ)`, `name`, `unit_of_measure`, `min_stock`, `status / is_active`, `created_at`, `updated_at` |
| Product | `products` | `id`, `sku (UQ)`, `name`, `description`, `price`, `status / is_active`, `created_at`, `updated_at` |
| RecipeSupply | `recipe_supplies` | `id`, `product_id (FK)`, `supply_id (FK)`, `quantity`, `status / is_active`, `created_at`, `updated_at` |
| CashShift | `cash_shifts` | `id`, `employee_id (FK)`, `name`, `description`, `opened_at`, `closed_at`, `initial_balance`, `final_balance`, `status`, `created_at`, `updated_at` |
| Order | `orders` | `id`, `customer_id (FK)`, `cash_shift_id (FK)`, `channel`, `order_date`, `subtotal`, `total`, `status`, `created_at`, `updated_at` |
| OrderDetail | `order_details` | `id`, `order_id (FK)`, `product_id (FK)`, `quantity`, `unit_price`, `total`, `observations`, `created_at`, `updated_at` |
| Payment | `payments` | `id`, `reference_type`, `reference_id`, `method`, `amount`, `payment_date`, `status`, `created_at`, `updated_at` |
| PointMovement | `point_movements` | `id`, `customer_id (FK)`, `order_id (FK)`, `reference_type`, `reference_id`, `movement_type`, `points`, `movement_date`, `observations`, `status`, `created_at`, `updated_at` |

---

# Base de datos en MySQL - Scripts DBeaver

## 1. Creación de la tabla Customers

La tabla `customers` almacena la información de los clientes registrados en la cafetería para su identificación y acumulación de puntos.

### Código

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

### Evidencia

![Crear customers en MySQL](./evidencias/scripts-mysql/image-1.png)

---

## 2. Creación de la tabla Employees

La tabla `employees` almacena los datos de los baristas, cajeros y supervisores encargados de los turnos y pedidos.

### Código

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

### Evidencia

![Crear employees en MySQL](./evidencias/scripts-mysql/image-2.png)

---

## 3. Creación de la tabla Supplies

La tabla `supplies` (Insumos) almacena los ingredientes base (café en grano, leche, jarabes, vasos) y su stock mínimo.

### Código

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

### Evidencia

![Crear supplies en MySQL](./evidencias/scripts-mysql/image-3.png)

---

## 4. Creación de la tabla Products

La tabla `products` contiene el catálogo de bebidas y alimentos disponibles en la cafetería.

### Código

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

### Evidencia

![Crear products en MySQL](./evidencias/scripts-mysql/image-4.png)

---

## 5. Creación de la tabla RecipeSupplies

La tabla `recipe_supplies` materializa la relación N:M entre `products` e `supplies`, definiendo qué insumos y en qué cantidad componen cada producto.

### Código

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

### Evidencia

![Crear recipe_supplies en MySQL](./evidencias/scripts-mysql/image-5.png)

---

## 6. Creación de la tabla CashShifts

La tabla `cash_shifts` administra la apertura, control y cierre de turnos de caja asignados a cada empleado.

### Código

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

### Evidencia

![Crear cash_shifts en MySQL](./evidencias/scripts-mysql/image-6.png)

---

## 7. Creación de la tabla Orders

La tabla `orders` registra los pedidos atendidos en caja o para llevar, vinculados al cliente y al turno de caja activo.

### Código

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

### Evidencia

![Crear orders en MySQL](./evidencias/scripts-mysql/image-7.png)

---

## 8. Creación de la tabla OrderDetails

La tabla `order_details` contiene cada ítem del pedido, cantidad, precio, valor total y notas/variantes (leche deslactosada, sin azúcar, etc.).

### Código

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

### Evidencia

![Crear order_details en MySQL](./evidencias/scripts-mysql/image-8.png)

---

## 9. Creación de la tabla Payments

La tabla `payments` gestiona los pagos realizados sobre los pedidos (efectivo, tarjeta, transferencia).

### Código

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

### Evidencia

![Crear payments en MySQL](./evidencias/scripts-mysql/image-9.png)

---

## 10. Creación de la tabla PointMovements

La tabla `point_movements` almacena el historial auditable de acumulación o redención de puntos del cliente asociado a sus pedidos pagados.

### Código

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

### Evidencia

![Crear point_movements en MySQL](./evidencias/scripts-mysql/image-10.png)

---

## Diagrama de la base de datos en MySQL

Una vez creadas todas las tablas y establecidas las relaciones correspondientes, se procede a visualizar el diagrama de la base de datos en DBeaver.

### Evidencia

![Diagrama MySQL TazaNorte](./evidencias/scripts-mysql/image-11.png)

---

# Base de datos en PostgreSQL - Terminal DBeaver

Para la implementación de la base de datos TazaNorte en PostgreSQL se utilizó DBeaver como herramienta de administración. Se mantuvo la misma estructura lógica, adaptando los tipos de datos correspondientes a PostgreSQL (`GENERATED ALWAYS AS IDENTITY`, `NUMERIC`, `TIMESTAMP`, `BOOLEAN`).

## 1. Creación de la tabla Customers

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
```

### Evidencia

![Crear customers en PostgreSQL](./evidencias/scripts-postgres/image-1.png)

---

## 2. Creación de la tabla Employees

```sql
CREATE TABLE employees (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    description TEXT,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

### Evidencia

![Crear employees en PostgreSQL](./evidencias/scripts-postgres/image-2.png)

---

## 3. Creación de la tabla Supplies

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
```

### Evidencia

![Crear supplies en PostgreSQL](./evidencias/scripts-postgres/image-3.png)

---

## 4. Creación de la tabla Products

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
```

### Evidencia

![Crear products en PostgreSQL](./evidencias/scripts-postgres/image-4.png)

---

## 5. Creación de la tabla RecipeSupplies

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
```

### Evidencia

![Crear recipe_supplies en PostgreSQL](./evidencias/scripts-postgres/image-5.png)

---

## 6. Creación de la tabla CashShifts

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
```

### Evidencia

![Crear cash_shifts en PostgreSQL](./evidencias/scripts-postgres/image-6.png)

---

## 7. Creación de la tabla Orders

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
```

### Evidencia

![Crear orders en PostgreSQL](./evidencias/scripts-postgres/image-7.png)

---

## 8. Creación de la tabla OrderDetails

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
```

### Evidencia

![Crear order_details en PostgreSQL](./evidencias/scripts-postgres/image-8.png)

---

## 9. Creación de la tabla Payments

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
```

### Evidencia

![Crear payments en PostgreSQL](./evidencias/scripts-postgres/image-9.png)

---

## 10. Creación de la tabla PointMovements

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
```

### Evidencia

![Crear point_movements en PostgreSQL](./evidencias/scripts-postgres/image-10.png)

---

## Diagrama de la base de datos en PostgreSQL

### Evidencia

![Diagrama PostgreSQL TazaNorte](./evidencias/scripts-postgres/image-11.png)

---

# Consideraciones de PostgreSQL

Durante la implementación de TazaNorte en PostgreSQL se realizaron las siguientes adaptaciones respecto a MySQL:

| MySQL | PostgreSQL |
|---|---|
| `BIGINT AUTO_INCREMENT` | `BIGINT GENERATED ALWAYS AS IDENTITY` |
| `DECIMAL(15,2)` | `NUMERIC(15,2)` |
| `DATETIME` | `TIMESTAMP` |
| `ENUM('active','inactive')` | `BOOLEAN` o `VARCHAR(30)` |
| `DEFAULT CURRENT_TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP` |
| `ON UPDATE CURRENT_TIMESTAMP` | No existe de forma nativa (requiere trigger para auto-actualizar) |

---

# Base de datos en MSSQL Server - Terminal DBeaver

Para la implementación de TazaNorte en MSSQL Server se adaptaron los tipos a `IDENTITY(1,1)`, `DECIMAL`, `VARCHAR(MAX)`, `DATETIME` y restricciones `CHECK` para campos de estado.

## 1. Creación de la tabla Customers

```sql
CREATE TABLE customers (
    id BIGINT IDENTITY(1,1) PRIMARY KEY,
    document_type VARCHAR(30) NOT NULL,
    document_number VARCHAR(50) NOT NULL UNIQUE,
    name VARCHAR(150) NOT NULL,
    phone VARCHAR(30),
    email VARCHAR(150),
    status VARCHAR(10) NOT NULL DEFAULT 'active',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_customers_status CHECK (status IN ('active', 'inactive'))
);
```

### Evidencia

![Crear customers en MSSQL Server](./evidencias/scripts-mssql/image-1.png)

---

## 2. Creación de la tabla Employees

```sql
CREATE TABLE employees (
    id BIGINT IDENTITY(1,1) PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    description VARCHAR(MAX),
    status VARCHAR(10) NOT NULL DEFAULT 'active',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_employees_status CHECK (status IN ('active', 'inactive'))
);
```

### Evidencia

![Crear employees en MSSQL Server](./evidencias/scripts-mssql/image-2.png)

---

## 3. Creación de la tabla Supplies

```sql
CREATE TABLE supplies (
    id BIGINT IDENTITY(1,1) PRIMARY KEY,
    code VARCHAR(50) NOT NULL UNIQUE,
    name VARCHAR(150) NOT NULL,
    unit_of_measure VARCHAR(30) NOT NULL,
    min_stock DECIMAL(15,3) NOT NULL DEFAULT 0,
    status VARCHAR(10) NOT NULL DEFAULT 'active',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_supplies_status CHECK (status IN ('active', 'inactive'))
);
```

### Evidencia

![Crear supplies en MSSQL Server](./evidencias/scripts-mssql/image-3.png)

---

## 4. Creación de la tabla Products

```sql
CREATE TABLE products (
    id BIGINT IDENTITY(1,1) PRIMARY KEY,
    sku VARCHAR(100) NOT NULL UNIQUE,
    name VARCHAR(150) NOT NULL,
    description VARCHAR(MAX),
    price DECIMAL(15,2) NOT NULL,
    status VARCHAR(10) NOT NULL DEFAULT 'active',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_products_status CHECK (status IN ('active', 'inactive'))
);
```

### Evidencia

![Crear products en MSSQL Server](./evidencias/scripts-mssql/image-4.png)

---

## 5. Creación de la tabla RecipeSupplies

```sql
CREATE TABLE recipe_supplies (
    id BIGINT IDENTITY(1,1) PRIMARY KEY,
    product_id BIGINT NOT NULL,
    supply_id BIGINT NOT NULL,
    quantity DECIMAL(15,3) NOT NULL,
    status VARCHAR(10) NOT NULL DEFAULT 'active',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_mssql_recipe_product FOREIGN KEY (product_id) REFERENCES products(id),
    CONSTRAINT fk_mssql_recipe_supply FOREIGN KEY (supply_id) REFERENCES supplies(id),
    CONSTRAINT uq_mssql_product_supply UNIQUE (product_id, supply_id),
    CONSTRAINT chk_recipe_supplies_status CHECK (status IN ('active', 'inactive'))
);
```

### Evidencia

![Crear recipe_supplies en MSSQL Server](./evidencias/scripts-mssql/image-5.png)

---

## 6. Creación de la tabla CashShifts

```sql
CREATE TABLE cash_shifts (
    id BIGINT IDENTITY(1,1) PRIMARY KEY,
    employee_id BIGINT NOT NULL,
    name VARCHAR(100) NOT NULL,
    description VARCHAR(MAX),
    opened_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    closed_at DATETIME NULL,
    initial_balance DECIMAL(15,2) NOT NULL DEFAULT 0,
    final_balance DECIMAL(15,2) NULL,
    status VARCHAR(10) NOT NULL DEFAULT 'active',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_mssql_cash_shifts_employee FOREIGN KEY (employee_id) REFERENCES employees(id),
    CONSTRAINT chk_cash_shifts_status CHECK (status IN ('active', 'inactive'))
);
```

### Evidencia

![Crear cash_shifts en MSSQL Server](./evidencias/scripts-mssql/image-6.png)

---

## 7. Creación de la tabla Orders

```sql
CREATE TABLE orders (
    id BIGINT IDENTITY(1,1) PRIMARY KEY,
    customer_id BIGINT NOT NULL,
    cash_shift_id BIGINT NOT NULL,
    channel VARCHAR(50) NOT NULL,
    order_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    subtotal DECIMAL(15,2) NOT NULL,
    total DECIMAL(15,2) NOT NULL,
    status VARCHAR(10) NOT NULL DEFAULT 'active',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_mssql_orders_customer FOREIGN KEY (customer_id) REFERENCES customers(id),
    CONSTRAINT fk_mssql_orders_cash_shift FOREIGN KEY (cash_shift_id) REFERENCES cash_shifts(id),
    CONSTRAINT chk_orders_status CHECK (status IN ('active', 'inactive'))
);
```

### Evidencia

![Crear orders en MSSQL Server](./evidencias/scripts-mssql/image-7.png)

---

## 8. Creación de la tabla OrderDetails

```sql
CREATE TABLE order_details (
    id BIGINT IDENTITY(1,1) PRIMARY KEY,
    order_id BIGINT NOT NULL,
    product_id BIGINT NOT NULL,
    quantity DECIMAL(15,3) NOT NULL,
    unit_price DECIMAL(15,2) NOT NULL,
    total DECIMAL(15,2) NOT NULL,
    observations VARCHAR(MAX),
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_mssql_order_details_order FOREIGN KEY (order_id) REFERENCES orders(id),
    CONSTRAINT fk_mssql_order_details_product FOREIGN KEY (product_id) REFERENCES products(id)
);
```

### Evidencia

![Crear order_details en MSSQL Server](./evidencias/scripts-mssql/image-8.png)

---

## 9. Creación de la tabla Payments

```sql
CREATE TABLE payments (
    id BIGINT IDENTITY(1,1) PRIMARY KEY,
    reference_type VARCHAR(50) NOT NULL,
    reference_id BIGINT NOT NULL,
    method VARCHAR(50) NOT NULL,
    amount DECIMAL(15,2) NOT NULL,
    payment_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(10) NOT NULL DEFAULT 'active',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_payments_status CHECK (status IN ('active', 'inactive'))
);
```

### Evidencia

![Crear payments en MSSQL Server](./evidencias/scripts-mssql/image-9.png)

---

## 10. Creación de la tabla PointMovements

```sql
CREATE TABLE point_movements (
    id BIGINT IDENTITY(1,1) PRIMARY KEY,
    customer_id BIGINT NOT NULL,
    order_id BIGINT NULL,
    reference_type VARCHAR(50) NOT NULL,
    reference_id BIGINT NOT NULL,
    movement_type VARCHAR(50) NOT NULL,
    points INT NOT NULL,
    movement_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    observations VARCHAR(MAX),
    status VARCHAR(10) NOT NULL DEFAULT 'active',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_mssql_point_movements_customer FOREIGN KEY (customer_id) REFERENCES customers(id),
    CONSTRAINT fk_mssql_point_movements_order FOREIGN KEY (order_id) REFERENCES orders(id),
    CONSTRAINT chk_point_movements_status CHECK (status IN ('active', 'inactive'))
);
```

### Evidencia

![Crear point_movements en MSSQL Server](./evidencias/scripts-mssql/image-10.png)

---

## Diagrama de la base de datos en MSSQL Server

### Evidencia

![Diagrama MSSQL TazaNorte](./evidencias/scripts-mssql/image-11.png)

---

# Consideraciones de MSSQL Server

Durante la implementación de TazaNorte en MSSQL Server se realizaron las siguientes adaptaciones:

| MySQL | PostgreSQL | MSSQL Server |
|---|---|---|
| `BIGINT AUTO_INCREMENT` | `BIGINT GENERATED ALWAYS AS IDENTITY` | `BIGINT IDENTITY(1,1)` |
| `DECIMAL(15,2)` | `NUMERIC(15,2)` | `DECIMAL(15,2)` |
| `DECIMAL(15,3)` | `NUMERIC(15,3)` | `DECIMAL(15,3)` |
| `DATETIME` | `TIMESTAMP` | `DATETIME` |
| `ENUM('active','inactive')` | `BOOLEAN` / `VARCHAR` | `VARCHAR(10)` + `CHECK` |
| `TEXT` | `TEXT` | `VARCHAR(MAX)` |
| `CURRENT_TIMESTAMP` | `CURRENT_TIMESTAMP` | `CURRENT_TIMESTAMP` |
| `ON UPDATE CURRENT_TIMESTAMP` | No nativo | No nativo |

---

# Base de datos en Oracle - Terminal DBeaver

Para la implementación en Oracle, se utiliza el esquema configurado con tipos de datos `NUMBER(19) GENERATED ALWAYS AS IDENTITY`, `VARCHAR2`, `CLOB` y restricciones `CHECK`.

## 1. Creación de la tabla Customers

```sql
CREATE TABLE customers (
    id NUMBER(19) GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    document_type VARCHAR2(30) NOT NULL,
    document_number VARCHAR2(50) NOT NULL UNIQUE,
    name VARCHAR2(150) NOT NULL,
    phone VARCHAR2(30),
    email VARCHAR2(150),
    status VARCHAR2(10) DEFAULT 'active' NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT chk_ora_customers_status CHECK (status IN ('active', 'inactive'))
);
```

### Evidencia

![Crear customers en Oracle](./evidencias/scripts-oracle/image-1.png)

---

## 2. Creación de la tabla Employees

```sql
CREATE TABLE employees (
    id NUMBER(19) GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR2(150) NOT NULL,
    description CLOB,
    status VARCHAR2(10) DEFAULT 'active' NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT chk_ora_employees_status CHECK (status IN ('active', 'inactive'))
);
```

### Evidencia

![Crear employees en Oracle](./evidencias/scripts-oracle/image-2.png)

---

## 3. Creación de la tabla Supplies

```sql
CREATE TABLE supplies (
    id NUMBER(19) GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    code VARCHAR2(50) NOT NULL UNIQUE,
    name VARCHAR2(150) NOT NULL,
    unit_of_measure VARCHAR2(30) NOT NULL,
    min_stock NUMBER(15,3) DEFAULT 0 NOT NULL,
    status VARCHAR2(10) DEFAULT 'active' NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT chk_ora_supplies_status CHECK (status IN ('active', 'inactive'))
);
```

### Evidencia

![Crear supplies en Oracle](./evidencias/scripts-oracle/image-3.png)

---

## 4. Creación de la tabla Products

```sql
CREATE TABLE products (
    id NUMBER(19) GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    sku VARCHAR2(100) NOT NULL UNIQUE,
    name VARCHAR2(150) NOT NULL,
    description CLOB,
    price NUMBER(15,2) NOT NULL,
    status VARCHAR2(10) DEFAULT 'active' NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT chk_ora_products_status CHECK (status IN ('active', 'inactive'))
);
```

### Evidencia

![Crear products en Oracle](./evidencias/scripts-oracle/image-4.png)

---

## 5. Creación de la tabla RecipeSupplies

```sql
CREATE TABLE recipe_supplies (
    id NUMBER(19) GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    product_id NUMBER(19) NOT NULL,
    supply_id NUMBER(19) NOT NULL,
    quantity NUMBER(15,3) NOT NULL,
    status VARCHAR2(10) DEFAULT 'active' NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT fk_ora_recipe_product FOREIGN KEY (product_id) REFERENCES products(id),
    CONSTRAINT fk_ora_recipe_supply FOREIGN KEY (supply_id) REFERENCES supplies(id),
    CONSTRAINT uq_ora_product_supply UNIQUE (product_id, supply_id),
    CONSTRAINT chk_ora_recipe_status CHECK (status IN ('active', 'inactive'))
);
```

### Evidencia

![Crear recipe_supplies en Oracle](./evidencias/scripts-oracle/image-5.png)

---

## 6. Creación de la tabla CashShifts

```sql
CREATE TABLE cash_shifts (
    id NUMBER(19) GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    employee_id NUMBER(19) NOT NULL,
    name VARCHAR2(100) NOT NULL,
    description CLOB,
    opened_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    closed_at TIMESTAMP NULL,
    initial_balance NUMBER(15,2) DEFAULT 0 NOT NULL,
    final_balance NUMBER(15,2) NULL,
    status VARCHAR2(10) DEFAULT 'active' NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT fk_ora_cash_shifts_employee FOREIGN KEY (employee_id) REFERENCES employees(id),
    CONSTRAINT chk_ora_cash_shifts_status CHECK (status IN ('active', 'inactive'))
);
```

### Evidencia

![Crear cash_shifts en Oracle](./evidencias/scripts-oracle/image-6.png)

---

## 7. Creación de la tabla Orders

```sql
CREATE TABLE orders (
    id NUMBER(19) GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    customer_id NUMBER(19) NOT NULL,
    cash_shift_id NUMBER(19) NOT NULL,
    channel VARCHAR2(50) NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    subtotal NUMBER(15,2) NOT NULL,
    total NUMBER(15,2) NOT NULL,
    status VARCHAR2(10) DEFAULT 'active' NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT fk_ora_orders_customer FOREIGN KEY (customer_id) REFERENCES customers(id),
    CONSTRAINT fk_ora_orders_cash_shift FOREIGN KEY (cash_shift_id) REFERENCES cash_shifts(id),
    CONSTRAINT chk_ora_orders_status CHECK (status IN ('active', 'inactive'))
);
```

### Evidencia

![Crear orders en Oracle](./evidencias/scripts-oracle/image-7.png)

---

## 8. Creación de la tabla OrderDetails

```sql
CREATE TABLE order_details (
    id NUMBER(19) GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    order_id NUMBER(19) NOT NULL,
    product_id NUMBER(19) NOT NULL,
    quantity NUMBER(15,3) NOT NULL,
    unit_price NUMBER(15,2) NOT NULL,
    total NUMBER(15,2) NOT NULL,
    observations CLOB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT fk_ora_order_details_order FOREIGN KEY (order_id) REFERENCES orders(id),
    CONSTRAINT fk_ora_order_details_product FOREIGN KEY (product_id) REFERENCES products(id)
);
```

### Evidencia

![Crear order_details en Oracle](./evidencias/scripts-oracle/image-8.png)

---

## 9. Creación de la tabla Payments

```sql
CREATE TABLE payments (
    id NUMBER(19) GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    reference_type VARCHAR2(50) NOT NULL,
    reference_id NUMBER(19) NOT NULL,
    method VARCHAR2(50) NOT NULL,
    amount NUMBER(15,2) NOT NULL,
    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    status VARCHAR2(10) DEFAULT 'active' NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT chk_ora_payments_status CHECK (status IN ('active', 'inactive'))
);
```

### Evidencia

![Crear payments en Oracle](./evidencias/scripts-oracle/image-9.png)

---

## 10. Creación de la tabla PointMovements

```sql
CREATE TABLE point_movements (
    id NUMBER(19) GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    customer_id NUMBER(19) NOT NULL,
    order_id NUMBER(19) NULL,
    reference_type VARCHAR2(50) NOT NULL,
    reference_id NUMBER(19) NOT NULL,
    movement_type VARCHAR2(50) NOT NULL,
    points NUMBER(10) NOT NULL,
    movement_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    observations CLOB,
    status VARCHAR2(10) DEFAULT 'active' NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT fk_ora_points_customer FOREIGN KEY (customer_id) REFERENCES customers(id),
    CONSTRAINT fk_ora_points_order FOREIGN KEY (order_id) REFERENCES orders(id),
    CONSTRAINT chk_ora_points_status CHECK (status IN ('active', 'inactive'))
);
```

### Evidencia

![Crear point_movements en Oracle](./evidencias/scripts-oracle/image-10.png)

---

## Diagrama de la base de datos en Oracle

### Evidencia

![Diagrama Oracle TazaNorte](./evidencias/scripts-oracle/image-11.png)

---

## Consideraciones de Oracle

Durante la implementación de TazaNorte en Oracle se realizaron adaptaciones respecto a los demás motores:

| MySQL | PostgreSQL | MSSQL Server | Oracle |
|---|---|---|---|
| `BIGINT AUTO_INCREMENT` | `BIGINT GENERATED ALWAYS AS IDENTITY` | `BIGINT IDENTITY(1,1)` | `NUMBER(19) GENERATED ALWAYS AS IDENTITY` |
| `DECIMAL(15,2)` | `NUMERIC(15,2)` | `DECIMAL(15,2)` | `NUMBER(15,2)` |
| `DECIMAL(15,3)` | `NUMERIC(15,3)` | `DECIMAL(15,3)` | `NUMBER(15,3)` |
| `DATETIME` | `TIMESTAMP` | `DATETIME` | `TIMESTAMP` |
| `ENUM('active','inactive')` | `BOOLEAN` / `VARCHAR` | `VARCHAR(10)` + `CHECK` | `VARCHAR2(10)` + `CHECK` |
| `TEXT` | `TEXT` | `VARCHAR(MAX)` | `CLOB` |
| `VARCHAR` | `VARCHAR` | `VARCHAR` | `VARCHAR2` |
| `CURRENT_TIMESTAMP` | `CURRENT_TIMESTAMP` | `CURRENT_TIMESTAMP` | `CURRENT_TIMESTAMP` |
| `ON UPDATE CURRENT_TIMESTAMP` | No nativo | No nativo | No nativo |

---

## Resumen de la implementación

La estructura lógica de **TazaNorte** se mantuvo equivalente en MySQL, PostgreSQL, MSSQL Server y Oracle.

Las relaciones de negocio implementadas fueron:

- `recipe_supplies.product_id` → `products.id` y `recipe_supplies.supply_id` → `supplies.id` (Relación N:M de receta de producto e insumos).
- `cash_shifts.employee_id` → `employees.id` (Relación 1:N de empleado con sus turnos de caja).
- `orders.customer_id` → `customers.id` (Relación 1:N de cliente con sus pedidos).
- `orders.cash_shift_id` → `cash_shifts.id` (Relación 1:N de turno de caja con pedidos).
- `order_details.order_id` → `orders.id` (Relación 1:N de pedido con sus detalles).
- `order_details.product_id` → `products.id` (Relación 1:N de producto con líneas de pedido).
- `point_movements.customer_id` → `customers.id` (Relación 1:N de cliente con sus movimientos de puntos).
- `point_movements.order_id` → `orders.id` (Relación 0..N de pedido con movimientos de puntos).
- `payments.reference_type` y `payments.reference_id` (Relación polimórfica para trazabilidad de pagos de pedidos).
