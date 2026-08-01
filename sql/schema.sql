CREATE DATABASE embedded_finance_analytics;

USE embedded_finance_analytics;
CREATE TABLE customers (
    customer_id VARCHAR(10) PRIMARY KEY,
    signup_date DATE,
    city VARCHAR(50),
    age_group VARCHAR(20),
    income_segment VARCHAR(20),
    acquisition_channel VARCHAR(30)
);
CREATE TABLE partners (
    partner_id VARCHAR(10) PRIMARY KEY,
    partner_name VARCHAR(100),
    industry VARCHAR(50)
);
CREATE TABLE products (
    product_id VARCHAR(10) PRIMARY KEY,
    product_name VARCHAR(100),
    category VARCHAR(50)
);
CREATE TABLE transactions (
    transaction_id VARCHAR(12) PRIMARY KEY,
    customer_id VARCHAR(10),
    partner_id VARCHAR(10),
    product_id VARCHAR(10),
    transaction_date DATE,
    amount DECIMAL(10,2),
    revenue DECIMAL(10,2),
    is_repeat VARCHAR(5),
    cross_sell VARCHAR(5),
    status VARCHAR(20),

    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (partner_id) REFERENCES partners(partner_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);
CREATE TABLE funnel_events (
    event_id VARCHAR(12) PRIMARY KEY,
    customer_id VARCHAR(10),
    product_id VARCHAR(10),
    stage VARCHAR(50),
    event_date DATE,

    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);