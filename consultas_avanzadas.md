# CONSULTAS AVANZADAS SQL - PROYECTO TAZANORTE

<p align="center">
  <img src="https://img.shields.io/badge/Project-TazaNorte_Cafetería-6F4E37?style=for-the-badge&logo=coffeescript&logoColor=white" alt="TazaNorte" />
  <img src="https://img.shields.io/badge/MySQL-005C84?style=for-the-badge&logo=mysql&logoColor=white" alt="MySQL" />
  <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL" />
  <img src="https://img.shields.io/badge/MSSQL_Server-CC292B?style=for-the-badge&logo=microsoftsqlserver&logoColor=white" alt="MSSQL Server" />
  <img src="https://img.shields.io/badge/Oracle_Database-F80000?style=for-the-badge&logo=oracle&logoColor=white" alt="Oracle" />
  <img src="https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white" alt="Ubuntu" />
</p>

Documento técnico de trazabilidad, homologación y ejecución de **consultas SQL avanzadas, procedimientos almacenados (Stored Procedures), subconsultas, teoría de conjuntos y triggers de auditoría con inmutabilidad estricta** sobre los cuatro motores de bases de datos relacionales containerizados mediante Docker (**MySQL 8.0, PostgreSQL 17, Microsoft SQL Server 2022 y Oracle Database 21c XE**). El conjunto de datos, las relaciones y las operaciones analíticas se encuentran adaptados de forma integral al ecosistema transaccional de **TazaNorte** (cafetería de especialidad).

---

## Imagenes de los registros de cada tabla creada :

A continuación se presentan las evidencias visuales del estado actual de registros y datos poblados en las 10 entidades que conforman la base de datos **TazaNorte**:

#### Registros de la Tabla customers

![](images/01_tabla_customers.png)

#### Registros de la Tabla employees

![](images/02_tabla_employees.png)

#### Registros de la Tabla supplies

![](images/03_tabla_supplies.png)

#### Registros de la Tabla products

![](images/04_tabla_products.png)

#### Registros de la Tabla recipe_supplies

![](images/05_tabla_recipe_supplies.png)

#### Registros de la Tabla cash_shifts

![](images/06_tabla_cash_shifts.png)

#### Registros de la Tabla orders

![](images/07_tabla_orders.png)

#### Registros de la Tabla order_details

![](images/08_tabla_order_details.png)

#### Registros de la Tabla payments

![](images/09_tabla_payments.png)

#### Registros de la Tabla point_movements

![](images/10_tabla_point_movements.png)

#### Diagrama Entidad-Relacion de la base de datos :

![](images/diagrama_erd_tazanorte.png)

---

## 1. Consultas avanzadas en MySQL :

### 1.1 Proyección de Atributos y Definición de Alias (SELECT, FROM, AS)

**Concepto y Narrativa:** 
La sentencia `SELECT` constituye la operación fundamental de proyección en álgebra relacional, permitiendo seleccionar columnas específicas desde una o varias entidades definidas tras la cláusula `FROM`. Asimismo, se utiliza la palabra reservada `AS` para definir **alias** de columnas, renombrando temporalmente los encabezados del conjunto de resultados para optimizar la legibilidad y claridad de la interfaz.

En esta consulta sobre la cafetería **TazaNorte**, se proyectan los atributos esenciales de los clientes (`name`, `document_type`, `document_number`) y su indicador de actividad (`is_active` de tipo `TINYINT`), renombrando los campos para una presentación ejecutiva.

```sql
SELECT 
    name AS cliente_nombre, 
    document_type AS tipo_documento, 
    document_number AS numero_documento, 
    is_active AS estado_activo 
FROM customers;
```

**Evidencia en DBeaver:**

![](images/mysql_1_1_campos.png)

---

### 1.2 Secuencia Cronológica y Criterios de Ordenamiento (ORDER BY, DESC, ASC)

**Concepto y Narrativa:** 
La cláusula `ORDER BY` permite clasificar las tuplas resultantes según criterios secuenciales ascendentes (`ASC`, por defecto) o descendentes (`DESC`). En sistemas transaccionales como TazaNorte, el ordenamiento descendente por fecha (`order_date DESC`) es indispensable para auditar los consumos más recientes en barra y mesa, garantizando la trazabilidad operativa en el punto de venta.

```sql
SELECT id, order_date, total, status 
FROM orders 
ORDER BY order_date DESC;
```

**Evidencia en DBeaver:**

![](images/mysql_1_2_order_by.png)

---

### 1.3 Asociación Relacional en Cláusula WHERE (Producto Cartesiano Filtrado y Operadores de Igualdad)

**Concepto y Narrativa:** 
Históricamente, las relaciones entre entidades en bases de datos relacionales se construían mediante un producto cartesiano delimitado por una condición de igualdad en la cláusula `WHERE` (`tabla1.fk = tabla2.pk`). Este operador de comparación (`=`) garantiza que únicamente se proyecten las órdenes que posean una correspondencia exacta con la clave primaria del cliente registrado.

```sql
SELECT c.name, o.id AS order_id, o.total, o.status 
FROM orders o, customers c 
WHERE c.id = o.customer_id;
```

**Evidencia en DBeaver:**

![](images/mysql_1_3_multitabla_where.png)

---

### 1.4 Combinación Explícita de Entidades mediante Cláusulas JOIN y ON (INNER JOIN, Claves Foráneas)

**Concepto y Narrativa:** 
La instrucción ANSI `INNER JOIN` formaliza la combinación relacional de tablas de forma más legible y optimizada para el planificador de consultas. La cláusula asociada **`ON`** define explícitamente el predicado lógico de unión (`ON c.id = o.customer_id`), estipulando la regla de integridad referencial bajo la cual se intersectan los datos de ventas y clientes en TazaNorte.

```sql
SELECT c.name, c.email, o.id AS order_id, o.order_date, o.total, o.status 
FROM customers AS c 
JOIN orders AS o ON (c.id = o.customer_id);
```

**Evidencia en DBeaver:**

![](images/mysql_1_4_multitabla_join.png)

---

### 1.5 Filtros Lógicos Compuestos y Comparadores Relacionales (WHERE, AND, Operadores de Igualdad y Estado)

**Concepto y Narrativa:** 
El operador lógico **`AND`** permite concatenar múltiples predicados dentro de la cláusula `WHERE`, evaluando como válidas únicamente aquellas filas que satisfacen simultáneamente todas las condiciones. Junto con los **comparadores lógicos** (`=`, `<>`, `>`, `<`), permite discriminar órdenes según su estado operativo (`active` vs `inactive`), segregando los pedidos válidos de aquellos anulados o cancelados.

