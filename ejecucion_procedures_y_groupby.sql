-- ==============================================================================
-- PROYECTO TAZANORTE - BASE DE DATOS II
-- SCRIPT CONSOLIDADO: STORED PROCEDURES Y CONSULTAS GROUP BY / HAVING (MySQL 8.0)
-- ==============================================================================
-- Indicaciones para DBeaver:
-- 1. Asegúrese de estar conectado a la base de datos "TazaNorte".
-- 2. Puede seleccionar cada bloque y presionar [Ctrl + Enter] para ejecutarlo.
-- 3. Cada bloque indica el nombre de la captura que debe tomar como evidencia.
-- ==============================================================================

USE TazaNorte;

-- ==============================================================================
-- 1.1 MOSTRAR ALGUNOS REGISTROS DE LA TABLA CUSTOMERS
-- ==============================================================================

-- [Evidencia: Creación de Procedure -> mysql_1_1_procedure_create.png]
DROP PROCEDURE IF EXISTS sp_get_customers;
DELIMITER //
CREATE PROCEDURE sp_get_customers()
BEGIN
    SELECT name, document_type, document_number, status 
    FROM customers;
END //
DELIMITER ;

-- [Evidencia: Ejecución del Procedure -> mysql_1_1_procedure_result.png]
CALL sp_get_customers();


-- ==============================================================================
-- 1.2 MOSTRAR DE FORMA ORDENADA (DESC) LOS PEDIDOS DESDE SU COMIENZO
-- ==============================================================================

-- [Evidencia: Creación de Procedure -> mysql_1_2_procedure_create.png]
DROP PROCEDURE IF EXISTS sp_get_orders_desc;
DELIMITER //
CREATE PROCEDURE sp_get_orders_desc()
BEGIN
    SELECT id, order_date, total, status 
    FROM orders 
    ORDER BY order_date DESC;
END //
DELIMITER ;

-- [Evidencia: Ejecución del Procedure -> mysql_1_2_procedure_result.png]
CALL sp_get_orders_desc();


-- ==============================================================================
-- 1.3 CONSULTA A MÚLTIPLES TABLAS MEDIANTE WHERE
-- ==============================================================================

-- [Evidencia: Creación de Procedure -> mysql_1_3_procedure_create.png]
DROP PROCEDURE IF EXISTS sp_get_orders_customers_where;
DELIMITER //
CREATE PROCEDURE sp_get_orders_customers_where()
BEGIN
    SELECT c.name, o.id AS order_id, o.total, o.status 
    FROM orders o, customers c 
    WHERE c.id = o.customer_id;
END //
DELIMITER ;

-- [Evidencia: Ejecución del Procedure -> mysql_1_3_procedure_result.png]
CALL sp_get_orders_customers_where();


-- ==============================================================================
-- 1.4 CONSULTA A MÚLTIPLES TABLAS MEDIANTE JOIN
-- ==============================================================================

-- [Evidencia: Creación de Procedure -> mysql_1_4_procedure_create.png]
DROP PROCEDURE IF EXISTS sp_get_orders_customers_join;
DELIMITER //
CREATE PROCEDURE sp_get_orders_customers_join()
BEGIN
    SELECT c.name, c.email, o.id AS order_id, o.order_date, o.total, o.status 
    FROM customers AS c 
    JOIN orders AS o ON (c.id = o.customer_id);
END //
DELIMITER ;

-- [Evidencia: Ejecución del Procedure -> mysql_1_4_procedure_result.png]
CALL sp_get_orders_customers_join();


-- ==============================================================================
-- 1.5 CONDICIONES Y FILTROS EN LAS CONSULTAS (ACTIVE / INACTIVE)
-- ==============================================================================

-- [Evidencia: Creación de Procedure -> mysql_1_5_procedure_create.png]
DROP PROCEDURE IF EXISTS sp_get_orders_by_status;
DELIMITER //
CREATE PROCEDURE sp_get_orders_by_status(IN p_status VARCHAR(20))
BEGIN
    SELECT c.name, c.email, o.id AS order_id, o.order_date, o.total, o.status 
    FROM customers AS c 
    JOIN orders AS o ON (c.id = o.customer_id)
    WHERE o.status = p_status;
