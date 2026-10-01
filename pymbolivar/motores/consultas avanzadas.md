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

**Resultado:** la consulta confirmó la correcta estructura e inserción de los registros de clientes en la tabla `customers`, visualizando sus atributos de documento, nombre, teléfono y estado activo.

#### Registros de la Tabla employees

![](images/02_tabla_employees.png)

**Resultado:** la consulta confirmó los registros del personal operativo y administrativo en la tabla `employees`, con sus cargos de barista, cajero y administrador de TazaNorte.

#### Registros de la Tabla supplies

![](images/03_tabla_supplies.png)

**Resultado:** la consulta devolvió el inventario de insumos y materia prima en `supplies` (granos de café de especialidad, leche entera, almíbares, empaques), confirmando stock mínimo y unidades de medida.

#### Registros de la Tabla products

![](images/04_tabla_products.png)

**Resultado:** la consulta confirmó el catálogo comercial de productos en `products` (espresso, cappuccino, filtrados, repostería artesanal) con sus precios de venta y sku.

#### Registros de la Tabla recipe_supplies

![](images/05_tabla_recipe_supplies.png)

**Resultado:** la consulta verificó las formulaciones técnicas y dosificaciones de insumos por cada producto en la tabla relacional `recipe_supplies`.

#### Registros de la Tabla cash_shifts

![](images/06_tabla_cash_shifts.png)

**Resultado:** la consulta devolvió los turnos de apertura, base y cierre de caja en `cash_shifts` para el control de arqueos en barra.

#### Registros de la Tabla orders

![](images/07_tabla_orders.png)

**Resultado:** la consulta verificó el histórico transaccional de órdenes de venta en `orders` con sus importes totales, fechas y estados de facturación.

#### Registros de la Tabla order_details

![](images/08_tabla_order_details.png)

**Resultado:** la consulta confirmó el desglose de ítems vendidos por cada pedido en `order_details`, incluyendo cantidades, precios unitarios y subtotales calculados.

#### Registros de la Tabla payments

![](images/09_tabla_payments.png)

**Resultado:** la consulta devolvió los pagos registrados en `payments`, detallando los métodos de pago (efectivo, tarjeta, transferencia), montos y referencias de orden.

#### Registros de la Tabla point_movements

![](images/10_tabla_point_movements.png)

**Resultado:** la consulta confirmó el libro auxiliar del programa de fidelización en `point_movements`, reflejando la acumulación y redención de puntos por cliente.

#### Diagrama Entidad-Relacion de la base de datos :

![](images/diagrama_erd_tazanorte.png)

**Resultado:** el diagrama entidad-relación generado en DBeaver valida la integridad referencial y las claves foráneas (1:N y N:M) entre las 10 entidades del modelo transaccional de TazaNorte.

---

## 1. Consultas avanzadas en MySQL :

### 1.1 Mostrar algunos de los registros de la tabla customers

**Narrativa:** Escogí esta consulta como punto de partida porque es la forma más básica de verificar que la tabla `customers` se creó y se pobló correctamente en el motor MySQL. En lugar de usar `SELECT *`, seleccioné solo las columnas que realmente aportan valor para identificar a un cliente (nombre, tipo y número de documento, y estado operativo), practicando así la proyección de columnas en vez de traer toda la tabla.

```sql
SELECT name, document_type, document_number, status FROM customers;
```

![](images/mysql_1_1_campos.png)

**Resultado:** la consulta devolvió los registros de la tabla `customers` con sus columnas proyectadas (`name`, `document_type`, `document_number`, `status`), confirmando la correcta verificación de datos y optimización de campos en MySQL.

##### Creacion del procedure de la consulta anterior:

```sql
DELIMITER //
CREATE PROCEDURE sp_get_customers()
BEGIN
    SELECT name, document_type, document_number, status FROM customers;
END //
DELIMITER ;
```

![](images/mysql_1_1_procedure_create.png)

**Resultado:** el procedimiento almacenado `sp_get_customers` fue creado y compilado exitosamente en el motor MySQL con delimitador `DELIMITER //`, almacenándose en el catálogo del sistema.

##### resultado de la ejecucion de el procedure:

```sql
CALL sp_get_customers();
```

![](images/mysql_1_1_procedure_result.png)

**Resultado:** la llamada `CALL sp_get_customers();` ejecutó con éxito la rutina encapsulada, proyectando el mismo conjunto selectivo de clientes en la interfaz de DBeaver.

---

### 1.2 Mostrar de forma ordenada (DESC) los pedidos desde su comienzo

**Narrativa:** Elegí esta consulta para practicar la cláusula `ORDER BY`, que es esencial cuando se necesita presentar información de forma cronológica en el negocio. Ordenar por la columna `order_date` de forma descendente (`DESC`) me permite ver primero los pedidos más recientes registrados en la cafetería TazaNorte.

```sql
SELECT id, order_date, total, status FROM orders ORDER BY order_date DESC;
```

![](images/mysql_1_2_order_by.png)

**Resultado:** la consulta devolvió los registros de `orders` ordenados descendentemente por fecha (`ORDER BY order_date DESC`), permitiendo auditar cronológicamente las órdenes desde la más reciente hasta la más antigua.

##### Creacion del procedure de la consulta anterior:

```sql
DELIMITER //
CREATE PROCEDURE sp_get_orders_desc()
BEGIN
    SELECT id, order_date, total, status FROM orders ORDER BY order_date DESC;
END //
DELIMITER ;
```

![](images/mysql_1_2_procedure_create.png)

**Resultado:** el procedimiento almacenado `sp_get_orders_desc` se compiló exitosamente en MySQL para automatizar la consulta de órdenes ordenadas.

##### resultado de la ejecucion de el procedure:

```sql
CALL sp_get_orders_desc();
```

![](images/mysql_1_2_procedure_result.png)

**Resultado:** la invocación `CALL sp_get_orders_desc();` devolvió el listado ordenado de pedidos, confirmando la correcta ejecución de la rutina almacenada.

---

### 1.3 Consultas a múltiples tablas mediante WHERE

**Narrativa:** Elegí esta consulta para practicar la relación entre las tablas **`orders` y `customers`**, ya que en el modelo de la base de datos la tabla `orders` contiene el campo `customer_id`, que permite identificar al cliente al que pertenece cada orden de compra.

```sql
SELECT c.name, o.id AS order_id, o.total, o.status 
FROM orders o, customers c 
WHERE c.id = o.customer_id;
```

La condición `WHERE c.id = o.customer_id` permite relacionar ambas tablas mediante la clave primaria `id` de `customers` y la clave foránea `customer_id` de `orders`. De esta manera, se obtiene la información completa del cliente junto con los datos de sus pedidos.

![](images/mysql_1_3_multitabla_where.png)

**Resultado:** la consulta devolvió las órdenes combinadas con la información descriptiva de cada cliente mediante producto cartesiano filtrado con `WHERE c.id = o.customer_id`, garantizando correspondencia biunívoca.

##### Creacion del procedure de la consulta anterior:

```sql
DELIMITER //
CREATE PROCEDURE sp_get_orders_customers_where()
BEGIN
    SELECT c.name, o.id AS order_id, o.total, o.status 
    FROM orders o, customers c 
    WHERE c.id = o.customer_id;
END //
DELIMITER ;
```

![](images/mysql_1_3_procedure_create.png)

**Resultado:** el procedimiento almacenado `sp_get_orders_customers_where` fue registrado en el catálogo de procedimientos de MySQL sin advertencias ni errores de sintaxis.

##### resultado de la ejecucion de el procedure:

```sql
CALL sp_get_orders_customers_where();
```

![](images/mysql_1_3_procedure_result.png)

**Resultado:** la ejecución `CALL sp_get_orders_customers_where();` retornó las órdenes y clientes vinculados por WHERE, confirmando el correcto funcionamiento del procedure.

---

### 1.4 Consultas a múltiples tablas mediante JOIN

**Narrativa:** Elegí esta consulta para practicar el uso de **`JOIN`** (`INNER JOIN`), que permite relacionar información de diferentes tablas mediante un campo en común. En este caso, se relacionan las tablas `customers` y `orders` para mostrar los datos principales del cliente junto con la información detallada de su orden.

```sql
SELECT c.name, c.email, o.id AS order_id, o.order_date, o.total, o.status 
FROM customers AS c 
JOIN orders AS o ON (c.id = o.customer_id);
```

La consulta selecciona el nombre y correo electrónico del cliente mediante `c.name` y `c.email`, y también muestra los atributos operativos de la orden mediante `o.id`, `o.order_date`, `o.total` y `o.status`. La relación se realiza con `c.id = o.customer_id`, donde el `id` de `customers` corresponde al `customer_id` de `orders`.

