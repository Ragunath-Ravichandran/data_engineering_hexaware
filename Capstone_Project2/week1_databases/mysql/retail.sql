CREATE DATABASE IF NOT EXISTS retail_dashboard;
USE retail_dashboard;


CREATE TABLE stores (
    store_id    INT AUTO_INCREMENT PRIMARY KEY,
    store_name  VARCHAR(100) NOT NULL,
    city        VARCHAR(50),
    region      VARCHAR(50)  NOT NULL,
    opened_date DATE
);

CREATE TABLE products (
    product_id   INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category     VARCHAR(50),
    price        DECIMAL(10,2) NOT NULL,
    cost         DECIMAL(10,2) NOT NULL
);

CREATE TABLE employees (
    employee_id INT AUTO_INCREMENT PRIMARY KEY,
    store_id    INT NOT NULL,
    full_name   VARCHAR(100) NOT NULL,
    role        VARCHAR(50),
    hire_date   DATE,
    FOREIGN KEY (store_id) REFERENCES stores(store_id)
);

CREATE TABLE sales (
    sale_id     INT AUTO_INCREMENT PRIMARY KEY,
    store_id    INT NOT NULL,
    product_id  INT NOT NULL,
    employee_id INT,
    sale_date   DATE NOT NULL,
    quantity    INT NOT NULL,
    unit_price  DECIMAL(10,2) NOT NULL,
    discount    DECIMAL(5,2) DEFAULT 0,      
    returned    BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (store_id)    REFERENCES stores(store_id),
    FOREIGN KEY (product_id)  REFERENCES products(product_id),
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
);


CREATE INDEX idx_products_name    ON products(product_name);
CREATE INDEX idx_products_cat     ON products(category);
CREATE INDEX idx_stores_region    ON stores(region);
CREATE INDEX idx_sales_product    ON sales(product_id);
CREATE INDEX idx_sales_store_date ON sales(store_id, sale_date);


INSERT INTO stores (store_name, city, region, opened_date) VALUES
('Anna Nagar Store', 'Chennai',   'South', '2019-05-10'),
('T Nagar Store',    'Chennai',   'South', '2018-02-20'),
('Whitefield Store', 'Bengaluru', 'South', '2020-08-15'),
('Andheri Store',    'Mumbai',    'West',  '2017-11-01');

INSERT INTO products (product_name, category, price, cost) VALUES
('Wireless Mouse',   'Electronics', 799.00,  450.00),
('Bluetooth Speaker','Electronics', 2499.00, 1600.00),
('Cotton T-Shirt',   'Apparel',     499.00,  220.00),
('Running Shoes',    'Footwear',    3299.00, 2100.00),
('Water Bottle',     'Home',        349.00,  150.00);

INSERT INTO employees (store_id, full_name, role, hire_date) VALUES
(1, 'Suresh Babu',  'Store Manager', '2019-06-01'),
(1, 'Lakshmi N',    'Sales Associate','2021-03-12'),
(2, 'Ramesh K',     'Store Manager', '2018-03-01'),
(3, 'Anitha R',     'Sales Associate','2022-01-17'),
(4, 'Vikram S',     'Store Manager', '2017-12-01');

INSERT INTO sales (store_id, product_id, employee_id, sale_date, quantity, unit_price, discount, returned) VALUES
(1, 1, 2, '2025-01-06', 10, 799.00,  5.00,  FALSE),
(1, 3, 2, '2025-01-06', 25, 499.00,  10.00, FALSE),
(1, 4, 1, '2025-01-06', 4,  3299.00, 0.00,  TRUE),
(2, 2, 3, '2025-01-06', 6,  2499.00, 0.00,  FALSE),
(2, 5, 3, '2025-01-07', 30, 349.00,  15.00, FALSE),
(3, 1, 4, '2025-01-07', 8,  799.00,  0.00,  FALSE),
(3, 4, 4, '2025-01-07', 2,  3299.00, 5.00,  TRUE),
(4, 3, 5, '2025-01-08', 40, 499.00,  20.00, FALSE),
(4, 2, 5, '2025-01-08', 3,  2499.00, 0.00,  FALSE);


SELECT * FROM sales WHERE store_id = 1;

SELECT s.sale_id, st.store_name, p.product_name, s.quantity,
       (s.quantity * s.unit_price) AS gross_amount
FROM sales s
JOIN stores   st ON st.store_id   = s.store_id
JOIN products p  ON p.product_id  = s.product_id;

SELECT st.region, p.product_name, SUM(s.quantity) AS units_sold
FROM sales s
JOIN stores st   ON st.store_id  = s.store_id
JOIN products p  ON p.product_id = s.product_id
GROUP BY st.region, p.product_name;


UPDATE products SET price = 849.00 WHERE product_id = 1;
UPDATE sales    SET returned = TRUE WHERE sale_id = 5;


DELETE FROM sales WHERE sale_id = 9;

DROP PROCEDURE IF EXISTS calc_daily_sales;

DELIMITER //
CREATE PROCEDURE calc_daily_sales(
    IN p_store_id  INT,
    IN p_sale_date DATE
)
BEGIN
    SELECT
        st.store_id,
        st.store_name,
        p_sale_date AS sale_date,
        COUNT(s.sale_id)                                              AS total_transactions,
        COALESCE(SUM(s.quantity), 0)                                  AS total_units_sold,
        COALESCE(ROUND(SUM(s.quantity * s.unit_price * (1 - s.discount/100)), 2), 0) AS total_sales_amount
    FROM stores st
    LEFT JOIN sales s
           ON s.store_id  = st.store_id
          AND s.sale_date = p_sale_date
          AND s.returned  = FALSE
    WHERE st.store_id = p_store_id
    GROUP BY st.store_id, st.store_name;
END //
DELIMITER ;


CALL calc_daily_sales(1, '2025-01-06');
CALL calc_daily_sales(4, '2025-01-08');