END //
DELIMITER ;

-- [Evidencia: Ejecución del Procedure -> mysql_1_5_procedure_result.png]
CALL sp_get_orders_by_status('inactive');
CALL sp_get_orders_by_status('active');


-- ==============================================================================
-- 1.6 CONSULTAS CON FILTRO CONDICIONAL LIKE
-- ==============================================================================

-- [Evidencia: Creación de Procedure -> mysql_1_6_procedure_create.png]
DROP PROCEDURE IF EXISTS sp_get_orders_like_combinado;
DELIMITER //
CREATE PROCEDURE sp_get_orders_like_combinado(IN p_status VARCHAR(20), IN p_initial VARCHAR(10))
BEGIN
    SELECT c.name, c.email, o.id AS order_id, o.total, o.status 
    FROM customers AS c 
    JOIN orders AS o ON (c.id = o.customer_id) 
    WHERE o.status = p_status AND c.email LIKE CONCAT(p_initial, '%');
END //
DELIMITER ;

-- [Evidencia: Ejecución del Procedure -> mysql_1_6_procedure_result.png]
CALL sp_get_orders_like_combinado('active', 'm');


-- ==============================================================================
-- 1.7 CONSULTAS CON FILTROS CONDICIONALES BETWEEN
-- ==============================================================================

-- [Evidencia: Creación de Procedure -> mysql_1_7_procedure_create.png]
DROP PROCEDURE IF EXISTS sp_get_payments_between;
DELIMITER //
CREATE PROCEDURE sp_get_payments_between(IN p_inicio DATETIME, IN p_fin DATETIME)
BEGIN
    SELECT c.name, c.email, o.order_date, o.status, pay.payment_date, pay.amount, pay.method 
    FROM customers c
    JOIN orders o ON c.id = o.customer_id
    JOIN payments pay ON pay.reference_id = o.id AND pay.reference_type = 'order'
    WHERE pay.payment_date BETWEEN p_inicio AND p_fin
    ORDER BY pay.payment_date ASC;
END //
DELIMITER ;

-- [Evidencia: Ejecución del Procedure -> mysql_1_7_procedure_result.png]
CALL sp_get_payments_between('2026-09-01 00:00:00', '2026-09-24 00:00:00');


-- ==============================================================================
-- 1.8 CONSULTAS CON AGRUPAMIENTO GROUP BY Y CLÁUSULA HAVING
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- 1.8.1 FORMA 1 (CON WHERE): Resumen mensual de pagos por cliente (SUM, COUNT, AVG)
-- ------------------------------------------------------------------------------

-- [Evidencia: Consulta directa -> mysql_1_8_group_by_where.png]
SELECT c.id, c.name, SUM(p.amount) AS TotalSuma, 
       COUNT(p.id) AS CuentaTotal, 
       AVG(p.amount) AS Promedio  
FROM customers AS c
JOIN orders AS o ON c.id = o.customer_id
JOIN payments AS p ON (p.reference_id = o.id AND p.reference_type = 'order')
WHERE p.payment_date BETWEEN '2026-09-01 00:00:00' AND '2026-09-30 23:59:59'
GROUP BY c.id, c.name
ORDER BY TotalSuma DESC;

-- [Evidencia: Creación de Procedure -> mysql_1_8_group_by_where_procedure_create.png]
DROP PROCEDURE IF EXISTS sp_resumen_pagos_periodo;
DELIMITER //
CREATE PROCEDURE sp_resumen_pagos_periodo(IN p_inicio DATETIME, IN p_fin DATETIME)
BEGIN
    SELECT c.id, c.name, SUM(p.amount) AS TotalSuma, 
           COUNT(p.id) AS CuentaTotal, 
           AVG(p.amount) AS Promedio  
    FROM customers AS c
    JOIN orders AS o ON c.id = o.customer_id
    JOIN payments AS p ON (p.reference_id = o.id AND p.reference_type = 'order')
    WHERE p.payment_date BETWEEN p_inicio AND p_fin
    GROUP BY c.id, c.name
    ORDER BY TotalSuma DESC;