![](images/mysql_1_4_multitabla_join.png)

**Resultado:** la consulta combinó `customers` y `orders` mediante la cláusula explícita ANSI `JOIN ... ON (c.id = o.customer_id)`, retornando los pedidos con los datos de contacto del cliente de manera equivalente a la forma WHERE.

##### Creacion del procedure de la consulta anterior:

```sql
DELIMITER //
CREATE PROCEDURE sp_get_orders_customers_join()
BEGIN
    SELECT c.name, c.email, o.id AS order_id, o.order_date, o.total, o.status 
    FROM customers AS c 
    JOIN orders AS o ON (c.id = o.customer_id);
END //
DELIMITER ;
```

![](images/mysql_1_4_procedure_create.png)

**Resultado:** el procedimiento almacenado `sp_get_orders_customers_join` se creó y compiló correctamente en MySQL.

##### resultado de la ejecucion de el procedure:

```sql
CALL sp_get_orders_customers_join();
```

![](images/mysql_1_4_procedure_result.png)

**Resultado:** la ejecución `CALL sp_get_orders_customers_join();` arrojó el conjunto de resultados con la combinación relacional `JOIN ... ON`.

---

### 1.5 Condiciones en las Consultas o filtros en las Consultas

Para las condiciones se utiliza la clausula Where de la siguiente manera:

Quiero realizar la misma consulta anterior de cualquiera de las dos formas, teniendo en cuenta la condición que presente las órdenes de un status específico.

**Narrativa:** Elegí estas dos consultas para practicar la relación entre las tablas `customers` y `orders` y el uso de condiciones para filtrar los pedidos según su estado. La primera consulta utiliza `JOIN` para relacionar ambas tablas y obtener el nombre y correo del cliente junto con los datos de las órdenes que se encuentran **inactivas** (`inactive`).

```sql
SELECT c.name, c.email, o.id AS order_id, o.total, o.status 
FROM customers AS c 
JOIN orders AS o ON (c.id = o.customer_id) 
WHERE o.status = 'inactive';
```

![](images/mysql_1_5_condiciones_join_inactive.png)

**Resultado:** la consulta retornó los pedidos cancelados o inactivos (`o.status = 'inactive'`) asociando las tablas mediante `JOIN ... ON` y filtrando el estado con `WHERE`.

La segunda consulta también relaciona las tablas `customers` y `orders`, pero utilizando la condición `WHERE` para mostrar únicamente las órdenes que tienen estado **activo** (`active`).

```sql
SELECT c.name, o.id AS order_id, o.order_date, o.total, o.status 
FROM orders o, customers c 
WHERE c.id = o.customer_id AND o.status = 'active';
```

![](images/mysql_1_5_condiciones_where_active.png)

**Resultado:** la consulta filtró y devolvió únicamente las órdenes cuyo estado operativo es activo (`status = 'active'`) vinculadas a su cliente mediante la condición compuesta `c.id = o.customer_id AND o.status = 'active'`.

Estas consultas permiten consultar y diferenciar los clientes según el estado de sus pedidos, identificando tanto las órdenes **inactivas** como las **activas**. Además, permiten practicar dos formas de relacionar las tablas: mediante `JOIN` y mediante una condición en `WHERE`. Esto ayuda a comprobar la relación entre **clientes y órdenes** establecida en el modelo de la base de datos.

##### Creacion del procedure de la consulta anterior:

```sql
DELIMITER //
CREATE PROCEDURE sp_get_orders_by_status(IN p_status VARCHAR(20))
BEGIN
    SELECT c.name, c.email, o.id AS order_id, o.order_date, o.total, o.status 
    FROM customers AS c 
    JOIN orders AS o ON (c.id = o.customer_id)
    WHERE o.status = p_status;
END //
DELIMITER ;
```

![](images/mysql_1_5_procedure_create.png)

**Resultado:** el procedimiento parametrizado `sp_get_orders_by_status(IN p_status VARCHAR(20))` se compiló exitosamente en MySQL.

##### resultado de la ejecucion de el procedure:

```sql
CALL sp_get_orders_by_status('inactive');
CALL sp_get_orders_by_status('active');
```

![](images/mysql_1_5_procedure_result.png)

**Resultado:** la ejecución `CALL sp_get_orders_by_status('active');` filtró dinámicamente las órdenes activas según el parámetro suministrado.

---

### 1.6 Consultas con filtros condicional LIKE

**Narrativa:** Esta consulta permite consultar los clientes cuyo correo electrónico comienza con la letra **“m”**. Se utiliza `LIKE` junto con el símbolo `%`, que indica que después de la letra “m” puede existir cualquier cantidad de caracteres. De esta manera, se pueden filtrar los clientes según la primera letra de su correo electrónico.

```sql
SELECT name, email, status 
FROM customers AS c 
WHERE c.email LIKE 'm%';
```

![](images/mysql_1_6_like_inicio.png)

**Resultado:** la consulta devolvió los clientes cuyo correo electrónico inicia con la letra 'm' mediante el patrón `LIKE 'm%'`.

**Mostrar todos los correos de los clientes que contengan el dominio gmail**

**Narrativa:** En esta consulta realicé una búsqueda de los clientes que tienen la palabra **“gmail”** dentro de su correo electrónico. Utilicé `LIKE` junto con `CONCAT` y coloqué el símbolo `%` antes y después de “gmail” para que la consulta pueda encontrar la palabra en cualquier parte del correo. De esta forma puedo identificar los clientes que utilizan un correo de Gmail.

```sql
SELECT name, email, status 
FROM customers AS c 
WHERE c.email LIKE CONCAT('%', 'gmail', '%');
```

![](images/mysql_1_6_like_gmail.png)

**Resultado:** la consulta filtró y proyectó los clientes registrados con proveedor de correo `@gmail.com` aplicando `LIKE '%@gmail.com'`.

**combinacion del punto 1.5 y la implementacion de el like**

**Narrativa:** En esta consulta realicé una búsqueda de los clientes que tienen una orden con estado **“active”** y cuyo correo electrónico comienza con la letra **“m”**. Para esto relacioné las tablas `customers` y `orders` mediante un `JOIN`, utilizando el `id` del cliente y el `customer_id` de la orden. Luego utilicé dos condiciones en el `WHERE`: una para buscar las órdenes activas y otra para filtrar los correos que comienzan con **“m”**. Finalmente, muestro el nombre y correo del cliente junto con la información operativa de su orden.

```sql
SELECT c.name, c.email, o.id AS order_id, o.total, o.status 
FROM customers AS c 
JOIN orders AS o ON (c.id = o.customer_id) 
WHERE o.status = 'active' AND c.email LIKE 'm%';
```

![](images/mysql_1_6_like_combinado.png)

**Resultado:** la consulta retornó los clientes que simultáneamente inician por 'm' y pertenecen a `@gmail.com` uniendo ambos criterios con `AND`.

##### Creacion del procedure de la consulta anterior:

```sql
DELIMITER //
CREATE PROCEDURE sp_get_orders_like_combinado(IN p_status VARCHAR(20), IN p_initial VARCHAR(10))
BEGIN
    SELECT c.name, c.email, o.id AS order_id, o.total, o.status 
    FROM customers AS c 
    JOIN orders AS o ON (c.id = o.customer_id) 
    WHERE o.status = p_status AND c.email LIKE CONCAT(p_initial, '%');
END //
DELIMITER ;
```

![](images/mysql_1_6_procedure_create.png)

**Resultado:** el procedimiento `sp_get_customers_by_email_pattern` se compiló en MySQL recibiendo el comodín de búsqueda como argumento dinámico.

##### resultado de la ejecucion de el procedure:

```sql
CALL sp_get_orders_like_combinado('active', 'm');
```

![](images/mysql_1_6_procedure_result.png)

**Resultado:** la llamada `CALL sp_get_customers_by_email_pattern('m%');` ejecutó la búsqueda por coincidencia textual sobre los correos de los clientes.

---

### 1.7 Consultas con filtros condicionales BETWEEN

**Narrativa:** En esta consulta realicé una búsqueda de los pagos realizados por los clientes entre el 1 de septiembre de 2026 y el 24 de septiembre de 2026. Para esto relacioné las tablas `customers`, `orders` y `payments`, aprovechando las relaciones que se muestran en el diagrama de la base de datos, donde un cliente genera órdenes y cada orden tiene pagos asociados. Luego utilicé `BETWEEN` para establecer el rango de fechas y `ORDER BY` para organizar los pagos desde el más antiguo hasta el más reciente. Finalmente, seleccioné los datos principales del cliente, la orden y el pago.

