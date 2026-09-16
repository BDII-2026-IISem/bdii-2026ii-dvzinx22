-- ========================================================
-- BASE DE DATOS / ESQUEMA: tazanorte
-- MOTOR: Oracle (DBeaver / SQL Developer)
-- ========================================================

-- 1. Customers
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

-- 2. Employees
CREATE TABLE employees (
    id NUMBER(19) GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR2(150) NOT NULL,
    description CLOB,
    status VARCHAR2(10) DEFAULT 'active' NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT chk_ora_employees_status CHECK (status IN ('active', 'inactive'))
);

-- 3. Supplies
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

-- 4. Products
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

-- 5. RecipeSupplies
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

-- 6. CashShifts
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

-- 7. Orders
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

-- 8. OrderDetails
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

-- 9. Payments
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

-- 10. PointMovements
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