END //
DELIMITER ;

-- [Evidencia: Ejecución del Procedure -> mysql_1_8_group_by_where_procedure_result.png]
CALL sp_resumen_pagos_periodo('2026-09-01 00:00:00', '2026-09-30 23:59:59');


-- ------------------------------------------------------------------------------
-- 1.8.2 FORMA 1: Resumen de pagos con filtro por estado y método (active + card)
-- ------------------------------------------------------------------------------

-- [Evidencia: Consulta directa -> mysql_1_8_group_by_condicion.png]
SELECT c.id, c.name, SUM(p.amount) AS TotalGasto, 
       COUNT(p.id) AS CantidadPagos
FROM customers AS c
JOIN orders AS o ON c.id = o.customer_id
JOIN payments AS p ON (p.reference_id = o.id AND p.reference_type = 'order')
WHERE p.status = 'active' AND p.method = 'card'
GROUP BY c.id, c.name
ORDER BY TotalGasto DESC;

-- [Evidencia: Creación de Procedure -> mysql_1_8_group_by_condicion_procedure_create.png]
DROP PROCEDURE IF EXISTS sp_resumen_pagos_metodo_estado;
DELIMITER //
CREATE PROCEDURE sp_resumen_pagos_metodo_estado(IN p_status VARCHAR(20), IN p_method VARCHAR(50))
BEGIN
    SELECT c.id, c.name, SUM(p.amount) AS TotalGasto, 
           COUNT(p.id) AS CantidadPagos
    FROM customers AS c
    JOIN orders AS o ON c.id = o.customer_id
    JOIN payments AS p ON (p.reference_id = o.id AND p.reference_type = 'order')
    WHERE p.status = p_status AND p.method = p_method
    GROUP BY c.id, c.name
    ORDER BY TotalGasto DESC;
END //
DELIMITER ;

-- [Evidencia: Ejecución del Procedure -> mysql_1_8_group_by_condicion_procedure_result.png]
CALL sp_resumen_pagos_metodo_estado('active', 'card');


-- ------------------------------------------------------------------------------
-- 1.8.3 FORMA 2 (CON HAVING): Clientes con total pagado >= 20000
-- ------------------------------------------------------------------------------

-- [Evidencia: Consulta directa -> mysql_1_8_group_by_having.png]
SELECT c.id, c.name, SUM(p.amount) AS TotalSuma, 
       AVG(p.amount) AS PromedioPago
FROM customers AS c
JOIN orders AS o ON c.id = o.customer_id
JOIN payments AS p ON (p.reference_id = o.id AND p.reference_type = 'order') 
GROUP BY c.id, c.name 
HAVING SUM(p.amount) >= 20000 
ORDER BY TotalSuma DESC;

-- [Evidencia: Creación de Procedure -> mysql_1_8_group_by_having_procedure_create.png]
DROP PROCEDURE IF EXISTS sp_resumen_pagos_minimo;
DELIMITER //
CREATE PROCEDURE sp_resumen_pagos_minimo(IN p_min_monto DECIMAL(15,2))
BEGIN
    SELECT c.id, c.name, SUM(p.amount) AS TotalSuma, 
           AVG(p.amount) AS PromedioPago
    FROM customers AS c
    JOIN orders AS o ON c.id = o.customer_id
    JOIN payments AS p ON (p.reference_id = o.id AND p.reference_type = 'order') 
    GROUP BY c.id, c.name 
    HAVING SUM(p.amount) >= p_min_monto 
    ORDER BY TotalSuma DESC;
END //
DELIMITER ;

-- [Evidencia: Ejecución del Procedure -> mysql_1_8_group_by_having_procedure_result.png]
CALL sp_resumen_pagos_minimo(20000);


-- ------------------------------------------------------------------------------
-- 1.8.4 FORMA 2: Segmentación con filtro BETWEEN y HAVING compuesto (COUNT >= 1 AND SUM > 15000)
-- ------------------------------------------------------------------------------

