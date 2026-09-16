-- ========================================================
-- BASE DE DATOS: tazanorte
-- MOTOR: MSSQL Server (DBeaver / SSMS)
-- ========================================================

-- 1. Customers
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

-- 2. Employees
CREATE TABLE employees (
    id BIGINT IDENTITY(1,1) PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    description VARCHAR(MAX),
    status VARCHAR(10) NOT NULL DEFAULT 'active',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_employees_status CHECK (status IN ('active', 'inactive'))
);

-- 3. Supplies
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

-- 4. Products
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

-- 5. RecipeSupplies
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

-- 6. CashShifts
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

-- 7. Orders
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

-- 8. OrderDetails
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

-- 9. Payments
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

-- 10. PointMovements
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