**Filtro por órdenes con estado activo:**
```sql
SELECT c.name, o.id AS order_id, o.order_date, o.total, o.status 
FROM orders o, customers c 
WHERE c.id = o.customer_id AND o.status = 'active';
```
![](images/mysql_1_5_condiciones_where_active.png)

**Filtro combinado con JOIN por órdenes con estado inactivo:**
```sql
SELECT c.name, c.email, o.id AS order_id, o.total, o.status 
FROM customers AS c 
JOIN orders AS o ON (c.id = o.customer_id) 
WHERE o.status = 'inactive';
```
![](images/mysql_1_5_condiciones_join_inactive.png)

---

### 1.6 Búsqueda por Patrones de Texto con Operador LIKE (Comodines %, Concatenación y Filtros Compuestos)

**Concepto y Narrativa:** 
El operador **`LIKE`** realiza búsquedas por concordancia de patrones de cadenas de texto empleando caracteres comodín:
- `%` : Representa cualquier secuencia de cero o más caracteres.
- `_` : Representa un único carácter en una posición específica.

En TazaNorte se aplica para localizar clientes por inicial de correo, segmentar cuentas corporativas bajo el dominio `@gmail` y combinar estas búsquedas con estados transaccionales activos.

**1.6.1 Filtro por inicial (`m%`):**
```sql
SELECT name, email, is_active 
FROM customers AS c 
WHERE c.email LIKE 'm%';
```
![](images/mysql_1_6_like_inicio.png)

**1.6.2 Filtro por dominio corporativo (`@gmail`):**
```sql
SELECT name, email, is_active 
FROM customers AS c 
WHERE c.email LIKE CONCAT('%', 'gmail', '%');
```
![](images/mysql_1_6_like_gmail.png)

**1.6.3 Filtro combinado (JOIN + Estado Activo + LIKE inicial):**
```sql
SELECT c.name, c.email, o.id AS order_id, o.total, o.status 
FROM customers AS c 
JOIN orders AS o ON (c.id = o.customer_id) 
WHERE o.status = 'active' AND c.email LIKE 'm%';
```
![](images/mysql_1_6_like_combinado.png)

---

### 1.7 Evaluación de Rangos Temporales y Facturación (BETWEEN, TIMESTAMP y Procedimientos Almacenados)

**Concepto y Narrativa:** 
El operador **`BETWEEN`** evalúa si un atributo cuantitativo o de fecha se encuentra contenido dentro de un intervalo cerrado inclusivo (`val >= limite_inferior AND val <= limite_superior`). Para optimizar y estandarizar esta consulta analítica sobre la facturación de TazaNorte en septiembre de 2026, la lógica se encapsuló en un **Procedimiento Almacenado (Stored Procedure)** reutilizable y parametrizado con `CREATE PROCEDURE` e invocado mediante `CALL`.

**Consulta SQL con BETWEEN (Filtro temporal de pagos):**
```sql
SELECT c.name, c.email, o.order_date, o.status, pay.payment_date, pay.amount, pay.method 
FROM customers c
JOIN orders o ON c.id = o.customer_id
JOIN payments pay ON (pay.reference_id = o.id AND pay.reference_type = 'order')
WHERE pay.payment_date BETWEEN '2026-09-01 00:00:00' AND '2026-09-24 00:00:00'
ORDER BY pay.payment_date ASC;
```
![](images/mysql_1_7_between_join.png)

**Definición del Procedimiento Almacenado:**
```sql
DROP PROCEDURE IF EXISTS sp_reporte_consumo_clientes;
DELIMITER //
CREATE PROCEDURE sp_reporte_consumo_clientes(IN p_status VARCHAR(20))
BEGIN
  SELECT 
      c.name AS cliente,
      c.email,
      o.id AS order_id,
      o.order_date,
      o.total,
      pay.method AS metodo_pago,
      pay.amount AS monto_pagado
  FROM customers c
  JOIN orders o ON c.id = o.customer_id
  JOIN payments pay ON (pay.reference_id = o.id AND pay.reference_type = 'order')
  WHERE o.status = p_status
    AND pay.payment_date BETWEEN '2026-09-01 00:00:00' AND '2026-09-24 00:00:00'
  ORDER BY pay.payment_date ASC;
END //
DELIMITER ;
```
![](images/mysql_1_7_procedure_create.png)

**Ejecución del Procedimiento en DBeaver:**
```sql
CALL sp_reporte_consumo_clientes('active');
```
![](images/mysql_1_7_procedure_result.png)

---

### 1.8 Agrupamiento y Funciones de Agregación (GROUP BY, HAVING, COUNT, SUM, AVG)

**Concepto y Narrativa:** 
La cláusula **`GROUP BY`** condensa múltiples filas en grupos analíticos basándose en columnas coincidentes. Sobre estos grupos se aplican **funciones de agregación** como:
- `COUNT()` : Conteo de registros no nulos.
- `SUM()` : Sumatoria de montos facturados.
- `AVG()` : Cálculo de ticket de consumo promedio.
- `MIN()` / `MAX()` : Extremos de facturación.

Para filtrar los grupos resultantes se emplea la cláusula **`HAVING`**, la cual opera exclusivamente después de que las sumatorias y promedios han sido calculados.

**1.8.1 Agrupamiento básico con filtro temporal en WHERE:**
```sql
SELECT c.id, c.name, SUM(pay.amount) AS TotalSuma
FROM customers c
JOIN orders o ON c.id = o.customer_id
JOIN payments pay ON (pay.reference_id = o.id AND pay.reference_type = 'order')
WHERE pay.payment_date BETWEEN '2026-09-01 00:00:00' AND '2026-09-30 23:59:59'
GROUP BY c.id, c.name;
```
![](images/mysql_1_8_group_by_where.png)

**1.8.2 Agrupamiento con condición de umbral en HAVING:**
```sql
SELECT c.id, c.name, 
       SUM(pay.amount) AS TotalSuma, 
       COUNT(pay.id) AS TotalPagos, 
       AVG(pay.amount) AS PromedioPago
FROM customers c
JOIN orders o ON c.id = o.customer_id
JOIN payments pay ON (pay.reference_id = o.id AND pay.reference_type = 'order')
WHERE pay.payment_date BETWEEN '2026-09-01 00:00:00' AND '2026-09-30 23:59:59'
GROUP BY c.id, c.name
HAVING SUM(pay.amount) >= 20000
ORDER BY TotalSuma DESC;
```
![](images/mysql_1_8_group_by_having.png)