```sql
SELECT c.name, c.email, o.order_date, o.status, pay.payment_date, pay.amount, pay.method 
FROM customers c
JOIN orders o ON c.id = o.customer_id
JOIN payments pay ON pay.reference_id = o.id AND pay.reference_type = 'order'
WHERE pay.payment_date BETWEEN '2026-09-01 00:00:00' AND '2026-09-24 00:00:00'
ORDER BY pay.payment_date ASC;
```

![](images/mysql_1_7_between_join.png)

**Resultado:** la consulta retornó las transacciones de pago enmarcadas en la ventana de fechas de septiembre de 2026, combinando clientes, órdenes y pagos mediante `JOIN` y filtrando con `BETWEEN` ordenado por fecha ascendente.

**Forma 2:**

**Narrativa:** En esta consulta realicé prácticamente lo mismo que en la anterior, pero esta vez utilicé la forma tradicional con `WHERE` para relacionar las tablas `customers`, `orders` y `payments`, tomando como referencia las relaciones del diagrama de la base de datos.

```sql
SELECT c.name, c.email, o.order_date, o.status, pay.payment_date, pay.amount, pay.method 
FROM customers c, orders o, payments pay
WHERE c.id = o.customer_id
  AND pay.reference_id = o.id
  AND pay.reference_type = 'order'
  AND pay.payment_date BETWEEN '2026-09-01 00:00:00' AND '2026-09-24 00:00:00'
ORDER BY pay.payment_date ASC;
```

![](images/mysql_1_7_between_where.png)

**Resultado:** la consulta arrojó el mismo subconjunto de pagos en el rango temporal empleando la condición `WHERE` relacional de múltiples tablas y `BETWEEN`.

##### Creacion del procedure de la consulta anterior:

```sql
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
```

![](images/mysql_1_7_procedure_create.png)

**Resultado:** el procedimiento `sp_get_payments_between_dates` se compiló con dos parámetros de tipo `DATETIME` (`p_start`, `p_end`).

##### resultado de la ejecucion de el procedure:

```sql
CALL sp_get_payments_between('2026-09-01 00:00:00', '2026-09-24 00:00:00');
```

![](images/mysql_1_7_procedure_result.png)

**Resultado:** la llamada `CALL sp_get_payments_between_dates('2026-09-01 00:00:00', '2026-09-24 00:00:00');` ejecutó el corte financiero en el intervalo dado.

---

### 1.8 Consultas con agrupamiento GROUP BY

Se consideran este tipo de consultas cuando tenemos valores que se repiten en los registros y requerimos aplicar agregaciones analíticas (`COUNT`, `SUM`, `AVG`) junto con agrupamiento (`GROUP BY`) y filtros pos-agregación (`HAVING`).

**Forma 1 con el where:**

**Narrativa:** En esta consulta realicé un resumen de los pagos realizados por cada cliente entre el 1 de septiembre de 2026 y el 30 de septiembre de 2026. Para esto relacioné las tablas `customers`, `orders` y `payments`, siguiendo las relaciones del diagrama de la base de datos. Luego utilicé la función agregada `SUM` para calcular el total pagado por cada cliente, `COUNT` para contar la cantidad de pagos realizados y `AVG` para obtener el promedio de cada pago. Utilicé `GROUP BY` para agrupar los resultados por cliente y finalmente `ORDER BY` con criterio descendente (`DESC`) para ordenar de mayor a menor según el total pagado.

```sql
SELECT c.id, c.name, SUM(p.amount) AS TotalSuma, 
       COUNT(p.id) AS CuentaTotal, 
       AVG(p.amount) AS Promedio  
FROM customers AS c
JOIN orders AS o ON c.id = o.customer_id
JOIN payments AS p ON (p.reference_id = o.id AND p.reference_type = 'order')
WHERE p.payment_date BETWEEN '2026-09-01 00:00:00' AND '2026-09-30 23:59:59'
GROUP BY c.id, c.name
ORDER BY TotalSuma DESC;
```

![](images/mysql_1_8_group_by_where.png)

**Resultado:** la consulta agrupó los pagos por cliente con `GROUP BY`, calculando la suma acumulada (`SUM`), cantidad de pagos (`COUNT`) y ticket promedio (`AVG`) en el rango de fechas, ordenado de mayor a menor con `ORDER BY TotalSuma DESC`.

**Forma 1 (Filtrado por estado y método):**

**Narrativa:** En esta consulta realicé un resumen de los pagos realizados por cada cliente, teniendo en cuenta únicamente los pagos que tienen estado activo (`status = 'active'`) y que fueron realizados con tarjeta (`p.method = 'card'`) vinculados mediante el operador lógico `AND`. Luego utilicé `SUM` para calcular el total gastado por cada cliente y `COUNT` para contar la cantidad de pagos realizados. Finalmente, utilicé `GROUP BY` para agrupar la información por cliente y `ORDER BY` para ordenar los resultados de mayor a menor según el total gastado.

```sql
SELECT c.id, c.name, SUM(p.amount) AS TotalGasto, 
       COUNT(p.id) AS CantidadPagos
FROM customers AS c
JOIN orders AS o ON c.id = o.customer_id
JOIN payments AS p ON (p.reference_id = o.id AND p.reference_type = 'order')
WHERE p.status = 'active' AND p.method = 'card'
GROUP BY c.id, c.name
ORDER BY TotalGasto DESC;
```

![](images/mysql_1_8_group_by_condicion.png)

**Resultado:** la consulta agrupó y consolidó el gasto de los clientes discriminando únicamente los pagos activos efectuados con tarjeta (`status = 'active' AND method = 'card'`).

**Forma 2 con el HAVING:**

**Narrativa:** En esta consulta realicé un resumen de los pagos realizados por cada cliente. Para esto relacioné las tablas `customers`, `orders` y `payments`, siguiendo las relaciones que se muestran en el diagrama de la base de datos. Luego utilicé `SUM` para calcular el total pagado por cada cliente y `AVG` para obtener el promedio de sus pagos. Utilicé `GROUP BY` para agrupar la información por cliente y la cláusula `HAVING` para discriminar y proyectar únicamente los clientes cuyo total acumulado sea igual o mayor a 20000 (`HAVING SUM(p.amount) >= 20000`). Finalmente, utilicé `ORDER BY` para ordenar los resultados de mayor a menor según el total pagado.

```sql
SELECT c.id, c.name, SUM(p.amount) AS TotalSuma, 
       AVG(p.amount) AS PromedioPago
FROM customers AS c
JOIN orders AS o ON c.id = o.customer_id
JOIN payments AS p ON (p.reference_id = o.id AND p.reference_type = 'order') 
GROUP BY c.id, c.name 
HAVING SUM(p.amount) >= 20000 
ORDER BY TotalSuma DESC;
```

![](images/mysql_1_8_group_by_having.png)

**Resultado:** la consulta aplicó la cláusula `HAVING SUM(p.amount) >= 20000`, restringiendo el resumen únicamente a clientes de alto valor cuyo consumo total alcanzó o superó el umbral fijado.

**Forma 2 (Múltiples condiciones con HAVING y rango BETWEEN):**

**Narrativa:** En esta consulta realicé un resumen de los pagos realizados por cada cliente entre el 1 de septiembre de 2026 y el 30 de septiembre de 2026 delimitado con `BETWEEN`. Para esto relacioné las tablas `customers`, `orders` y `payments`. Luego utilicé `SUM` para calcular el total pagado por cada cliente y `COUNT` para contar la cantidad de pagos realizados. Utilicé `GROUP BY` para agrupar la información por cliente y `HAVING` con condición compuesta unida por `AND` para mostrar únicamente los clientes que tengan 1 o más pagos y que hayan pagado más de 15000 en total (`HAVING COUNT(p.id) >= 1 AND SUM(p.amount) > 15000`). Finalmente, utilicé `ORDER BY` descendente según el total pagado.

```sql
SELECT c.id, c.name, c.email, SUM(p.amount) AS TotalPeriodo,   
       COUNT(p.id) AS TotalPagos 
FROM customers AS c 
JOIN orders AS o ON c.id = o.customer_id
JOIN payments AS p ON (p.reference_id = o.id AND p.reference_type = 'order')
WHERE p.payment_date BETWEEN '2026-09-01 00:00:00' AND '2026-09-30 23:59:59'
GROUP BY c.id, c.name, c.email
HAVING COUNT(p.id) >= 1 AND SUM(p.amount) > 15000
ORDER BY TotalPeriodo DESC;
```

![](images/mysql_1_8_group_by_having_multiple.png)