-- [Evidencia: Consulta directa -> mysql_1_8_group_by_having_multiple.png]
SELECT c.id, c.name, c.email, SUM(p.amount) AS TotalPeriodo,   
       COUNT(p.id) AS TotalPagos 
FROM customers AS c 
JOIN orders AS o ON c.id = o.customer_id
JOIN payments AS p ON (p.reference_id = o.id AND p.reference_type = 'order')
WHERE p.payment_date BETWEEN '2026-09-01 00:00:00' AND '2026-09-30 23:59:59'
GROUP BY c.id, c.name, c.email
HAVING COUNT(p.id) >= 1 AND SUM(p.amount) > 15000
ORDER BY TotalPeriodo DESC;

-- [Evidencia: Creación de Procedure -> mysql_1_8_group_by_having_multiple_procedure_create.png]
DROP PROCEDURE IF EXISTS sp_resumen_pagos_anual_having;
DELIMITER //
CREATE PROCEDURE sp_resumen_pagos_anual_having(IN p_inicio DATETIME, IN p_fin DATETIME, IN p_min_pagos INT, IN p_min_total DECIMAL(15,2))
BEGIN
    SELECT c.id, c.name, c.email, SUM(p.amount) AS TotalPeriodo,   
           COUNT(p.id) AS TotalPagos 
    FROM customers AS c 
    JOIN orders AS o ON c.id = o.customer_id
    JOIN payments AS p ON (p.reference_id = o.id AND p.reference_type = 'order')
    WHERE p.payment_date BETWEEN p_inicio AND p_fin
    GROUP BY c.id, c.name, c.email
    HAVING COUNT(p.id) >= p_min_pagos AND SUM(p.amount) > p_min_total
    ORDER BY TotalPeriodo DESC;
END //
DELIMITER ;

-- [Evidencia: Ejecución del Procedure -> mysql_1_8_group_by_having_multiple_procedure_result.png]
CALL sp_resumen_pagos_anual_having('2026-09-01 00:00:00', '2026-09-30 23:59:59', 1, 15000);


-- ==============================================================================
-- 1.9 SUBCONSULTAS Y TEORÍA DE CONJUNTOS
-- ==============================================================================

-- [Evidencia: Forma 1 (NOT IN) -> mysql_1_9_subconsulta_notin.png]
SELECT * 
FROM customers AS c 
WHERE c.id NOT IN (
    SELECT o.customer_id 
    FROM orders AS o 
    WHERE o.order_date BETWEEN '2026-09-01 00:00:00' AND '2026-09-10 23:59:59'
);

-- [Evidencia: Forma 2 (LEFT JOIN ... IS NULL) -> mysql_1_9_subconsulta_leftjoin.png]
SELECT c.* 
FROM customers AS c 
LEFT JOIN orders AS o ON (c.id = o.customer_id AND o.order_date BETWEEN '2026-09-01 00:00:00' AND '2026-09-10 23:59:59') 
WHERE o.customer_id IS NULL;

-- [Evidencia: Creación de Procedure -> mysql_1_9_procedure_create.png]
DROP PROCEDURE IF EXISTS sp_clientes_sin_ordenes_periodo;
DELIMITER //
CREATE PROCEDURE sp_clientes_sin_ordenes_periodo(IN p_inicio DATETIME, IN p_fin DATETIME)
BEGIN
    SELECT c.* 
    FROM customers AS c 
    LEFT JOIN orders AS o ON (c.id = o.customer_id AND o.order_date BETWEEN p_inicio AND p_fin) 
    WHERE o.customer_id IS NULL;
END //
DELIMITER ;

-- [Evidencia: Ejecución del Procedure -> mysql_1_9_procedure_result.png]
CALL sp_clientes_sin_ordenes_periodo('2026-09-01 00:00:00', '2026-09-10 23:59:59');


-- ==============================================================================
-- 2.0 TRIGGERS DE AUDITORÍA E INMUTABILIDAD EN TABLA: PRODUCTS
-- ==============================================================================