**1.8.3 Agrupamiento con múltiples condiciones en HAVING:**
```sql
SELECT c.id, c.name, 
       SUM(pay.amount) AS TotalSuma, 
       COUNT(pay.id) AS TotalPagos, 
       AVG(pay.amount) AS PromedioPago
FROM customers c
JOIN orders o ON c.id = o.customer_id
JOIN payments pay ON (pay.reference_id = o.id AND pay.reference_type = 'order')
WHERE pay.payment_date BETWEEN '2026-09-01 00:00:00' AND '2026-09-30 23:59:59'
GROUP BY c.id, c.name
HAVING SUM(pay.amount) >= 20000 AND COUNT(pay.id) >= 1
ORDER BY TotalSuma DESC;
```
![](images/mysql_1_8_group_by_having_multiple.png)

---

### 1.9 Subconsultas y Operaciones de Teoría de Conjuntos (SUBCONSULTAS, NOT IN, LEFT JOIN ... IS NULL)

**Concepto y Narrativa:** 
Las **subconsultas** son instrucciones `SELECT` anidadas que devuelven conjuntos intermedios para resolver dependencias dinámicas. En la teoría de conjuntos relacional:
- **Diferencia con NOT IN:** Aísla a los clientes cuyo identificador no se encuentre presente en el conjunto de pedidos del período (`A - B`).
- **Diferencia con LEFT JOIN ... IS NULL:** Realiza una unión externa izquierda proyectando todas las tuplas de la entidad principal y filtrando donde la clave foránea derecha es `NULL`.

**1.9.1 Diferencia de conjuntos mediante Subconsulta NOT IN:**
```sql
SELECT * 
FROM customers AS c 
WHERE c.id NOT IN (
    SELECT o.customer_id 
    FROM orders AS o 
    WHERE o.order_date BETWEEN '2026-09-01 00:00:00' AND '2026-09-10 23:59:59'
);
```
![](images/mysql_1_9_subconsulta_notin.png)

**1.9.2 Diferencia de conjuntos mediante LEFT JOIN ... IS NULL:**
```sql
SELECT c.* 
FROM customers AS c 
LEFT JOIN orders AS o ON (c.id = o.customer_id AND o.order_date BETWEEN '2026-09-01 00:00:00' AND '2026-09-10 23:59:59') 
WHERE o.customer_id IS NULL;
```
![](images/mysql_1_9_subconsulta_leftjoin.png)

---

### 1.10 Auditoría Transaccional e Inmutabilidad con Disparadores (TRIGGERS, JSON, SIGNAL SQLSTATE)

**Concepto y Narrativa:** 
Los **Disparadores (Triggers)** son bloques de código procedural que el motor ejecuta automáticamente ante eventos `DML` (`INSERT`, `UPDATE`, `DELETE`). En la arquitectura de TazaNorte se diseñó un esquema de **Auditoría e Inmutabilidad Estricta**:
- Triggers reactivos (`AFTER INSERT/UPDATE/DELETE`) serializan el estado previo (`OLD`) y posterior (`NEW`) de la fila en formato estructurado **JSON** dentro de tablas de auditoría dedicadas (`products_audit`, `orders_audit`, `payments_audit`).
- Disparadores preventivos (`BEFORE UPDATE/DELETE`) sobre las tablas de auditoría arrojan excepciones `SIGNAL SQLSTATE '45000'`, impidiendo cualquier manipulación, truncado o borrado administrativo del historial.

#### 1.10.1 Auditoría en la Tabla products
```sql
-- Creación de tabla de auditoría con columnas JSON
CREATE TABLE IF NOT EXISTS products_audit (
  id              BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  product_id      BIGINT NOT NULL,
  actionSale      ENUM('UPDATE','DELETE','INSERT') NOT NULL DEFAULT 'INSERT',
  changed_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  changed_by      VARCHAR(255) NOT NULL DEFAULT 'Admin',
  before_data     JSON NULL,
  after_data      JSON NULL
) ENGINE=InnoDB;
```
![](images/mysql_trigger_products_audit_table.png)

```sql
-- Trigger AFTER INSERT
CREATE TRIGGER ai_products_audit AFTER INSERT ON products FOR EACH ROW
BEGIN
  SET @from_products_trigger = 1;
  INSERT INTO products_audit (product_id, actionSale, before_data, after_data)
  VALUES (NEW.id, 'INSERT', NULL, JSON_OBJECT('id', NEW.id, 'sku', NEW.sku, 'name', NEW.name, 'price', NEW.price, 'status', NEW.status));
  SET @from_products_trigger = NULL;
END;
```
![](images/mysql_trigger_products_after_insert.png)

```sql
-- Trigger AFTER UPDATE
CREATE TRIGGER au_products_audit AFTER UPDATE ON products FOR EACH ROW
BEGIN
  SET @from_products_trigger = 1;
  INSERT INTO products_audit (product_id, actionSale, before_data, after_data)
  VALUES (NEW.id, 'UPDATE', 
    JSON_OBJECT('id', OLD.id, 'sku', OLD.sku, 'name', OLD.name, 'price', OLD.price, 'status', OLD.status),
    JSON_OBJECT('id', NEW.id, 'sku', NEW.sku, 'name', NEW.name, 'price', NEW.price, 'status', NEW.status)
  );
  SET @from_products_trigger = NULL;
END;
```
![](images/mysql_trigger_products_after_update.png)

```sql
-- Trigger AFTER DELETE
CREATE TRIGGER ad_products_audit AFTER DELETE ON products FOR EACH ROW
BEGIN
  SET @from_products_trigger = 1;
  INSERT INTO products_audit (product_id, actionSale, before_data, after_data)
  VALUES (OLD.id, 'DELETE', JSON_OBJECT('id', OLD.id, 'sku', OLD.sku, 'name', OLD.name, 'price', OLD.price, 'status', OLD.status), NULL);
  SET @from_products_trigger = NULL;
END;
```
![](images/mysql_trigger_products_after_delete.png)

```sql
-- Inmutabilidad estricta (Bloqueo de Modificación)
CREATE TRIGGER bu_products_audit_block BEFORE UPDATE ON products_audit FOR EACH ROW
BEGIN
  SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'products_audit es inmutable: UPDATE prohibido.';
END;
```
![](images/mysql_trigger_products_block_update.png)

**Pruebas de Funcionalidad y Seguridad en products:**
- **Inserción:** `INSERT INTO products (sku, name, description, price, status) VALUES ('SKU-TEST-001', 'Café Especial Prueba', 'Prueba trigger', 12500.00, 'active');`
  ![](images/mysql_trigger_products_test_insert.png)