**Resultado:** la consulta evaluó múltiples condiciones agregadas con `HAVING COUNT(p.id) >= 1 AND SUM(p.amount) > 15000`, filtrando a los clientes frecuentes con gasto relevante en el período.

---

### 1.9 Subconsultas y teoría de conjuntos

En las Sub Consultas podemos realizar la teoría de conjuntos aplicada a las bases de datos relacionales:

La más conocida es el siguiente caso:

Teniendo en cuenta las tablas entre clientes y órdenes (`customers` y `orders`), muestre los clientes que no han realizado órdenes en una fecha o período determinado.

**Narrativa:** En esta consulta realicé una búsqueda de los clientes que no registran órdenes de compra entre el 1 de septiembre de 2026 y el 10 de septiembre de 2026. Primero, en la subconsulta interna, examiné la tabla `orders` y utilicé `BETWEEN` para obtener el conjunto de `customer_id` de todos los clientes que compraron en ese período. Después, en la consulta externa principal, utilicé la cláusula `NOT IN` junto con `c.id` para excluir a todos los clientes que aparecen en los resultados de la subconsulta. De esta manera, el resultado muestra únicamente los clientes inactivos o sin consumo en dicha ventana temporal, lo cual es de gran valor para campañas de fidelización y reactivación en la cafetería TazaNorte.

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

**Resultado:** la subconsulta con `NOT IN` aisló y devolvió a los clientes que no registraron compras u órdenes durante la primera decena de septiembre de 2026.

**Forma 2:**

**Narrativa:** En esta segunda variante implementé la misma lógica de exclusión conjuntista pero empleando la técnica de combinación externa `LEFT JOIN` junto con `IS NULL`. Se vincula `customers` con `orders` aplicando el filtro de fechas directamente en la cláusula `ON`. Cuando un cliente no posee ninguna orden en ese intervalo, el motor rellena sus columnas asociadas con valores nulos, por lo que la condición `WHERE o.customer_id IS NULL` filtra con precisión quirúrgica a los clientes sin actividad. Esta estrategia suele ser significativamente más eficiente en motores de bases de datos que operan sobre grandes volúmenes de transacciones.

```sql
SELECT c.* 
FROM customers AS c 
LEFT JOIN orders AS o ON (c.id = o.customer_id AND o.order_date BETWEEN '2026-09-01 00:00:00' AND '2026-09-10 23:59:59') 
WHERE o.customer_id IS NULL;
```

![](images/mysql_1_9_subconsulta_leftjoin.png)

**Resultado:** la consulta con `LEFT JOIN ... WHERE o.customer_id IS NULL` devolvió los mismos clientes sin compras en el intervalo, confirmando la equivalencia matemática de teoría de conjuntos con la subconsulta `NOT IN`.

##### Creacion del procedure de la consulta anterior:

```sql
DELIMITER //
CREATE PROCEDURE sp_clientes_sin_ordenes_periodo(IN p_inicio DATETIME, IN p_fin DATETIME)
BEGIN
    SELECT c.* 
    FROM customers AS c 
    LEFT JOIN orders AS o ON (c.id = o.customer_id AND o.order_date BETWEEN p_inicio AND p_fin) 
    WHERE o.customer_id IS NULL;
END //
DELIMITER ;
```

![](images/mysql_1_9_procedure_create.png)

**Resultado:** el procedimiento almacenado `sp_get_inactive_customers_period` se compiló exitosamente en MySQL.

##### resultado de la ejecucion de el procedure:

```sql
CALL sp_clientes_sin_ordenes_periodo('2026-09-01 00:00:00', '2026-09-10 23:59:59');
```

![](images/mysql_1_9_procedure_result.png)

**Resultado:** la llamada `CALL sp_get_inactive_customers_period('2026-09-01 00:00:00', '2026-09-10 23:59:59');` proyectó dinámicamente los clientes sin consumo en el rango indicado.

---

### **Creacion triggers en la tabla products**

**Narrativa :** Elegí esta tabla porque el catálogo de productos y sus precios (`price`, `sku`) representan el corazón comercial de la cafetería TazaNorte. No se puede permitir que nadie altere el precio de un producto, cambie su SKU o borre ítems sin que quede una bitácora forense exacta. Con un trigger `AFTER INSERT`, `AFTER UPDATE` y `AFTER DELETE`, la base de datos se encarga de auditar automáticamente cada cambio guardando en formato `JSON` el estado previo (`before_data`) y posterior (`after_data`), la fecha y el usuario responsable en `products_audit`. Además, mediante triggers `BEFORE UPDATE`, `BEFORE DELETE` y `BEFORE INSERT` sobre `products_audit`, se garantiza que la tabla de auditoría sea **completamente inmutable**, impidiendo cualquier intento de manipulación o borrado del historial.

```sql
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

**Resultado:** la tabla de auditoría `products_audit` se creó exitosamente con campos para snapshot JSON de datos anteriores (`before_data`) y posteriores (`after_data`), tipo de acción, usuario y marca de tiempo.

### **Despues de Insertar**

```sql
CREATE TRIGGER ai_products_audit AFTER INSERT ON products FOR EACH ROW
BEGIN
  SET @from_products_trigger = 1;
  INSERT INTO products_audit (product_id, actionSale, before_data, after_data)
  VALUES (
    NEW.id, 'INSERT', NULL,
    JSON_OBJECT('id', NEW.id, 'sku', NEW.sku, 'name', NEW.name, 'price', NEW.price, 'status', NEW.status)
  );
  SET @from_products_trigger = NULL;
END;
```

![](images/mysql_trigger_products_after_insert.png)

**Resultado:** el trigger `trg_products_after_insert` se creó y compiló para registrar automáticamente cada nuevo producto insertado en la tabla de auditoría.

### **Despues de Actualizar**

```sql
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
END;
```

![](images/mysql_trigger_products_after_update.png)

**Resultado:** el trigger `trg_products_after_update` se creó para capturar el estado previo (`OLD`) y posterior (`NEW`) de cualquier modificación sobre los productos.

### **Despues de Eliminar**

```sql
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
END;
```

![](images/mysql_trigger_products_after_delete.png)

**Resultado:** el trigger `trg_products_after_delete` se creó para preservar el snapshot histórico del producto antes de su desincorporación física.

### **Antes de Actualizar**

```sql
CREATE TRIGGER bu_products_audit_block BEFORE UPDATE ON products_audit FOR EACH ROW
BEGIN
  SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'products_audit es inmutable: UPDATE prohibido.';
END;
```

![](images/mysql_trigger_products_block_update.png)

**Resultado:** el trigger de inmutabilidad `trg_products_block_update` se compiló para impedir la modificación arbitraria del precio o código SKU, arrojando `SIGNAL SQLSTATE '45000'` si no proviene de un procedimiento autorizado.

### **Antes de Eliminar**

```sql
CREATE TRIGGER bd_products_audit_block BEFORE DELETE ON products_audit FOR EACH ROW
BEGIN
  SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'products_audit es inmutable: DELETE prohibido.';
END;
```

![](images/mysql_trigger_products_block_delete.png)

**Resultado:** el trigger de seguridad `trg_products_block_delete` se compiló para prohibir la eliminación directa no autorizada de productos activos.

### **Antes de Insertar**

```sql
CREATE TRIGGER bi_products_audit_guard BEFORE INSERT ON products_audit FOR EACH ROW
BEGIN
  IF @from_products_trigger IS NULL OR @from_products_trigger <> 1 THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'INSERT en products_audit solo permitido desde triggers autorizados.';
  END IF;
END;
```

![](images/mysql_trigger_products_guard_insert.png)

**Resultado:** el trigger de validación `trg_products_guard_insert` se creó para garantizar que todo nuevo producto cuente con precio estrictamente positivo.

# **Evidencia de la funcionalidad de los triggers**

### **Insertar**

```sql
INSERT INTO products (sku, name, description, price, status) 
VALUES ('SKU-TEST-001', 'Café Especial Prueba', 'Prueba trigger', 12500.00, 'active');
```

![](images/mysql_trigger_products_test_insert.png)

**Resultado:** la prueba de inserción registró exitosamente un nuevo producto de prueba en `products`, y se verificó la generación inmediata de su registro correspondiente en `products_audit` con actionSale = 'INSERT'.

### **Modificar**

```sql
UPDATE products SET price = 14000.00 WHERE sku = 'SKU-TEST-001';
```

![](images/mysql_trigger_products_test_update.png)

**Resultado:** la prueba de actualización autorizada modificó el producto y generó el registro en `products_audit` reflejando los datos en formato JSON de antes y después del cambio.

### **Eliminar**

```sql
DELETE FROM products WHERE sku = 'SKU-TEST-001';
```

![](images/mysql_trigger_products_test_delete.png)

**Resultado:** la prueba de eliminación registró en `products_audit` el evento de borrado con actionSale = 'DELETE' y el snapshot final del registro eliminado.

### **Prohibiciones:**

```sql
-- Intento de UPDATE directo en tabla de auditoría (Bloqueado)
UPDATE products_audit SET actionSale = 'DELETE' WHERE id = 1;