-- [Evidencia: Creación de Tabla Auditoría -> mysql_trigger_products_audit_table.png]
DROP TABLE IF EXISTS products_audit;
CREATE TABLE IF NOT EXISTS products_audit (
  id              BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  product_id      BIGINT NOT NULL,
  actionSale      ENUM('UPDATE','DELETE','INSERT') NOT NULL DEFAULT 'INSERT',
  changed_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  changed_by      VARCHAR(255) NOT NULL DEFAULT 'Admin',
  before_data     JSON NULL,
  after_data      JSON NULL
) ENGINE=InnoDB;

-- [Evidencia: Trigger AFTER INSERT -> mysql_trigger_products_after_insert.png]
DROP TRIGGER IF EXISTS ai_products_audit;
DELIMITER //
CREATE TRIGGER ai_products_audit AFTER INSERT ON products FOR EACH ROW
BEGIN
  SET @from_products_trigger = 1;
  INSERT INTO products_audit (product_id, actionSale, before_data, after_data)
  VALUES (
    NEW.id, 'INSERT', NULL,
    JSON_OBJECT('id', NEW.id, 'sku', NEW.sku, 'name', NEW.name, 'price', NEW.price, 'status', NEW.status)
  );
  SET @from_products_trigger = NULL;
END //
DELIMITER ;

-- [Evidencia: Trigger AFTER UPDATE -> mysql_trigger_products_after_update.png]
DROP TRIGGER IF EXISTS au_products_audit;
DELIMITER //
CREATE TRIGGER au_products_audit AFTER UPDATE ON products FOR EACH ROW
BEGIN
  SET @from_products_trigger = 1;
  INSERT INTO products_audit (product_id, actionSale, before_data, after_data)
  VALUES (
    NEW.id, 'UPDATE',
    JSON_OBJECT('id', OLD.id, 'sku', OLD.sku, 'name', OLD.name, 'price', OLD.price, 'status', OLD.status),
    JSON_OBJECT('id', NEW.id, 'sku', NEW.sku, 'name', NEW.name, 'price', NEW.price, 'status', NEW.status)
  );
  SET @from_products_trigger = NULL;
END //
DELIMITER ;

-- [Evidencia: Trigger AFTER DELETE -> mysql_trigger_products_after_delete.png]
DROP TRIGGER IF EXISTS ad_products_audit;
DELIMITER //
CREATE TRIGGER ad_products_audit AFTER DELETE ON products FOR EACH ROW
BEGIN
  SET @from_products_trigger = 1;
  INSERT INTO products_audit (product_id, actionSale, before_data, after_data)
  VALUES (
    OLD.id, 'DELETE',
    JSON_OBJECT('id', OLD.id, 'sku', OLD.sku, 'name', OLD.name, 'price', OLD.price, 'status', OLD.status),
    NULL
  );
  SET @from_products_trigger = NULL;
END //
DELIMITER ;

-- [Evidencia: Inmutabilidad BEFORE UPDATE -> mysql_trigger_products_block_update.png]
DROP TRIGGER IF EXISTS bu_products_audit_block;
DELIMITER //
CREATE TRIGGER bu_products_audit_block BEFORE UPDATE ON products_audit FOR EACH ROW
BEGIN
  SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'products_audit es inmutable: UPDATE prohibido.';
END //
DELIMITER ;

-- [Evidencia: Inmutabilidad BEFORE DELETE -> mysql_trigger_products_block_delete.png]
DROP TRIGGER IF EXISTS bd_products_audit_block;
DELIMITER //
CREATE TRIGGER bd_products_audit_block BEFORE DELETE ON products_audit FOR EACH ROW
BEGIN
  SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'products_audit es inmutable: DELETE prohibido.';
END //
DELIMITER ;

-- [Evidencia: Control BEFORE INSERT -> mysql_trigger_products_guard_insert.png]
DROP TRIGGER IF EXISTS bi_products_audit_guard;
DELIMITER //
CREATE TRIGGER bi_products_audit_guard BEFORE INSERT ON products_audit FOR EACH ROW
BEGIN
  IF @from_products_trigger IS NULL OR @from_products_trigger <> 1 THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'INSERT en products_audit solo permitido desde triggers autorizados.';
  END IF;