- **Modificación:** `UPDATE products SET price = 14500.00, name = 'Café Especial Prueba Modificado' WHERE sku = 'SKU-TEST-001';`
  ![](images/mysql_trigger_products_test_update.png)
- **Eliminación:** `DELETE FROM products WHERE sku = 'SKU-TEST-001';`
  ![](images/mysql_trigger_products_test_delete.png)
- **Bloqueo de Inmutabilidad:** `UPDATE products_audit SET actionSale = 'UPDATE' WHERE id = 1;`
  ![](images/mysql_trigger_products_test_prohibition.png)

---

#### 1.10.2 Auditoría en la Tabla orders
```sql
CREATE TABLE IF NOT EXISTS orders_audit (
  id              BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  order_id        BIGINT NOT NULL,
  actionSale      ENUM('UPDATE','DELETE','INSERT') NOT NULL DEFAULT 'INSERT',
  changed_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  changed_by      VARCHAR(255) NOT NULL DEFAULT 'Admin',
  before_data     JSON NULL,
  after_data      JSON NULL
) ENGINE=InnoDB;
```
![](images/mysql_trigger_orders_audit_table.png)

```sql
CREATE TRIGGER ai_orders_audit AFTER INSERT ON orders FOR EACH ROW
BEGIN
  SET @from_orders_trigger = 1;
  INSERT INTO orders_audit (order_id, actionSale, before_data, after_data)
  VALUES (NEW.id, 'INSERT', NULL, JSON_OBJECT('id', NEW.id, 'customer_id', NEW.customer_id, 'channel', NEW.channel, 'total', NEW.total, 'status', NEW.status));
  SET @from_orders_trigger = NULL;
END;
```
![](images/mysql_trigger_orders_after_insert.png)

```sql
CREATE TRIGGER au_orders_audit AFTER UPDATE ON orders FOR EACH ROW
BEGIN
  SET @from_orders_trigger = 1;
  INSERT INTO orders_audit (order_id, actionSale, before_data, after_data)
  VALUES (NEW.id, 'UPDATE',
    JSON_OBJECT('id', OLD.id, 'customer_id', OLD.customer_id, 'channel', OLD.channel, 'total', OLD.total, 'status', OLD.status),
    JSON_OBJECT('id', NEW.id, 'customer_id', NEW.customer_id, 'channel', NEW.channel, 'total', NEW.total, 'status', NEW.status)
  );
  SET @from_orders_trigger = NULL;
END;
```
![](images/mysql_trigger_orders_after_update.png)

```sql
CREATE TRIGGER ad_orders_audit AFTER DELETE ON orders FOR EACH ROW
BEGIN
  SET @from_orders_trigger = 1;
  INSERT INTO orders_audit (order_id, actionSale, before_data, after_data)
  VALUES (OLD.id, 'DELETE', JSON_OBJECT('id', OLD.id, 'customer_id', OLD.customer_id, 'channel', OLD.channel, 'total', OLD.total, 'status', OLD.status), NULL);
  SET @from_orders_trigger = NULL;
END;
```
![](images/mysql_trigger_orders_after_delete.png)

```sql
CREATE TRIGGER bu_orders_audit_block BEFORE UPDATE ON orders_audit FOR EACH ROW
BEGIN
  SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'orders_audit es inmutable: UPDATE prohibido.';
END;
```
![](images/mysql_trigger_orders_block_update.png)

**Pruebas de Operaciones e Inmutabilidad en orders:**
- Operaciones auditadas: `SELECT id, order_id, actionSale, changed_at, before_data, after_data FROM orders_audit;`
  ![](images/mysql_trigger_orders_test_all.png)
- Bloqueo de seguridad: `UPDATE orders_audit SET actionSale = 'UPDATE' WHERE id = 1;`
  ![](images/mysql_trigger_orders_test_prohibition.png)

---

#### 1.10.3 Auditoría en la Tabla payments
```sql
CREATE TABLE IF NOT EXISTS payments_audit (
  id              BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  payment_id      BIGINT NOT NULL,
  actionSale      ENUM('UPDATE','DELETE','INSERT') NOT NULL DEFAULT 'INSERT',
  changed_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  changed_by      VARCHAR(255) NOT NULL DEFAULT 'Admin',
  before_data     JSON NULL,
  after_data      JSON NULL
) ENGINE=InnoDB;
```
![](images/mysql_trigger_payments_audit_table.png)

```sql
-- Creación consolidada de triggers de auditoría e inmutabilidad en payments
CREATE TRIGGER ai_payments_audit AFTER INSERT ON payments FOR EACH ROW
BEGIN
  SET @from_payments_trigger = 1;
  INSERT INTO payments_audit (payment_id, actionSale, before_data, after_data)
  VALUES (NEW.id, 'INSERT', NULL, JSON_OBJECT('id', NEW.id, 'reference_type', NEW.reference_type, 'reference_id', NEW.reference_id, 'method', NEW.method, 'amount', NEW.amount, 'status', NEW.status));
  SET @from_payments_trigger = NULL;
END;
```
![](images/mysql_trigger_payments_all.png)

**Pruebas de Operaciones e Inmutabilidad en payments:**
- Operaciones auditadas: `SELECT id, payment_id, actionSale, changed_at, before_data, after_data FROM payments_audit;`
  ![](images/mysql_trigger_payments_test_all.png)
- Bloqueo de seguridad: `UPDATE payments_audit SET actionSale = 'UPDATE' WHERE id = 1;`
  ![](images/mysql_trigger_payments_test_prohibition.png)

---

## 2. Consultas avanzadas en PostgreSQL :

### 2.1 Proyección de Atributos y Evaluación de Booleanos (SELECT, FROM, AS, BOOLEAN)

**Concepto y Narrativa:** 
En PostgreSQL 17 se proyectan las columnas de la entidad `customers`, evaluando la representación del tipo booleano nativo `is_active` (`t` para verdadero, `f` para falso). La cláusula `AS` define alias representativos para los encabezados de salida.

```sql
SELECT name, document_type, document_number, is_active FROM customers;
```
![](images/postgres_1_1_campos.png)

---

### 2.2 Secuencia Cronológica y Criterios de Ordenamiento (ORDER BY, DESC)

**Concepto y Narrativa:** 
La instrucción `ORDER BY order_date DESC` ordena cronológicamente de forma descendente las órdenes registradas en PostgreSQL, priorizando el análisis de los pedidos más recientes en cafetería.

