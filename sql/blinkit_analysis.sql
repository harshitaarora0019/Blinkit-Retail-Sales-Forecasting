-- Create Database
CREATE DATABASE blinkit_db;
USE blinkit_db;

-- View Tables
SHOW TABLES;

-- Query used for forecasting dataset
SELECT
    order_date,
    order_total
FROM blinkit_orders;

-- Top Selling Products
SELECT
    p.product_name,
    SUM(oi.quantity) AS total_quantity
FROM blinkit_order_items oi
JOIN blinkit_products p
ON oi.product_id = p.product_id
GROUP BY p.product_name
ORDER BY total_quantity DESC;

-- Total Revenue
SELECT
    ROUND(SUM(order_total),2) AS total_revenue
FROM blinkit_orders;

-- Top Customers
SELECT
    c.customer_name,
    ROUND(SUM(o.order_total),2) AS total_spent
FROM blinkit_orders o
JOIN blinkit_customers c
ON o.customer_id = c.customer_id
GROUP BY c.customer_name
ORDER BY total_spent DESC;

-- Delivery Performance
SELECT
    delivery_status,
    COUNT(*) AS total_deliveries
FROM blinkit_delivery_performance
GROUP BY delivery_status;

-- Payment Method Analysis
SELECT
    payment_method,
    COUNT(*) AS total_orders
FROM blinkit_orders
GROUP BY payment_method;