END //
DELIMITER ;

-- PRUEBAS DE FUNCIONALIDAD PRODUCTS:
-- [Evidencia: Prueba Insertar -> mysql_trigger_products_test_insert.png]
INSERT INTO products (sku, name, description, price, status) 
VALUES ('SKU-TEST-001', 'Café Especial Prueba', 'Prueba trigger', 12500.00, 'active');

-- [Evidencia: Prueba Modificar -> mysql_trigger_products_test_update.png]
UPDATE products SET price = 14000.00 WHERE sku = 'SKU-TEST-001';

-- [Evidencia: Prueba Eliminar -> mysql_trigger_products_test_delete.png]
DELETE FROM products WHERE sku = 'SKU-TEST-001';

-- [Evidencia: Prueba Prohibición Inmutabilidad -> mysql_trigger_products_test_prohibition.png]
-- (Debe arrojar ERROR 1644: products_audit es inmutable: UPDATE prohibido)
UPDATE products_audit SET actionSale = 'DELETE' WHERE id = 1;


-- ==============================================================================
-- 3.0 TRIGGERS DE AUDITORÍA E INMUTABILIDAD EN TABLA: ORDERS
-- ==============================================================================

-- [Evidencia: Creación de Tabla Auditoría -> mysql_trigger_orders_audit_table.png]
DROP TABLE IF EXISTS orders_audit;
CREATE TABLE IF NOT EXISTS orders_audit (
  id              BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  order_id        BIGINT NOT NULL,
  actionSale      ENUM('UPDATE','DELETE','INSERT') NOT NULL DEFAULT 'INSERT',
  changed_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  changed_by      VARCHAR(255) NOT NULL DEFAULT 'Admin',
  before_data     JSON NULL,
  after_data      JSON NULL
) ENGINE=InnoDB;

-- [Evidencia: Trigger AFTER INSERT -> mysql_trigger_orders_after_insert.png]
DROP TRIGGER IF EXISTS ai_orders_audit;
DELIMITER //
CREATE TRIGGER ai_orders_audit AFTER INSERT ON orders FOR EACH ROW
BEGIN
  SET @from_orders_trigger = 1;
  INSERT INTO orders_audit (order_id, actionSale, before_data, after_data)
  VALUES (
    NEW.id, 'INSERT', NULL,
    JSON_OBJECT('id', NEW.id, 'customer_id', NEW.customer_id, 'channel', NEW.channel, 'total', NEW.total, 'status', NEW.status)
  );
  SET @from_orders_trigger = NULL;
END //
DELIMITER ;

-- [Evidencia: Trigger AFTER UPDATE -> mysql_trigger_orders_after_update.png]
DROP TRIGGER IF EXISTS au_orders_audit;
DELIMITER //
CREATE TRIGGER au_orders_audit AFTER UPDATE ON orders FOR EACH ROW
BEGIN
  SET @from_orders_trigger = 1;
  INSERT INTO orders_audit (order_id, actionSale, before_data, after_data)
  VALUES (
    NEW.id, 'UPDATE',
    JSON_OBJECT('id', OLD.id, 'customer_id', OLD.customer_id, 'channel', OLD.channel, 'total', OLD.total, 'status', OLD.status),
    JSON_OBJECT('id', NEW.id, 'customer_id', NEW.customer_id, 'channel', NEW.channel, 'total', NEW.total, 'status', NEW.status)
  );
  SET @from_orders_trigger = NULL;
END //
DELIMITER ;