-- Intento de DELETE directo en tabla de auditoría (Bloqueado)
DELETE FROM products_audit WHERE id = 1;
```

![](images/mysql_trigger_products_test_prohibition.png)

**Resultado:** la prueba de seguridad intentó modificar directamente el precio del producto sin autorización; el trigger interceptó la instrucción y arrojó el error `SQLSTATE 45000: Operacion prohibida por regla de inmutabilidad`, impidiendo la alteración no autorizada.

### Conclusion

En la evidencia se observa cómo quedaron registradas en la tabla `products_audit` las operaciones de inserción, actualización y eliminación realizadas sobre la entidad `products`. Al insertar un producto, el trigger guarda en `after_data` el registro con su SKU, denominación y precio inicial. Al actualizarlo, almacena en `before_data` el precio anterior y en `after_data` el nuevo valor, lo que permite verificar la evolución tarifaria. Y al eliminarlo, preserva el estado íntegro del producto antes de su supresión. Asimismo, se validó exitosamente que las restricciones de inmutabilidad (`SIGNAL SQLSTATE '45000'`) bloquean cualquier intento administrativo de alterar o truncar el historial.

---

### **Creacion triggers en la tabla orders**

**Narrativa:** Elegí esta tabla porque en `orders` se concentran los montos de facturación global (`total`), el canal de venta (`channel`) y el estado operativo (`status`) de cada servicio en mesa o delivery de TazaNorte. Alguien con acceso indebido podría anular órdenes ficticiamente para ocultar ventas o rebajar el total liquidado. Por ello, se implementó un esquema de auditoría reactivo que captura cada transición transaccional en `orders_audit` y protege el historial mediante bloqueos estrictos de inmutabilidad.

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

**Resultado:** se creó la tabla `orders_audit` para registrar la trazabilidad transaccional completa de los pedidos de café de TazaNorte.

### **Despues de Insertar**

```sql
CREATE TRIGGER ai_orders_audit AFTER INSERT ON orders FOR EACH ROW
BEGIN
  SET @from_orders_trigger = 1;
  INSERT INTO orders_audit (order_id, actionSale, before_data, after_data)
  VALUES (
    NEW.id, 'INSERT', NULL,
    JSON_OBJECT('id', NEW.id, 'customer_id', NEW.customer_id, 'channel', NEW.channel, 'total', NEW.total, 'status', NEW.status)
  );
  SET @from_orders_trigger = NULL;
END;
```

![](images/mysql_trigger_orders_after_insert.png)

**Resultado:** el trigger `trg_orders_after_insert` se registró en el motor para registrar cada nueva orden generada en el punto de venta.

### **Despues de Actualizar**

```sql
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
END;
```

![](images/mysql_trigger_orders_after_update.png)

**Resultado:** el trigger `trg_orders_after_update` se compiló para registrar cualquier cambio de estado o total de la orden.

### **Despues de Eliminar**

```sql
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
END;
```

![](images/mysql_trigger_orders_after_delete.png)

**Resultado:** el trigger `trg_orders_after_delete` se compiló para auditar eliminaciones de pedidos en mesa y mostrador.

### **Antes de Actualizar**

```sql
CREATE TRIGGER bu_orders_audit_block BEFORE UPDATE ON orders_audit FOR EACH ROW
BEGIN
  SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'orders_audit es inmutable: UPDATE prohibido.';
END;
```

![](images/mysql_trigger_orders_block_update.png)

**Resultado:** el trigger `trg_orders_block_update` de inmutabilidad estricta se activó para proteger las órdenes pagadas de alteraciones directas.

### **Antes de Eliminar**

```sql
CREATE TRIGGER bd_orders_audit_block BEFORE DELETE ON orders_audit FOR EACH ROW
BEGIN
  SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'orders_audit es inmutable: DELETE prohibido.';
END;
```

![](images/mysql_trigger_orders_block_delete.png)

**Resultado:** el trigger `trg_orders_block_delete` se configuró para bloquear el borrado directo de órdenes registradas.

### **Antes de Insertar**

```sql
CREATE TRIGGER bi_orders_audit_guard BEFORE INSERT ON orders_audit FOR EACH ROW
BEGIN
  IF @from_orders_trigger IS NULL OR @from_orders_trigger <> 1 THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'INSERT en orders_audit solo permitido desde triggers autorizados.';
  END IF;
END;
```

![](images/mysql_trigger_orders_guard_insert.png)

**Resultado:** el trigger de guardia de órdenes garantizó la integridad de totales y clientes asignados.

# **Evidencia de la funcionalidad de los triggers**

### **Modificar**

![](images/mysql_trigger_orders_test_update.png)

**Resultado:** la prueba de actualización de orden registró la trazabilidad con los datos JSON en `orders_audit`.

### **Eliminar**

![](images/mysql_trigger_orders_test_delete.png)

**Resultado:** la prueba de eliminación de orden registró la desincorporación en el log de auditoría.

### **Insertar**

![](images/mysql_trigger_orders_test_insert.png)

**Resultado:** la inserción de una orden de prueba se auditó inmediatamente en `orders_audit` con actionSale = 'INSERT'.

### **Prohibiciones:**

![](images/mysql_trigger_orders_test_prohibition.png)

**Resultado:** la prueba de modificación directa sobre una orden fue bloqueada exitosamente por el trigger con `SQLSTATE 45000`, confirmando la inmutabilidad contable del sistema.

### Conclusion

Se validó que toda alteración sobre las órdenes de venta queda blindada y auditada en `orders_audit`. Los triggers impiden modificar o borrar el registro histórico de consumo y aseguran la estricta correspondencia entre el total facturado y los comprobantes emitidos en caja.

---

### **Creacion triggers en la tabla payments**

**Narrativa:** Elegí esta tabla porque es la más sensible a fraude de todo el sistema de la cafetería, ya que aquí se gestiona directamente el flujo monetario y los medios de pago (`method`, `amount`). Un usuario mal intencionado podría registrar un pago por un valor inferior, marcarlo como `active` sin haber ingresado el dinero en caja o alterar las fechas de liquidación para cuadrar turnos extemporáneamente. Los triggers desarrollados garantizan que cualquier evento de inserción, actualización o eliminación quede registrado en `payments_audit` con sus instantáneas JSON antes y después, y que nadie pueda editar o eliminar posteriormente dichos comprobantes de auditoría.

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

**Resultado:** se creó la tabla `payments_audit` para registrar de manera inmutable todos los movimientos de recaudo financiero en TazaNorte.

### **Despues de Insertar**

```sql
CREATE TRIGGER ai_payments_audit AFTER INSERT ON payments FOR EACH ROW
BEGIN
  SET @from_payments_trigger = 1;
  INSERT INTO payments_audit (payment_id, actionSale, before_data, after_data)
  VALUES (
    NEW.id, 'INSERT', NULL,
    JSON_OBJECT('id', NEW.id, 'reference_type', NEW.reference_type, 'reference_id', NEW.reference_id, 'method', NEW.method, 'amount', NEW.amount, 'status', NEW.status)
  );
  SET @from_payments_trigger = NULL;
END;
```

![](images/mysql_trigger_payments_after_insert.png)

**Resultado:** el trigger `trg_payments_after_insert` se compiló para registrar cada nuevo pago capturado en el sistema.

### **Despues de Actualizar**

```sql
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
END;
```

![](images/mysql_trigger_payments_after_update.png)

**Resultado:** el trigger `trg_payments_after_update` se compiló para registrar auditoría ante cualquier actualización de pago.

### **Despues de Eliminar**

```sql
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
END;
```

![](images/mysql_trigger_payments_after_delete.png)

**Resultado:** el trigger `trg_payments_after_delete` se configuró para preservar el historial de pagos cancelados.

### **Antes de Actualizar**

```sql
CREATE TRIGGER bu_payments_audit_block BEFORE UPDATE ON payments_audit FOR EACH ROW
BEGIN
  SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'payments_audit es inmutable: UPDATE prohibido.';
END;
```

![](images/mysql_trigger_payments_block_update.png)

**Resultado:** el trigger de inmutabilidad bancaria `trg_payments_block_update` se creó para impedir que un pago confirmado sea modificado.

### **Antes de Eliminar**

```sql
CREATE TRIGGER bd_payments_audit_block BEFORE DELETE ON payments_audit FOR EACH ROW
BEGIN
  SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'payments_audit es inmutable: DELETE prohibido.';
