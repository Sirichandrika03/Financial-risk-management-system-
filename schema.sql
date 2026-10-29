-- =============================================================================
-- Financial Risk Management System
-- College Problem-Based Learning (PBL) Project for DBMS and DSA
-- Database Name: financial_risk_db
-- =============================================================================

-- 1. Create the Database
CREATE DATABASE IF NOT EXISTS financial_risk_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE financial_risk_db;

-- 2. Drop Tables if already existing (in reverse dependency order)
DROP TABLE IF EXISTS Fraud_Incidents;
DROP TABLE IF EXISTS Risk_Assessments;
DROP TABLE IF EXISTS Transactions;
DROP TABLE IF EXISTS Accounts;

-- =============================================================================
-- TABLE 1: Accounts
-- One account can have multiple transactions (1-to-Many relationship)
-- =============================================================================
CREATE TABLE Accounts (
    account_id INT AUTO_INCREMENT PRIMARY KEY,
    account_holder VARCHAR(100) NOT NULL,
    account_type VARCHAR(50) NOT NULL,
    account_number VARCHAR(50) NOT NULL UNIQUE,
    balance DECIMAL(15, 2) NOT NULL DEFAULT 0.00,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_account_type CHECK (account_type IN ('Savings', 'Checking', 'Business', 'Investment')),
    CONSTRAINT chk_positive_balance CHECK (balance >= 0.00)
) ENGINE=InnoDB;

-- =============================================================================
-- TABLE 2: Transactions
-- Belongs to one Account via foreign key account_id
-- =============================================================================
CREATE TABLE Transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    account_id INT NOT NULL,
    transaction_type VARCHAR(20) NOT NULL,
    amount DECIMAL(15, 2) NOT NULL,
    transaction_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    description VARCHAR(255) NOT NULL,
    transaction_status VARCHAR(30) NOT NULL DEFAULT 'Completed',
    CONSTRAINT fk_transactions_account FOREIGN KEY (account_id)
        REFERENCES Accounts (account_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    CONSTRAINT chk_tx_type CHECK (transaction_type IN ('Income', 'Expense')),
    CONSTRAINT chk_tx_status CHECK (transaction_status IN ('Completed', 'Pending', 'Failed')),
    CONSTRAINT chk_tx_amount CHECK (amount > 0.00)
) ENGINE=InnoDB;