-- [Evidencia: Trigger AFTER DELETE -> mysql_trigger_orders_after_delete.png]
DROP TRIGGER IF EXISTS ad_orders_audit;
DELIMITER //
CREATE TRIGGER ad_orders_audit AFTER DELETE ON orders FOR EACH ROW
BEGIN
  SET @from_orders_trigger = 1;
  INSERT INTO orders_audit (order_id, actionSale, before_data, after_data)
  VALUES (
    OLD.id, 'DELETE',
    JSON_OBJECT('id', OLD.id, 'customer_id', OLD.customer_id, 'channel', OLD.channel, 'total', OLD.total, 'status', OLD.status),
    NULL
  );
  SET @from_orders_trigger = NULL;
END //
DELIMITER ;

-- [Evidencia: Inmutabilidad BEFORE UPDATE -> mysql_trigger_orders_block_update.png]
DROP TRIGGER IF EXISTS bu_orders_audit_block;
DELIMITER //
CREATE TRIGGER bu_orders_audit_block BEFORE UPDATE ON orders_audit FOR EACH ROW
BEGIN
  SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'orders_audit es inmutable: UPDATE prohibido.';
END //
DELIMITER ;

-- [Evidencia: Inmutabilidad BEFORE DELETE -> mysql_trigger_orders_block_delete.png]
DROP TRIGGER IF EXISTS bd_orders_audit_block;
DELIMITER //
CREATE TRIGGER bd_orders_audit_block BEFORE DELETE ON orders_audit FOR EACH ROW
BEGIN
  SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'orders_audit es inmutable: DELETE prohibido.';
END //
DELIMITER ;

-- [Evidencia: Control BEFORE INSERT -> mysql_trigger_orders_guard_insert.png]
DROP TRIGGER IF EXISTS bi_orders_audit_guard;
DELIMITER //
CREATE TRIGGER bi_orders_audit_guard BEFORE INSERT ON orders_audit FOR EACH ROW
BEGIN
  IF @from_orders_trigger IS NULL OR @from_orders_trigger <> 1 THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'INSERT en orders_audit solo permitido desde triggers autorizados.';
  END IF;
END //
DELIMITER ;

-- PRUEBAS DE FUNCIONALIDAD ORDERS:
-- [Evidencia: Prueba Insertar -> mysql_trigger_orders_test_insert.png]
INSERT INTO orders (customer_id, cash_shift_id, channel, subtotal, total, status) 
VALUES (1, 1, 'pos', 20000.00, 20000.00, 'active');

-- [Evidencia: Prueba Modificar -> mysql_trigger_orders_test_update.png]
UPDATE orders SET total = 22000.00, subtotal = 22000.00 WHERE id = LAST_INSERT_ID();

-- [Evidencia: Prueba Prohibición Inmutabilidad -> mysql_trigger_orders_test_prohibition.png]
UPDATE orders_audit SET actionSale = 'DELETE' WHERE id = 1;


-- ==============================================================================
-- 4.0 TRIGGERS DE AUDITORÍA E INMUTABILIDAD EN TABLA: PAYMENTS
-- ==============================================================================

-- [Evidencia: Creación de Tabla Auditoría -> mysql_trigger_payments_audit_table.png]
DROP TABLE IF EXISTS payments_audit;
CREATE TABLE IF NOT EXISTS payments_audit (
  id              BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  payment_id      BIGINT NOT NULL,
  actionSale      ENUM('UPDATE','DELETE','INSERT') NOT NULL DEFAULT 'INSERT',
  changed_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  changed_by      VARCHAR(255) NOT NULL DEFAULT 'Admin',
  before_data     JSON NULL,
  after_data      JSON NULL
) ENGINE=InnoDB;

-- [Evidencia: Trigger AFTER INSERT -> mysql_trigger_payments_after_insert.png]
DROP TRIGGER IF EXISTS ai_payments_audit;
DELIMITER //
CREATE TRIGGER ai_payments_audit AFTER INSERT ON payments FOR EACH ROW
BEGIN
  SET @from_payments_trigger = 1;
  INSERT INTO payments_audit (payment_id, actionSale, before_data, after_data)
  VALUES (
    NEW.id, 'INSERT', NULL,
    JSON_OBJECT('id', NEW.id, 'reference_type', NEW.reference_type, 'reference_id', NEW.reference_id, 'method', NEW.method, 'amount', NEW.amount, 'status', NEW.status)
  );
  SET @from_payments_trigger = NULL;