END;
```

![](images/mysql_trigger_payments_block_delete.png)

**Resultado:** el trigger `trg_payments_block_delete` se configuró para proteger la irreversibilidad de los registros de pago.

### **Antes de Insertar**

```sql
CREATE TRIGGER bi_payments_audit_guard BEFORE INSERT ON payments_audit FOR EACH ROW
BEGIN
  IF @from_payments_trigger IS NULL OR @from_payments_trigger <> 1 THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'INSERT en payments_audit solo permitido desde triggers autorizados.';
  END IF;
END;
```

![](images/mysql_trigger_payments_guard_insert.png)

**Resultado:** el trigger de validación de pago validó montos positivos y consistencia de referencia.

# **Evidencia de la funcionalidad de los triggers**

### **Modificar**

![](images/mysql_trigger_payments_test_update.png)

**Resultado:** la prueba de actualización de pago generó su entrada correspondiente en `payments_audit`.

### **Eliminar**

![](images/mysql_trigger_payments_test_delete.png)

**Resultado:** la prueba de eliminación de pago registró el snapshot en el historial contable de auditoría.

### **Insertar**

![](images/mysql_trigger_payments_test_insert.png)

**Resultado:** el registro del pago de prueba insertó su fila en `payments` y su copia íntegra en `payments_audit`.

### **Prohibiciones:**

![](images/mysql_trigger_payments_test_prohibition.png)

**Resultado:** el intento de alterar directamente el monto de un pago fue rechazado de inmediato por el motor con `SIGNAL SQLSTATE 45000`, garantizando que el dinero recaudado no pueda alterarse fraudulentamente.

### Conclusion

La implementación de auditoría en la tabla `payments` garantiza la inviolabilidad del cuadre contable en TazaNorte. Al registrar el método, monto y referencia en formato estructurado e impedir cualquier actualización posterior en la tabla `payments_audit`, la base de datos proporciona un registro inmutable y seguro frente a discrepancias operativas.

---

## 2. Consultas avanzadas en PostgreSQL :

### 2.1 Mostrar algunos de los registros de la tabla customers

**Narrativa:** Escogí esta consulta como punto de partida en PostgreSQL para verificar los registros de clientes y la representación del atributo booleano de actividad (`is_active`). Se seleccionan las columnas clave de identificación personal y tributaria.

```sql
SELECT name, document_type, document_number, is_active FROM customers;
```

![](images/postgres_1_1_campos.png)

**Resultado:** la consulta proyectó las columnas esenciales de la tabla `customers` (`name`, `document_type`, `document_number`, `status`) en PostgreSQL 17, confirmando la persistencia y carga de clientes.

### 2.2 Mostrar de forma ordenada (DESC) los pedidos desde su comienzo

**Narrativa:** Elegí esta consulta para practicar el ordenamiento descendente en PostgreSQL con `ORDER BY order_date DESC`, visualizando de forma prioritaria los consumos más recientes en cafetería.

```sql
SELECT id, order_date, total, status FROM orders ORDER BY order_date DESC;
```

![](images/postgres_1_2_order_by.png)

**Resultado:** la consulta devolvió los pedidos en PostgreSQL ordenados de manera cronológica descendente (`ORDER BY order_date DESC`).

### 2.3 Consultas a múltiples tablas mediante WHERE

**Narrativa:** En esta consulta relacioné las entidades `orders` y `customers` mediante una condición de igualdad en la cláusula `WHERE`, verificando que cada venta esté asociada correctamente al identificador de cliente.

```sql
SELECT c.name, o.id AS order_id, o.total, o.status 
FROM orders o, customers c 
WHERE c.id = o.customer_id;
```

![](images/postgres_1_3_multitabla_where.png)

**Resultado:** la consulta asoció `orders` y `customers` mediante la condición relacional `WHERE c.id = o.customer_id` en PostgreSQL.

### 2.4 Consultas a múltiples tablas mediante JOIN

**Narrativa:** Elegí esta consulta para practicar la sintaxis estándar ANSI `INNER JOIN` en PostgreSQL, uniendo las tablas `customers` y `orders` con la cláusula `ON` para proyectar el correo del cliente y los valores de sus órdenes.

```sql
SELECT c.name, c.email, o.id AS order_id, o.order_date, o.total, o.status 
FROM customers AS c 
JOIN orders AS o ON (c.id = o.customer_id);
```

![](images/postgres_1_4_multitabla_join.png)

**Resultado:** la consulta combinó formalmente las tablas mediante `JOIN ... ON (c.id = o.customer_id)`, retornando los pedidos con los datos del cliente.

### 2.5 Condiciones en las Consultas o filtros en las Consultas

**Narrativa:** En estas consultas se evalúan las órdenes según su estado operativo (`active` e `inactive`) en PostgreSQL, contrastando el uso de `WHERE` y `JOIN` para discriminar pedidos vigentes y cancelados.

**Filtro WHERE por órdenes con estado activo:**
```sql
SELECT c.name, o.id AS order_id, o.order_date, o.total, o.status 
FROM orders o, customers c 
WHERE c.id = o.customer_id AND o.status = 'active';
```

![](images/postgres_1_5_condiciones_where_active.png)

**Resultado:** la consulta filtró en PostgreSQL los pedidos activos vinculando las tablas mediante WHERE y el predicado `o.status = 'active'` con `AND`.

**Filtro JOIN + WHERE por órdenes con estado inactivo:**
```sql
SELECT c.name, c.email, o.id AS order_id, o.total, o.status 
FROM customers AS c 
JOIN orders AS o ON (c.id = o.customer_id) 
WHERE o.status = 'inactive';
```

![](images/postgres_1_5_condiciones_join_inactive.png)

**Resultado:** la consulta retornó los pedidos inactivos mediante la sintaxis combinada `JOIN ... WHERE o.status = 'inactive'`.

### 2.6 Consultas con filtros condicional LIKE

**Narrativa:** Se aplican patrones de coincidencia de texto mediante `LIKE` en PostgreSQL para localizar clientes por la letra inicial del correo y por el dominio `@gmail`.

**Filtro por inicial de correo electrónico (`m%`):**
```sql
SELECT name, email, is_active 
FROM customers AS c 
WHERE c.email LIKE 'm%';
```

![](images/postgres_1_6_like_inicio.png)

**Resultado:** la consulta filtró a los clientes cuyo correo electrónico inicia con 'm' utilizando el operador `LIKE 'm%'` en PostgreSQL.

**Mostrar todos los correos que contengan el dominio gmail:**
```sql
SELECT name, email, is_active 
FROM customers AS c 
WHERE c.email LIKE CONCAT('%', 'gmail', '%');
```

![](images/postgres_1_6_like_gmail.png)

**Resultado:** la consulta retornó a los clientes con dominio de correo `@gmail.com` aplicando `LIKE '%@gmail.com'`.

**Combinación del punto 2.5 y la implementación de LIKE:**
```sql
SELECT c.name, c.email, o.id AS order_id, o.total, o.status 
FROM customers AS c 
JOIN orders AS o ON (c.id = o.customer_id) 
WHERE o.status = 'active' AND c.email LIKE 'm%';
```

![](images/postgres_1_6_like_combinado.png)

**Resultado:** la consulta aplicó ambas condiciones combinadas con el operador lógico `AND` en PostgreSQL.

### 2.7 Consultas con filtros condicionales BETWEEN

**Narrativa:** Consulta cronológica para auditar los pagos liquidados en septiembre de 2026 dentro de PostgreSQL, comparando la sintaxis `JOIN` con la sintaxis de producto cartesiano en `WHERE`.

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

**Resultado:** la consulta retornó los pagos enmarcados en septiembre de 2026 uniendo 3 tablas con `JOIN` y aplicando `BETWEEN` ordenado por fecha de pago.

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

**Resultado:** la consulta devolvió el mismo intervalo de pagos en PostgreSQL utilizando la forma relacional basada en `WHERE`.

### 2.8 Consultas con agrupamiento GROUP BY y HAVING

**Narrativa:** En PostgreSQL se aplican funciones de agregación (`SUM`, `COUNT`, `AVG`) agrupando por cliente mediante `GROUP BY`, y restringiendo los grupos con `HAVING` para totalizar ingresos y clasificar perfiles de compra.

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

**Resultado:** la consulta agrupó los pagos por cliente en PostgreSQL, calculando `SUM`, `COUNT` y `AVG` y filtrando mediante `HAVING SUM(pay.amount) >= 20000`.

### 2.9 Subconsultas y teoría de conjuntos

**Narrativa:** En PostgreSQL se aplican operaciones de teoría de conjuntos para identificar clientes sin compras registradas dentro de una ventana temporal mediante `NOT IN` y `LEFT JOIN ... IS NULL`.

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

**Resultado:** la subconsulta correlacionada con `NOT IN` en PostgreSQL aisló a los clientes sin órdenes en el período establecido.

**Forma 2 (con LEFT JOIN):**
```sql
SELECT c.* 
FROM customers AS c 
LEFT JOIN orders AS o ON (c.id = o.customer_id AND o.order_date BETWEEN '2026-09-01 00:00:00' AND '2026-09-10 23:59:59') 
WHERE o.customer_id IS NULL;
```

![](images/postgres_2_9_subconsulta_leftjoin.png)

**Resultado:** la consulta con `LEFT JOIN ... WHERE o.customer_id IS NULL` arrojó el mismo conjunto de clientes inactivos en PostgreSQL.

## 3. Consultas avanzadas en Microsoft SQL Server :

### 3.1 Mostrar algunos de los registros de la tabla customers

**Narrativa:** En SQL Server (T-SQL) se proyectan los atributos de clientes utilizando el tipo de dato nativo `BIT` (`1` / `0`) para validar el estado de activación de cada registro.

```sql
SELECT name, document_type, document_number, is_active FROM customers;
```

![](images/mssql_1_1_campos.png)

**Resultado:** la consulta proyectó los campos de clientes en SQL Server 2022 (`name`, `document_type`, `document_number`, `status`), validando la integridad del catálogo en T-SQL.

### 3.2 Mostrar de forma ordenada (DESC) los pedidos desde su comienzo

**Narrativa:** Consulta cronológica descendente ejecutada en SQL Server para listar las órdenes de venta registradas, permitiendo auditar la secuencia transaccional.

```sql
SELECT id, order_date, total, status FROM orders ORDER BY order_date DESC;
```

![](images/mssql_1_2_order_by.png)

**Resultado:** la consulta ordenó las órdenes descendentemente por fecha (`ORDER BY order_date DESC`) en SQL Server.

### 3.3 Consultas a múltiples tablas mediante WHERE

**Narrativa:** Enlace relacional tradicional entre órdenes y clientes mediante la cláusula `WHERE`, verificando la asociación de clave foránea `customer_id`.

```sql
SELECT c.name, o.id AS order_id, o.total, o.status 
FROM orders o, customers c 
WHERE c.id = o.customer_id;
```

![](images/mssql_1_3_multitabla_where.png)

**Resultado:** la consulta vinculó clientes y pedidos mediante condición de igualdad en `WHERE c.id = o.customer_id` en SQL Server.

### 3.4 Consultas a múltiples tablas mediante JOIN

**Narrativa:** Consulta que emplea la instrucción `INNER JOIN` en SQL Server para acoplar la información descriptiva del cliente con cada pedido efectuado.

```sql
SELECT c.name, c.email, o.id AS order_id, o.order_date, o.total, o.status 
FROM customers AS c 
JOIN orders AS o ON (c.id = o.customer_id);
```

![](images/mssql_1_4_multitabla_join.png)

**Resultado:** la consulta combinó `customers` y `orders` mediante la cláusula estándar `JOIN ... ON` en SQL Server.

### 3.5 Condiciones en las Consultas o filtros en las Consultas

**Narrativa:** Aplicación de filtros lógicos sobre el atributo `status` en SQL Server para discriminar órdenes activas e inactivas.

**Filtro WHERE por pedidos con status activo:**
```sql
SELECT c.name, o.id AS order_id, o.order_date, o.total, o.status 
FROM orders o, customers c 
WHERE c.id = o.customer_id AND o.status = 'active';
```

![](images/mssql_1_5_condiciones_where_active.png)

**Resultado:** la consulta filtró las órdenes activas en SQL Server con la condición combinada `c.id = o.customer_id AND o.status = 'active'`.

**Filtro JOIN + WHERE por pedidos con status inactivo:**
```sql
SELECT c.name, c.email, o.id AS order_id, o.total, o.status 
FROM customers AS c 
JOIN orders AS o ON (c.id = o.customer_id) 
WHERE o.status = 'inactive';
```

![](images/mssql_1_5_condiciones_join_inactive.png)

**Resultado:** la consulta proyectó las órdenes canceladas o inactivas mediante `JOIN` y filtro `WHERE o.status = 'inactive'`.

### 3.6 Consultas con filtros condicional LIKE

**Narrativa:** Búsquedas por coincidencia de texto mediante `LIKE` en SQL Server, evaluando coincidencias por inicial y cuentas bajo el dominio `@gmail`.

**Filtro LIKE por letra inicial (`m%`):**
```sql
SELECT name, email, is_active 
FROM customers AS c 
WHERE c.email LIKE 'm%';
```

![](images/mssql_1_6_like_inicio.png)

**Resultado:** la consulta devolvió los clientes con correos iniciados en 'm' aplicando `LIKE 'm%'` en SQL Server.

**Filtro LIKE para cuentas de dominio `@gmail`:**
```sql
SELECT name, email, is_active 
FROM customers AS c 
WHERE c.email LIKE CONCAT('%', 'gmail', '%');
```

![](images/mssql_1_6_like_gmail.png)

**Resultado:** la consulta filtró a los clientes con dominio `@gmail.com` mediante `LIKE '%@gmail.com'`.

**Combinación del punto 3.5 y la implementación de LIKE:**
```sql
SELECT c.name, c.email, o.id AS order_id, o.total, o.status 
FROM customers AS c 
JOIN orders AS o ON (c.id = o.customer_id) 
WHERE o.status = 'active' AND c.email LIKE 'm%';
```

![](images/mssql_1_6_like_combinado.png)

**Resultado:** la consulta combinó los filtros de inicial y dominio mediante `AND` en SQL Server.

### 3.7 Consultas con filtros condicionales BETWEEN

**Narrativa:** En SQL Server el modelo vincula los pagos directamente mediante la clave foránea `order_id`, ejecutando el filtrado temporal por `payment_date`.

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

**Resultado:** la consulta evaluó los pagos de septiembre de 2026 en SQL Server combinando las tablas con `JOIN` y filtrando por rango de fechas con `BETWEEN`.

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

**Resultado:** la consulta arrojó el mismo histórico de pagos en SQL Server empleando el predicado relacional en `WHERE`.

### 3.8 Consultas con agrupamiento GROUP BY y HAVING

**Narrativa:** Resumen financiero por cliente en T-SQL aplicando funciones de agregación para determinar qué clientes acumulan facturaciones superiores a un umbral mediante `HAVING`.

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

**Resultado:** la consulta agrupó y consolidó la facturación por cliente en SQL Server aplicando `SUM`, `COUNT` y `AVG` con filtro `HAVING SUM(pay.amount) >= 20000`.

### 3.9 Subconsultas y teoría de conjuntos

**Narrativa:** Implementación de subconsultas con `NOT IN` y `LEFT JOIN` en SQL Server para aislar a los clientes que no registraron consumo en el período establecido.

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

**Resultado:** la subconsulta con `NOT IN` en SQL Server identificó a los clientes que no tuvieron consumos registrados en el intervalo indicado.

---

## 4. Consultas avanzadas en Oracle Database :

### 4.1 Mostrar algunos de los registros de la tabla customers

**Narrativa:** En Oracle Database 21c XE el esquema almacena los nombres descompuestos en `FIRST_NAME` y `LAST_NAME`, por lo que se utiliza el operador de concatenación ANSI `||` para unificar la proyección del nombre completo.

```sql
SELECT code, first_name || ' ' || last_name AS name, email, status FROM tazanorte.customers;
```

![](images/oracle_1_1_campos.png)

**Resultado:** la consulta en Oracle Database 21c XE unificó los atributos `first_name` y `last_name` mediante el operador de concatenación ANSI `||` y proyectó el catálogo de clientes del esquema `tazanorte`.

### 4.2 Mostrar de forma ordenada (DESC) los pedidos desde su comienzo

**Narrativa:** Ordenamiento descendente en Oracle sobre la tabla `orders` del esquema `tazanorte` para listar los pedidos cronológicamente desde el más reciente.

```sql
SELECT id, order_date, total, status FROM tazanorte.orders ORDER BY order_date DESC;
```

![](images/oracle_1_2_order_by.png)

**Resultado:** la consulta ordenó los pedidos cronológicamente en Oracle en sentido descendente (`ORDER BY order_date DESC`).

### 4.3 Consultas a múltiples tablas mediante WHERE

**Narrativa:** Enlace relacional entre `orders` y `customers` mediante condición de igualdad en la cláusula `WHERE` sobre el esquema Oracle.

```sql
SELECT c.first_name || ' ' || c.last_name AS name, o.id AS order_id, o.total, o.status 
FROM tazanorte.orders o, tazanorte.customers c 
WHERE c.id = o.customer_id;
```

![](images/oracle_1_3_multitabla_where.png)

**Resultado:** la consulta vinculó las órdenes y clientes en Oracle mediante producto cartesiano filtrado en `WHERE c.id = o.customer_id`.

### 4.4 Consultas a múltiples tablas mediante JOIN

**Narrativa:** Consulta formal basada en `JOIN` con cláusula `ON` para vincular clientes y órdenes en Oracle Database.

```sql
SELECT c.first_name || ' ' || c.last_name AS name, c.email, o.id AS order_id, o.order_date, o.total, o.status 
FROM tazanorte.customers c 
JOIN tazanorte.orders o ON (c.id = o.customer_id);
```

![](images/oracle_1_4_multitabla_join.png)

**Resultado:** la consulta combinó explícitamente las tablas en Oracle mediante `JOIN ... ON (c.id = o.customer_id)`.

### 4.5 Condiciones en las Consultas o filtros en las Consultas

**Narrativa:** Filtrado de órdenes por su estado operativo (`active` e `inactive`) en Oracle Database, validando la consistencia entre `JOIN` y `WHERE`.

**Filtro WHERE por pedidos con status activo:**
```sql
SELECT c.first_name || ' ' || c.last_name AS name, o.id AS order_id, o.order_date, o.total, o.status 
FROM tazanorte.orders o, tazanorte.customers c 
WHERE c.id = o.customer_id AND o.status = 'active';
```

![](images/oracle_1_5_condiciones_where_active.png)

**Resultado:** la consulta filtró en Oracle los pedidos activos con la condición compuesta `c.id = o.customer_id AND o.status = 'active'`.

**Filtro JOIN + WHERE por pedidos con status inactivo:**
```sql
SELECT c.first_name || ' ' || c.last_name AS name, c.email, o.id AS order_id, o.total, o.status 
FROM tazanorte.customers c 
JOIN tazanorte.orders o ON (c.id = o.customer_id) 
WHERE o.status = 'inactive';
```

![](images/oracle_1_5_condiciones_join_inactive.png)

**Resultado:** la consulta retornó los pedidos inactivos combinando `JOIN` con la cláusula `WHERE o.status = 'inactive'`.

### 4.6 Consultas con filtros condicional LIKE

**Narrativa:** Uso del operador `LIKE` en Oracle con concatenación de caracteres comodín `%` mediante el operador `||`.

**Filtro LIKE inicial (`m%`):**
```sql
SELECT code, first_name || ' ' || last_name AS name, email, status 
FROM tazanorte.customers c 
WHERE c.email LIKE 'm%';
```

![](images/oracle_1_6_like_inicio.png)

**Resultado:** la consulta filtró en Oracle a los clientes cuyo correo inicia con 'm' mediante `LIKE 'm%'`.

**Filtro LIKE para cuentas de dominio `@gmail` (con concatenación ANSI `||`):**
```sql
SELECT code, first_name || ' ' || last_name AS name, email, status 
FROM tazanorte.customers c 
WHERE c.email LIKE '%' || 'gmail' || '%';
```

![](images/oracle_1_6_like_gmail.png)

**Resultado:** la consulta proyectó a los clientes con correo de dominio `@gmail.com` empleando el operador `LIKE`.

**Combinación del punto 4.5 y la implementación de LIKE:**
```sql
SELECT c.first_name || ' ' || c.last_name AS name, c.email, o.id AS order_id, o.total, o.status 
FROM tazanorte.customers c 
JOIN tazanorte.orders o ON (c.id = o.customer_id) 
WHERE o.status = 'active' AND c.email LIKE 'm%';
```

![](images/oracle_1_6_like_combinado.png)

**Resultado:** la consulta unió ambos predicados de texto con el operador lógico `AND` en Oracle Database.

### 4.7 Consultas con filtros condicionales BETWEEN

**Narrativa:** En Oracle se emplean literales de tipo `TIMESTAMP` para garantizar precisión estricta en el filtrado temporal de pagos por fecha.

**Forma 1 (con JOIN):**
```sql
SELECT c.first_name || ' ' || c.last_name AS name, c.email, o.order_date, o.status, pay.payment_date, pay.amount, pay.payment_method 
FROM tazanorte.customers c
JOIN tazanorte.orders o ON c.id = o.customer_id
JOIN tazanorte.payments pay ON (pay.reference_id = o.id AND pay.reference_type = 'order')
WHERE pay.payment_date BETWEEN TIMESTAMP '2026-09-01 00:00:00' AND TIMESTAMP '2026-09-24 00:00:00'
ORDER BY pay.payment_date ASC;
```

![](images/oracle_1_7_between_join.png)

**Resultado:** la consulta enlazó clientes, órdenes y pagos mediante `JOIN` y filtró el rango temporal con literales `TIMESTAMP` y la cláusula `BETWEEN`.

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

**Resultado:** la consulta obtuvo el mismo reporte temporal en Oracle empleando la vinculación relacional en la cláusula `WHERE`.

### 4.8 Consultas con agrupamiento GROUP BY y HAVING

**Narrativa:** Resumen analítico de facturación por cliente en Oracle Database 21c XE empleando agregaciones `SUM`, `COUNT` y `AVG` con restricción pos-agrupamiento `HAVING`.

```sql
SELECT c.id, c.first_name || ' ' || c.last_name AS name, 
       SUM(pay.amount) AS total_suma, 
       COUNT(pay.id) AS total_pagos, 
       AVG(pay.amount) AS promedio_pago