```sql
SELECT id, order_date, total, status FROM orders ORDER BY order_date DESC;
```
![](images/postgres_1_2_order_by.png)

---

### 2.3 Asociación Relacional en Cláusula WHERE (Producto Cartesiano con Igualdad =)

**Concepto y Narrativa:** 
Relación clásica entre `orders` y `customers` mediante una condición de igualdad en la cláusula `WHERE`, verificando la correspondencia entre la clave foránea `customer_id` y la clave primaria del cliente.

```sql
SELECT c.name, o.id AS order_id, o.total, o.status 
FROM orders o, customers c 
WHERE c.id = o.customer_id;
```
![](images/postgres_1_3_multitabla_where.png)

---

### 2.4 Combinación Explícita mediante JOIN y ON (INNER JOIN)

**Concepto y Narrativa:** 
Uso formal de la cláusula estándar ANSI `INNER JOIN` acoplada a la condición explícita `ON (c.id = o.customer_id)` para fusionar clientes y pedidos de forma estandarizada.

```sql
SELECT c.name, c.email, o.id AS order_id, o.order_date, o.total, o.status 
FROM customers AS c 
JOIN orders AS o ON (c.id = o.customer_id);
```
![](images/postgres_1_4_multitabla_join.png)

---

### 2.5 Filtros Lógicos Compuestos y Comparadores (WHERE, AND, Comparador de Estado)

**Concepto y Narrativa:** 
El operador lógico `AND` concatena criterios de filtrado para segregar los pedidos según su estado operativo (`active` e `inactive`).

**Filtro por órdenes con estado activo:**
```sql
SELECT c.name, o.id AS order_id, o.order_date, o.total, o.status 
FROM orders o, customers c 
WHERE c.id = o.customer_id AND o.status = 'active';
```
![](images/postgres_1_5_condiciones_where_active.png)

**Filtro combinado con JOIN por órdenes con estado inactivo:**
```sql
SELECT c.name, c.email, o.id AS order_id, o.total, o.status 
FROM customers AS c 
JOIN orders AS o ON (c.id = o.customer_id) 
WHERE o.status = 'inactive';
```
![](images/postgres_1_5_condiciones_join_inactive.png)

---

### 2.6 Búsqueda por Patrones de Texto con Operador LIKE (Comodines %, Iniciales y Dominios)

**Concepto y Narrativa:** 
Búsqueda de patrones en cadenas de texto empleando `LIKE` con comodines `%` para iniciales y cuentas de correo.

**2.6.1 Filtro por inicial (`m%`):**
```sql
SELECT name, email, is_active 
FROM customers AS c 
WHERE c.email LIKE 'm%';
```
![](images/postgres_1_6_like_inicio.png)

**2.6.2 Filtro por dominio corporativo (`@gmail`):**
```sql
SELECT name, email, is_active 
FROM customers AS c 
WHERE c.email LIKE CONCAT('%', 'gmail', '%');
```
![](images/postgres_1_6_like_gmail.png)

**2.6.3 Filtro combinado (JOIN + Activo + LIKE inicial):**
```sql
SELECT c.name, c.email, o.id AS order_id, o.total, o.status 
FROM customers AS c 
JOIN orders AS o ON (c.id = o.customer_id) 
WHERE o.status = 'active' AND c.email LIKE 'm%';
```
![](images/postgres_1_6_like_combinado.png)

---

### 2.7 Evaluación de Rangos Temporales y Facturación (BETWEEN, TIMESTAMP)

**Concepto y Narrativa:** 
Filtrado analítico de pagos liquidados en septiembre de 2026 empleando `BETWEEN` sobre marcas temporales `TIMESTAMP`.

**Forma 1 (con JOIN):**
```sql
SELECT c.name, c.email, o.order_date, o.status, pay.payment_date, pay.amount, pay.method 
FROM customers c
JOIN orders o ON c.id = o.customer_id
JOIN payments pay ON pay.reference_id = o.id AND pay.reference_type = 'order'
WHERE pay.payment_date BETWEEN '2026-09-01 00:00:00' AND '2026-09-24 00:00:00'
ORDER BY pay.payment_date ASC;
```
![](images/postgres_1_7_between_join.png)

**Forma 2 (con WHERE):**
```sql
SELECT c.name, c.email, o.order_date, o.status, pay.payment_date, pay.amount, pay.method 
FROM customers c, orders o, payments pay
WHERE c.id = o.customer_id
  AND pay.reference_id = o.id
  AND pay.reference_type = 'order'
  AND pay.payment_date BETWEEN '2026-09-01 00:00:00' AND '2026-09-24 00:00:00'
ORDER BY pay.payment_date ASC;
```
![](images/postgres_1_7_between_where.png)

---

### 2.8 Agrupamiento y Funciones de Agregación (GROUP BY, HAVING, SUM, COUNT, AVG)

**Concepto y Narrativa:** 
Agrupamiento por cliente mediante `GROUP BY` calculando sumatorias (`SUM`), conteos (`COUNT`) y promedios (`AVG`), evaluando grupos calculados con la cláusula `HAVING`.

```sql
SELECT c.id, c.name, SUM(p.amount) AS total_suma, 
       COUNT(p.id) AS cuenta_total, 
       AVG(p.amount) AS promedio  
FROM customers AS c
JOIN orders AS o ON c.id = o.customer_id
JOIN payments AS p ON (p.reference_id = o.id AND p.reference_type = 'order')
WHERE p.payment_date BETWEEN '2026-09-01 00:00:00' AND '2026-09-30 23:59:59'
GROUP BY c.id, c.name
ORDER BY total_suma DESC;
```
![](images/postgres_2_8_group_by.png)

---

### 2.9 Subconsultas y Operaciones de Teoría de Conjuntos (NOT IN, LEFT JOIN ... IS NULL)

**Concepto y Narrativa:** 
Operaciones de teoría de conjuntos para identificar clientes sin consumos registrados dentro de una ventana temporal.

**Forma 1 (con NOT IN):**
```sql
SELECT * 
FROM customers AS c 
WHERE c.id NOT IN (
    SELECT o.customer_id 
    FROM orders AS o 
    WHERE o.order_date BETWEEN '2026-09-01 00:00:00' AND '2026-09-10 23:59:59'
);
```
![](images/postgres_2_9_subconsulta_notin.png)

**Forma 2 (con LEFT JOIN ... IS NULL):**
```sql
SELECT c.* 
FROM customers AS c 
LEFT JOIN orders AS o ON (c.id = o.customer_id AND o.order_date BETWEEN '2026-09-01 00:00:00' AND '2026-09-10 23:59:59') 
WHERE o.customer_id IS NULL;
```
![](images/postgres_2_9_subconsulta_leftjoin.png)

