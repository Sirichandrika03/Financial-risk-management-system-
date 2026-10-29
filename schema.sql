-- ========================================================
-- Financial Risk Management System (PBL)
-- Database Creation & Schema Setup Script
-- Database Name: financial_risk_db
-- ========================================================

CREATE DATABASE IF NOT EXISTS financial_risk_db;
USE financial_risk_db;

-- 1. Categories Table
-- Stores transaction categories and their base risk tier
CREATE TABLE IF NOT EXISTS categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(50) NOT NULL UNIQUE,
    category_type ENUM('INCOME', 'EXPENSE') NOT NULL,
    default_risk_level ENUM('LOW', 'MEDIUM', 'HIGH') NOT NULL DEFAULT 'LOW',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Transactions Table
-- Main ledger storing transactions, categorized with financial risk levels
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    amount DECIMAL(12, 2) NOT NULL,
    transaction_type ENUM('INCOME', 'EXPENSE') NOT NULL,
    category_id INT NOT NULL,
    risk_level ENUM('LOW', 'MEDIUM', 'HIGH') NOT NULL DEFAULT 'LOW',
    risk_score INT NOT NULL DEFAULT 0, -- Score from 0 to 100 based on risk rules
    description TEXT,
    transaction_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_transaction_category 
        FOREIGN KEY (category_id) REFERENCES categories(category_id)
        ON UPDATE CASCADE 
        ON DELETE RESTRICT
);

-- 3. Risk Audit Logs Table
-- Logs risk evaluations and manual/automated updates for governance
CREATE TABLE IF NOT EXISTS risk_audit_logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    transaction_id INT NOT NULL,
    previous_risk ENUM('LOW', 'MEDIUM', 'HIGH'),
    updated_risk ENUM('LOW', 'MEDIUM', 'HIGH') NOT NULL,
    reason VARCHAR(255) NOT NULL,
    logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_audit_transaction 
        FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id)
        ON UPDATE CASCADE 
        ON DELETE CASCADE
);
