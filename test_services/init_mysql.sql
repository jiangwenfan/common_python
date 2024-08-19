-- 创建 customers 表
CREATE TABLE customers (
    customer_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);

-- 创建 orders 表，并建立外键关系
CREATE TABLE orders (
    order_id INT PRIMARY KEY AUTO_INCREMENT,
    order_date DATE NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    customer_id INT,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- 插入数据到 customers 表
INSERT INTO customers (customer_name, email) VALUES
('Alice Smith', 'alice@example.com'),
('Bob Johnson', 'bob@example.com'),
('Charlie Lee', 'charlie@example.com');

-- 插入数据到 orders 表
INSERT INTO orders (order_date, amount, customer_id) VALUES
('2024-08-01', 250.75, 1),
('2024-08-02', 100.00, 2),
('2024-08-03', 300.50, 3),
('2024-08-04', 150.00, 1),
('2024-08-05', 200.00, 2),
('2024-08-06', 175.25, 3);

-- 查询表中的数据以确认插入成功
SELECT * FROM customers;
SELECT * FROM orders;