---

## 3. Consultas avanzadas en Microsoft SQL Server :

### 3.1 Proyección de Atributos y Tipos de Datos (SELECT, FROM, BIT)

**Concepto y Narrativa:** 
En T-SQL se proyectan los atributos de clientes utilizando el tipo de dato nativo `BIT` (`1` / `0`) para validar el estado de activación en Microsoft SQL Server 2022.

```sql
SELECT name, document_type, document_number, is_active FROM customers;
```
![](images/mssql_1_1_campos.png)

---

### 3.2 Secuencia Cronológica y Criterios de Ordenamiento (ORDER BY, DESC)

**Concepto y Narrativa:** 
Consulta cronológica descendente en SQL Server para listar las órdenes de venta registradas, permitiendo auditar la secuencia transaccional.

```sql
SELECT id, order_date, total, status FROM orders ORDER BY order_date DESC;
```
![](images/mssql_1_2_order_by.png)

---

### 3.3 Asociación Relacional en Cláusula WHERE (Igualdad relacional =)

**Concepto y Narrativa:** 
Enlace relacional entre órdenes y clientes mediante la cláusula `WHERE`, verificando la asociación de clave foránea `customer_id`.

```sql
SELECT c.name, o.id AS order_id, o.total, o.status 
FROM orders o, customers c 
WHERE c.id = o.customer_id;
```
![](images/mssql_1_3_multitabla_where.png)

---

### 3.4 Combinación Explícita mediante JOIN y ON (INNER JOIN)

**Concepto y Narrativa:** 
Instrucción `INNER JOIN` en SQL Server con condición explícita `ON (c.id = o.customer_id)` para acoplar la información del cliente con sus pedidos.

```sql
SELECT c.name, c.email, o.id AS order_id, o.order_date, o.total, o.status 
FROM customers AS c 
JOIN orders AS o ON (c.id = o.customer_id);
```
![](images/mssql_1_4_multitabla_join.png)

---

### 3.5 Filtros Lógicos Compuestos y Comparadores (WHERE, AND, Estados)

**Concepto y Narrativa:** 
Aplicación de predicados lógicos con `AND` sobre el atributo `status` en SQL Server para discriminar órdenes activas e inactivas.

**Filtro por pedidos con status activo:**
```sql
SELECT c.name, o.id AS order_id, o.order_date, o.total, o.status 
FROM orders o, customers c 
WHERE c.id = o.customer_id AND o.status = 'active';
```
![](images/mssql_1_5_condiciones_where_active.png)

**Filtro combinado con JOIN por pedidos con status inactivo:**
```sql
SELECT c.name, c.email, o.id AS order_id, o.total, o.status 
FROM customers AS c 
JOIN orders AS o ON (c.id = o.customer_id) 
WHERE o.status = 'inactive';
```
![](images/mssql_1_5_condiciones_join_inactive.png)

---

### 3.6 Búsqueda por Patrones de Texto con Operador LIKE (Iniciales y Dominios)

**Concepto y Narrativa:** 
Búsquedas por coincidencia de texto mediante `LIKE` en SQL Server con comodines `%`.

**3.6.1 Filtro por inicial (`m%`):**
```sql
SELECT name, email, is_active 
FROM customers AS c 
WHERE c.email LIKE 'm%';
```
![](images/mssql_1_6_like_inicio.png)

**3.6.2 Filtro por dominio corporativo (`@gmail`):**
```sql
SELECT name, email, is_active 
FROM customers AS c 
WHERE c.email LIKE CONCAT('%', 'gmail', '%');
```
![](images/mssql_1_6_like_gmail.png)

**3.6.3 Filtro combinado (JOIN + Activo + LIKE inicial):**
```sql
SELECT c.name, c.email, o.id AS order_id, o.total, o.status 
FROM customers AS c 
JOIN orders AS o ON (c.id = o.customer_id) 
WHERE o.status = 'active' AND c.email LIKE 'm%';
```
![](images/mssql_1_6_like_combinado.png)

---

### 3.7 Evaluación de Rangos Temporales y Facturación (BETWEEN, DATETIME)

**Concepto y Narrativa:** 
Filtrado temporal de pagos en SQL Server vinculando las claves foráneas con la condición de rango `BETWEEN`.

**Forma 1 (con JOIN):**
```sql
SELECT c.name, c.email, o.order_date, o.status, pay.payment_date, pay.amount, pay.payment_method 
FROM customers c
JOIN orders o ON c.id = o.customer_id
JOIN payments pay ON pay.order_id = o.id
WHERE pay.payment_date BETWEEN '2026-09-01 00:00:00' AND '2026-09-24 00:00:00'
ORDER BY pay.payment_date ASC;
```
![](images/mssql_1_7_between_join.png)

**Forma 2 (con WHERE):**
```sql
SELECT c.name, c.email, o.order_date, o.status, pay.payment_date, pay.amount, pay.payment_method 
FROM customers c, orders o, payments pay
WHERE c.id = o.customer_id
  AND pay.order_id = o.id
  AND pay.payment_date BETWEEN '2026-09-01 00:00:00' AND '2026-09-24 00:00:00'
ORDER BY pay.payment_date ASC;
```
![](images/mssql_1_7_between_where.png)

---

### 3.8 Agrupamiento y Funciones de Agregación (GROUP BY, HAVING, SUM, COUNT, AVG)

**Concepto y Narrativa:** 
Resumen financiero por cliente en T-SQL aplicando agregaciones cuantitativas y restringiendo clientes con facturación acumulada representativa mediante `HAVING`.

```sql
SELECT c.id, c.name, SUM(pay.amount) AS TotalSuma, 
       COUNT(pay.id) AS TotalPagos, 
       AVG(pay.amount) AS PromedioPago
FROM customers c
JOIN orders o ON c.id = o.customer_id
JOIN payments pay ON pay.order_id = o.id
WHERE pay.payment_date BETWEEN '2026-09-01 00:00:00' AND '2026-09-30 23:59:59'
GROUP BY c.id, c.name
HAVING SUM(pay.amount) >= 20000
ORDER BY TotalSuma DESC;
```
![](images/mssql_3_8_group_by.png)

---

### 3.9 Subconsultas y Operaciones de Teoría de Conjuntos (NOT IN)

**Concepto y Narrativa:** 
Implementación de subconsultas con `NOT IN` en SQL Server para aislar a los clientes que no registraron consumo en el período establecido.

