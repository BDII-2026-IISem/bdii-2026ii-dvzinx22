-- ========================================================
-- BASE DE DATOS: tazanorte
-- MOTOR: PostgreSQL (DBeaver)
-- ========================================================

-- 1. Customers
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

-- 2. Employees
CREATE TABLE employees (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    description TEXT,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 3. Supplies
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

-- 4. Products
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

-- 5. RecipeSupplies
CREATE TABLE recipe_supplies (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    product_id BIGINT NOT NULL,
    supply_id BIGINT NOT NULL,
    quantity NUMERIC(15,3) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_recipe_supplies_product FOREIGN KEY (product_id) REFERENCES products(id),
    CONSTRAINT fk_recipe_supplies_supply FOREIGN KEY (supply_id) REFERENCES supplies(id),
    CONSTRAINT uq_pg_product_supply UNIQUE (product_id, supply_id)
);

-- 6. CashShifts
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
    CONSTRAINT fk_cash_shifts_employee FOREIGN KEY (employee_id) REFERENCES employees(id)
);

-- 7. Orders
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
    CONSTRAINT fk_orders_customer FOREIGN KEY (customer_id) REFERENCES customers(id),
    CONSTRAINT fk_orders_cash_shift FOREIGN KEY (cash_shift_id) REFERENCES cash_shifts(id)
);

-- 8. OrderDetails
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
    CONSTRAINT fk_order_details_order FOREIGN KEY (order_id) REFERENCES orders(id),
    CONSTRAINT fk_order_details_product FOREIGN KEY (product_id) REFERENCES products(id)
);

-- 9. Payments
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

-- 10. PointMovements
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
    CONSTRAINT fk_point_movements_customer FOREIGN KEY (customer_id) REFERENCES customers(id),
    CONSTRAINT fk_point_movements_order FOREIGN KEY (order_id) REFERENCES orders(id)
);