END //
DELIMITER ;

-- [Evidencia: Trigger AFTER UPDATE -> mysql_trigger_payments_after_update.png]
DROP TRIGGER IF EXISTS au_payments_audit;
DELIMITER //
CREATE TRIGGER au_payments_audit AFTER UPDATE ON payments FOR EACH ROW
BEGIN
  SET @from_payments_trigger = 1;
  INSERT INTO payments_audit (payment_id, actionSale, before_data, after_data)
  VALUES (
    NEW.id, 'UPDATE',
    JSON_OBJECT('id', OLD.id, 'reference_type', OLD.reference_type, 'reference_id', OLD.reference_id, 'method', OLD.method, 'amount', OLD.amount, 'status', OLD.status),
    JSON_OBJECT('id', NEW.id, 'reference_type', NEW.reference_type, 'reference_id', NEW.reference_id, 'method', NEW.method, 'amount', NEW.amount, 'status', NEW.status)
  );
  SET @from_payments_trigger = NULL;
END //
DELIMITER ;

-- [Evidencia: Trigger AFTER DELETE -> mysql_trigger_payments_after_delete.png]
DROP TRIGGER IF EXISTS ad_payments_audit;
DELIMITER //
CREATE TRIGGER ad_payments_audit AFTER DELETE ON payments FOR EACH ROW
BEGIN
  SET @from_payments_trigger = 1;
  INSERT INTO payments_audit (payment_id, actionSale, before_data, after_data)
  VALUES (
    OLD.id, 'DELETE',
    JSON_OBJECT('id', OLD.id, 'reference_type', OLD.reference_type, 'reference_id', OLD.reference_id, 'method', OLD.method, 'amount', OLD.amount, 'status', OLD.status),
    NULL
  );
  SET @from_payments_trigger = NULL;
END //
DELIMITER ;

-- [Evidencia: Inmutabilidad BEFORE UPDATE -> mysql_trigger_payments_block_update.png]
DROP TRIGGER IF EXISTS bu_payments_audit_block;
DELIMITER //
CREATE TRIGGER bu_payments_audit_block BEFORE UPDATE ON payments_audit FOR EACH ROW
BEGIN
  SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'payments_audit es inmutable: UPDATE prohibido.';
END //
DELIMITER ;

-- [Evidencia: Inmutabilidad BEFORE DELETE -> mysql_trigger_payments_block_delete.png]
DROP TRIGGER IF EXISTS bd_payments_audit_block;
DELIMITER //
CREATE TRIGGER bd_payments_audit_block BEFORE DELETE ON payments_audit FOR EACH ROW
BEGIN
  SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'payments_audit es inmutable: DELETE prohibido.';
END //
DELIMITER ;

-- [Evidencia: Control BEFORE INSERT -> mysql_trigger_payments_guard_insert.png]
DROP TRIGGER IF EXISTS bi_payments_audit_guard;
DELIMITER //
CREATE TRIGGER bi_payments_audit_guard BEFORE INSERT ON payments_audit FOR EACH ROW
BEGIN
  IF @from_payments_trigger IS NULL OR @from_payments_trigger <> 1 THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'INSERT en payments_audit solo permitido desde triggers autorizados.';
  END IF;
END //
DELIMITER ;

-- PRUEBAS DE FUNCIONALIDAD PAYMENTS:
-- [Evidencia: Prueba Insertar -> mysql_trigger_payments_test_insert.png]
INSERT INTO payments (reference_type, reference_id, method, amount, status) 
VALUES ('order', 1, 'card', 22000.00, 'active');

-- [Evidencia: Prueba Modificar -> mysql_trigger_payments_test_update.png]
UPDATE payments SET amount = 23000.00 WHERE id = LAST_INSERT_ID();

-- [Evidencia: Prueba Prohibición Inmutabilidad -> mysql_trigger_payments_test_prohibition.png]
UPDATE payments_audit SET actionSale = 'DELETE' WHERE id = 1;