-- =============================================================================
-- TABLE 3: Risk_Assessments
-- Linked to a Transaction via foreign key transaction_id
-- =============================================================================
CREATE TABLE Risk_Assessments (
    risk_id INT AUTO_INCREMENT PRIMARY KEY,
    transaction_id INT NOT NULL,
    risk_score INT NOT NULL,
    risk_level VARCHAR(20) NOT NULL,
    risk_reason VARCHAR(255) NOT NULL,
    assessment_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_risk_transaction FOREIGN KEY (transaction_id)
        REFERENCES Transactions (transaction_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT chk_risk_score CHECK (risk_score BETWEEN 0 AND 100),
    CONSTRAINT chk_risk_level CHECK (risk_level IN ('Low', 'Medium', 'High'))
) ENGINE=InnoDB;

-- =============================================================================
-- TABLE 4: Fraud_Incidents
-- Suspicious transaction escalated for compliance audit
-- =============================================================================
CREATE TABLE Fraud_Incidents (
    incident_id INT AUTO_INCREMENT PRIMARY KEY,
    transaction_id INT NOT NULL,
    fraud_type VARCHAR(100) NOT NULL,
    incident_description TEXT NOT NULL,
    incident_status VARCHAR(30) NOT NULL DEFAULT 'Open',
    reported_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_fraud_transaction FOREIGN KEY (transaction_id)
        REFERENCES Transactions (transaction_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT chk_incident_status CHECK (incident_status IN ('Open', 'Under Investigation', 'Resolved', 'False Positive'))
) ENGINE=InnoDB;

-- =============================================================================
-- SAMPLE DATA INSERTION (Educational Seeding)
-- =============================================================================

-- Accounts
INSERT INTO Accounts (account_holder, account_type, account_number, balance, created_at) VALUES
('Eleanor Vance', 'Savings', 'AC-100234', 14500.00, '2026-01-15 10:00:00'),
('David Sterling', 'Checking', 'AC-200456', 8200.50, '2026-01-18 11:30:00'),
('Apex Dynamics Corp', 'Business', 'AC-300789', 95400.00, '2026-02-01 09:15:00'),
('Maya Lin', 'Investment', 'AC-400912', 32000.75, '2026-02-10 14:20:00'),
('Marcus Brody', 'Checking', 'AC-500331', 4150.00, '2026-02-14 16:45:00');

-- Transactions
INSERT INTO Transactions (transaction_id, account_id, transaction_type, amount, transaction_date, description, transaction_status) VALUES
(101, 1, 'Income', 2500.00, '2026-03-01 09:10:00', 'Monthly Salary Direct Deposit', 'Completed'),
(102, 1, 'Expense', 120.00, '2026-03-02 12:45:00', 'Local Grocery Mart', 'Completed'),
(103, 2, 'Expense', 6800.00, '2026-03-03 14:22:00', 'Rapid International Wire Transfer', 'Completed'),
(104, 3, 'Income', 45000.00, '2026-03-04 10:00:00', 'Client Milestone Retainer Payment', 'Completed'),
(105, 3, 'Expense', 8500.00, '2026-03-05 16:30:00', 'Bulk Equipment Purchase Overseas', 'Pending'),
(106, 4, 'Expense', 12000.00, '2026-03-06 18:00:00', 'Crypto Exchange Arbitrage Outflow', 'Failed'),
(107, 5, 'Expense', 3900.00, '2026-03-07 11:15:00', 'Sudden High-Volume Cash Withdrawal', 'Completed');

-- Risk Assessments (Rule-based evaluation)
INSERT INTO Risk_Assessments (transaction_id, risk_score, risk_level, risk_reason, assessment_date) VALUES
(101, 15, 'Low', 'Standard regular payroll deposit matching historical profile', '2026-03-01 09:10:05'),
(102, 10, 'Low', 'Routine merchant expense well below threshold', '2026-03-02 12:45:02'),
(103, 85, 'High', 'Transaction amount exceeds $5,000 threshold and consumes >80% account balance', '2026-03-03 14:22:10'),
(104, 25, 'Low', 'Commercial business account standard customer revenue', '2026-03-04 10:00:04'),
(105, 55, 'Medium', 'Amount exceeds $5,000 threshold; overseas payee pending clearance', '2026-03-05 16:30:12'),
(106, 92, 'High', 'Transaction failed after large outflow attempt; potential unauthorized credential drain', '2026-03-06 18:00:08'),
(107, 60, 'Medium', 'Single cash withdrawal represents 94% of checking portfolio balance', '2026-03-07 11:15:09');

-- Fraud Incidents (Compliance review tickets)
INSERT INTO Fraud_Incidents (transaction_id, fraud_type, incident_description, incident_status, reported_date) VALUES
(103, 'Unusual High Value Spike', 'Rapid international wire of $6,800 triggered high-risk audit score (85/100). Customer identity verification requested.', 'Under Investigation', '2026-03-03 14:30:00'),
(106, 'Repeated Transaction Failures', 'Failed crypto outflow of $12,000 flagged for credential stuffing audit. Account placed on temporary security hold.', 'Open', '2026-03-06 18:15:00');

-- =============================================================================
-- DEMONSTRATION QUERIES FOR DBMS VIVA / EXAMINATION
-- =============================================================================

-- A. INNER JOIN: Combine Accounts and Transactions
-- SELECT a.account_holder, a.account_number, t.transaction_id, t.amount, t.transaction_type, t.transaction_date
-- FROM Accounts a
-- INNER JOIN Transactions t ON a.account_id = t.account_id;

-- B. LEFT JOIN: Combine Transactions with Risk Assessments & Fraud Incidents
-- SELECT t.transaction_id, a.account_holder, t.amount, r.risk_score, r.risk_level, f.incident_status
-- FROM Transactions t
-- JOIN Accounts a ON t.account_id = a.account_id
-- LEFT JOIN Risk_Assessments r ON t.transaction_id = r.transaction_id
-- LEFT JOIN Fraud_Incidents f ON t.transaction_id = f.transaction_id;

-- C. AGGREGATE QUERY: Financial Summary without row inflation
-- SELECT 
--     a.account_id, 
--     a.account_holder, 
--     COUNT(t.transaction_id) AS total_txns,
--     COALESCE(SUM(CASE WHEN t.transaction_type = 'Income' THEN t.amount ELSE 0 END), 0) AS total_income,
--     COALESCE(SUM(CASE WHEN t.transaction_type = 'Expense' THEN t.amount ELSE 0 END), 0) AS total_expense
-- FROM Accounts a
-- LEFT JOIN Transactions t ON a.account_id = t.account_id
-- GROUP BY a.account_id, a.account_holder;