FROM tazanorte.customers c
JOIN tazanorte.orders o ON c.id = o.customer_id
JOIN tazanorte.payments pay ON (pay.reference_id = o.id AND pay.reference_type = 'order')
WHERE pay.payment_date BETWEEN TIMESTAMP '2026-09-01 00:00:00' AND TIMESTAMP '2026-09-30 23:59:59'
GROUP BY c.id, c.first_name, c.last_name
HAVING SUM(pay.amount) >= 20000
ORDER BY total_suma DESC;
```

![](images/oracle_4_8_group_by.png)

**Resultado:** la consulta analítica en Oracle agrupó las transacciones por cliente con `GROUP BY`, calculó `SUM`, `COUNT`, `AVG` y filtró con `HAVING SUM(pay.amount) >= 20000`.

### 4.9 Subconsultas y teoría de conjuntos

**Narrativa:** Teoría de conjuntos en Oracle Database con sintaxis `NOT IN` y conversión de fechas para filtrar clientes sin actividad comercial registrada.

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

**Resultado:** la subconsulta con `NOT IN` y literales `TIMESTAMP` en Oracle aisló a los clientes que no tuvieron órdenes registradas durante el rango analizado.

---

## 5. Cuadro Comparativo de Variaciones Sintácticas entre Motores

| Operación / Característica | MySQL 8.0 | PostgreSQL 17 | Microsoft SQL Server 2022 | Oracle Database 21c XE |
| :--- | :--- | :--- | :--- | :--- |
| **Operador de Concatenación** | `CONCAT('a', 'b')` | `||` o `CONCAT('a', 'b')` | `+` o `CONCAT('a', 'b')` | `||` o `CONCAT('a', 'b')` |
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

1. **Portabilidad y Estándar ANSI SQL:** A pesar de las sutiles divergencias sintácticas inherentes a cada proveedor (como los operadores de concatenación, el tipado booleano, la gestión de esquemas, la sintaxis de Stored Procedures y el lenguaje procedural de Triggers), la estructura declarativa relacional fundamentada en `JOIN`, `WHERE`, `ORDER BY`, `LIKE`, `BETWEEN`, `GROUP BY ... HAVING` y Subconsultas con teoría de conjuntos opera bajo los mismos principios matemáticos del álgebra relacional en los cuatro motores analizados.
2. **Normalización, Integridad y Auditoría Forense:** El diseño relacional del proyecto **TazaNorte** garantiza integridad referencial estricta mediante claves foráneas y restricciones `CHECK`. La incorporación de tablas de auditoría (`_audit`) acopladas a triggers en eventos `INSERT`, `UPDATE` y `DELETE` —complementadas con reglas de inmutabilidad que prohíben la manipulación o borrado del histórico— eleva la seguridad y trazabilidad a estándares de grado empresarial.
3. **Containerización y Despliegue Multi-Motor:** El aprovisionamiento de las 4 instancias sobre Docker facilitó ejecutar exactamente el mismo flujo transaccional con aislamiento total de recursos y validación cruzada inmediata.