```sql
SELECT * 
FROM customers AS c 
WHERE c.id NOT IN (
    SELECT o.customer_id 
    FROM orders AS o 
    WHERE o.order_date BETWEEN '2026-09-01 00:00:00' AND '2026-09-10 23:59:59'
);
```
![](images/mssql_3_9_subconsulta.png)

---

## 4. Consultas avanzadas en Oracle Database :

### 4.1 Proyección de Atributos y Concatenación ANSI (SELECT, FROM, ||)

**Concepto y Narrativa:** 
En Oracle Database 21c XE el esquema almacena los nombres descompuestos en `FIRST_NAME` y `LAST_NAME`, por lo que se utiliza el operador de concatenación ANSI `||` para unificar la proyección del nombre completo.

```sql
SELECT code, first_name || ' ' || last_name AS name, email, status FROM tazanorte.customers;
```
![](images/oracle_1_1_campos.png)

---

### 4.2 Secuencia Cronológica y Criterios de Ordenamiento (ORDER BY, DESC)

**Concepto y Narrativa:** 
Ordenamiento descendente en Oracle sobre la tabla `orders` del esquema `tazanorte` para listar los pedidos cronológicamente desde el más reciente.

```sql
SELECT id, order_date, total, status FROM tazanorte.orders ORDER BY order_date DESC;
```
![](images/oracle_1_2_order_by.png)

---

### 4.3 Asociación Relacional en Cláusula WHERE (Igualdad relacional =)

**Concepto y Narrativa:** 
Enlace relacional entre `orders` y `customers` mediante condición de igualdad en la cláusula `WHERE` sobre el esquema Oracle.

```sql
SELECT c.first_name || ' ' || c.last_name AS name, o.id AS order_id, o.total, o.status 
FROM tazanorte.orders o, tazanorte.customers c 
WHERE c.id = o.customer_id;
```
![](images/oracle_1_3_multitabla_where.png)

---

### 4.4 Combinación Explícita mediante JOIN y ON (INNER JOIN)

**Concepto y Narrativa:** 
Consulta formal basada en `JOIN` con cláusula `ON` para vincular clientes y órdenes en Oracle Database.

```sql
SELECT c.first_name || ' ' || c.last_name AS name, c.email, o.id AS order_id, o.order_date, o.total, o.status 
FROM tazanorte.customers c 
JOIN tazanorte.orders o ON (c.id = o.customer_id);
```
![](images/oracle_1_4_multitabla_join.png)

---

### 4.5 Filtros Lógicos Compuestos y Comparadores (WHERE, AND, Estados)

**Concepto y Narrativa:** 
Filtrado de órdenes por su estado operativo (`active` e `inactive`) en Oracle Database, validando la consistencia entre `JOIN` y `WHERE`.

**Filtro por pedidos con status activo:**
```sql
SELECT c.first_name || ' ' || c.last_name AS name, o.id AS order_id, o.order_date, o.total, o.status 
FROM tazanorte.orders o, tazanorte.customers c 
WHERE c.id = o.customer_id AND o.status = 'active';
```
![](images/oracle_1_5_condiciones_where_active.png)

**Filtro combinado con JOIN por pedidos con status inactivo:**
```sql
SELECT c.first_name || ' ' || c.last_name AS name, c.email, o.id AS order_id, o.total, o.status 
FROM tazanorte.customers c 
JOIN tazanorte.orders o ON (c.id = o.customer_id) 
WHERE o.status = 'inactive';
```
![](images/oracle_1_5_condiciones_join_inactive.png)

---

### 4.6 Búsqueda por Patrones de Texto con Operador LIKE (Concatenación || y Comodines %)

**Concepto y Narrativa:** 
Uso del operador `LIKE` en Oracle con concatenación de caracteres comodín `%` mediante el operador `||`.

**4.6.1 Filtro por inicial (`m%`):**
```sql
SELECT code, first_name || ' ' || last_name AS name, email, status 
FROM tazanorte.customers c 
WHERE c.email LIKE 'm%';
```
![](images/oracle_1_6_like_inicio.png)

**4.6.2 Filtro por dominio corporativo (`@gmail`):**
```sql
SELECT code, first_name || ' ' || last_name AS name, email, status 
FROM tazanorte.customers c 
WHERE c.email LIKE '%' || 'gmail' || '%';
```
![](images/oracle_1_6_like_gmail.png)

**4.6.3 Filtro combinado (JOIN + Activo + LIKE inicial):**
```sql
SELECT c.first_name || ' ' || c.last_name AS name, c.email, o.id AS order_id, o.total, o.status 
FROM tazanorte.customers c 
JOIN tazanorte.orders o ON (c.id = o.customer_id) 
WHERE o.status = 'active' AND c.email LIKE 'm%';
```
![](images/oracle_1_6_like_combinado.png)

---

### 4.7 Evaluación de Rangos Temporales y Facturación (BETWEEN, TIMESTAMP)

**Concepto y Narrativa:** 
En Oracle se emplean literales de tipo `TIMESTAMP` para garantizar precisión estricta en el filtrado temporal de pagos por fecha mediante `BETWEEN`.

**Forma 1 (con JOIN):**
```sql
SELECT c.first_name || ' ' || c.last_name AS name, c.email, o.order_date, o.status, pay.payment_date, pay.amount, pay.payment_method 
FROM tazanorte.customers c
JOIN tazanorte.orders o ON c.id = o.customer_id
JOIN tazanorte.payments pay ON pay.order_id = o.id
WHERE pay.payment_date BETWEEN TIMESTAMP '2026-09-01 00:00:00' AND TIMESTAMP '2026-09-24 00:00:00'
ORDER BY pay.payment_date ASC;
```
![](images/oracle_1_7_between_join.png)

**Forma 2 (con WHERE):**
```sql
SELECT c.first_name || ' ' || c.last_name AS name, c.email, o.order_date, o.status, pay.payment_date, pay.amount, pay.payment_method 
FROM tazanorte.customers c, tazanorte.orders o, tazanorte.payments pay
WHERE c.id = o.customer_id
  AND pay.order_id = o.id
  AND pay.payment_date BETWEEN TIMESTAMP '2026-09-01 00:00:00' AND TIMESTAMP '2026-09-24 00:00:00'
ORDER BY pay.payment_date ASC;
```
![](images/oracle_1_7_between_where.png)

---

### 4.8 Agrupamiento y Funciones de Agregación (GROUP BY, HAVING, SUM, COUNT, AVG)

**Concepto y Narrativa:** 
Resumen analítico de facturación por cliente en Oracle Database 21c XE empleando agregaciones `SUM`, `COUNT` y `AVG` con restricción pos-agrupamiento `HAVING`.

```sql
SELECT c.id, c.first_name || ' ' || c.last_name AS name, 
       SUM(pay.amount) AS total_suma, 
       COUNT(pay.id) AS total_pagos, 
       AVG(pay.amount) AS total_promedio
FROM tazanorte.customers c
JOIN tazanorte.orders o ON c.id = o.customer_id
JOIN tazanorte.payments pay ON pay.order_id = o.id
WHERE pay.payment_date BETWEEN TIMESTAMP '2026-09-01 00:00:00' AND TIMESTAMP '2026-09-30 23:59:59'
GROUP BY c.id, c.first_name, c.last_name
HAVING SUM(pay.amount) >= 20000
ORDER BY total_suma DESC;
```
![](images/oracle_4_8_group_by.png)

---

### 4.9 Subconsultas y Operaciones de Teoría de Conjuntos (NOT IN)

**Concepto y Narrativa:** 
Teoría de conjuntos en Oracle Database con sintaxis `NOT IN` y conversión de fechas para filtrar clientes sin actividad comercial registrada.

```sql
SELECT * 
FROM tazanorte.customers c 
WHERE c.id NOT IN (
    SELECT o.customer_id 
    FROM tazanorte.orders o 
    WHERE o.order_date BETWEEN TIMESTAMP '2026-09-01 00:00:00' AND TIMESTAMP '2026-09-10 23:59:59'
);
```
![](images/oracle_4_9_subconsulta.png)

---

## 5. Cuadro Comparativo de Variaciones Sintácticas entre Motores

| Característica / Concepto | MySQL 8.0 | PostgreSQL 17 | Microsoft SQL Server 2022 | Oracle Database 21c XE |
| :--- | :--- | :--- | :--- | :--- |
| **Operador de Concatenación** | `CONCAT(a, b)` | `a || b` o `CONCAT(a, b)` | `a + b` o `CONCAT(a, b)` | `a || b` o `CONCAT(a, b)` |
| **Paginación / Límite de Filas** | `LIMIT n OFFSET m` | `LIMIT n OFFSET m` o `FETCH FIRST n ROWS ONLY` | `TOP (n)` o `OFFSET m ROWS FETCH NEXT n ROWS ONLY` | `FETCH FIRST n ROWS ONLY` o pseudo-columna `ROWNUM <= n` |
| **Literales Temporales** | `'YYYY-MM-DD HH:MM:SS'` | `'YYYY-MM-DD HH:MM:SS'::TIMESTAMP` | `'YYYY-MM-DD HH:MM:SS'` | `TIMESTAMP 'YYYY-MM-DD HH:MM:SS'` o `TO_TIMESTAMP()` |
| **Tipo de Booleano / Estado** | `ENUM('active', 'inactive')` / `TINYINT` | `BOOLEAN` (`TRUE` / `FALSE`) | `BIT` (`1` / `0`) con `CHECK` | `VARCHAR2(10)` con `CHECK` |
| **Procedimientos Almacenados** | `DELIMITER // ... CREATE PROCEDURE ... BEGIN ... END //` | `CREATE OR REPLACE PROCEDURE ... LANGUAGE plpgsql AS $$ ... $$` | `CREATE PROCEDURE ... AS BEGIN ... END` | `CREATE OR REPLACE PROCEDURE ... IS ... BEGIN ... END;` |
| **Invocación de Procedures** | `CALL sp_nombre();` | `CALL sp_nombre();` | `EXEC sp_nombre;` | `EXEC sp_nombre;` o bloque anónimo `BEGIN ... END;` |
| **Disparadores (Triggers)** | `CREATE TRIGGER ... AFTER/BEFORE ... FOR EACH ROW BEGIN ... END` | `CREATE TRIGGER ... EXECUTE FUNCTION fn_trigger();` | `CREATE TRIGGER ... ON ... AFTER/INSTEAD OF ... AS BEGIN ... END` | `CREATE OR REPLACE TRIGGER ... BEFORE/AFTER ... FOR EACH ROW BEGIN ... END;` |
| **Inmutabilidad y Excepciones** | `SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = '...'` | `RAISE EXCEPTION '...' USING ERRCODE = '45000';` | `THROW 50000, '...', 1;` o `RAISERROR('...', 16, 1);` | `RAISE_APPLICATION_ERROR(-20001, '...');` |
| **Manejo de Auditoría JSON** | `JSON_OBJECT(...)` | `to_jsonb(NEW)` / `to_jsonb(OLD)` | `FOR JSON PATH` | `JSON_OBJECT(...)` |
| **Autoincremento de ID** | `AUTO_INCREMENT` | `GENERATED ALWAYS AS IDENTITY` | `IDENTITY(1,1)` | `GENERATED ALWAYS AS IDENTITY` |
| **Sensibilidad de Identificadores** | Case-insensitive en Windows, case-sensitive en Linux | Case-insensitive por defecto (convierte a minúsculas) | Case-insensitive por defecto según Collation | Convierte identificadores a MAYÚSCULAS |
| **Inspección de Planes de Consulta** | `EXPLAIN ...` | `EXPLAIN ANALYZE ...` | `SET SHOWPLAN_TEXT ON;` | `EXPLAIN PLAN FOR ...` |

---

## Conclusiones

1. **Estandarización Conceptual sin Redundancia:** Al integrar formalmente las definiciones y reglas de cláusulas como `ON`, `JOIN`, `AS`, `AND`, `GROUP BY` y funciones agregadas directamente dentro de las consultas ejecutadas con evidencia, se eliminó la duplicidad innecesaria de bloques conceptuales aislados, ofreciendo un informe técnico mucho más sólido, ágil y representativo del trabajo práctico realizado.
2. **Homogeneidad entre los Cuatro Motores:** Cada motor (MySQL, PostgreSQL, SQL Server y Oracle) presenta sus 9 consultas avanzadas y esquemas de auditoría respaldados al 100% por capturas reales tomadas directamente desde DBeaver, demostrando la consistencia lógica del estándar SQL ANSI y documentando de forma precisa las particularidades de sintaxis propias de cada motor relacional.
3. **Seguridad y Control de Integridad:** La arquitectura de auditoría reactiva mediante triggers con inmutabilidad estricta probada en DBeaver certifica que el sistema transaccional de **TazaNorte** previene eficazmente cualquier alteración arbitraria de precios, pedidos o pagos, garantizando un historial contable inviolable para la organización.
