-- ========================================================
-- Financial Risk Management System (PBL)
-- Essential DBMS Queries for Evaluation & Workbench Testing
-- ========================================================

USE financial_risk_db;

-- --------------------------------------------------------
-- 1. SEARCH TRANSACTIONS
-- --------------------------------------------------------
-- Search transaction by specific ID (demonstrates primary key lookup)
SELECT * FROM transactions WHERE transaction_id = 5;

-- Search transactions by Risk Level (e.g., HIGH risk)
SELECT * FROM transactions WHERE risk_level = 'HIGH';

-- Search transactions within a specific amount range
SELECT * FROM transactions WHERE amount BETWEEN 20000 AND 100000;


-- --------------------------------------------------------
-- 2. UPDATE TRANSACTION
-- --------------------------------------------------------
-- Example: Manually reassessing and updating risk score & risk level
UPDATE transactions 
SET risk_level = 'HIGH', risk_score = 90, description = CONCAT(description, ' [Flagged after manual audit]')
WHERE transaction_id = 7;

-- Record this change into the audit log
INSERT INTO risk_audit_logs (transaction_id, previous_risk, updated_risk, reason)
VALUES (7, 'MEDIUM', 'HIGH', 'Manual compliance audit escalated due to high single purchase value');


-- --------------------------------------------------------
-- 3. DELETE TRANSACTION
-- --------------------------------------------------------
-- Delete a temporary or cancelled transaction
-- (Audit logs with CASCADE delete will be cleaned up automatically)
DELETE FROM transactions WHERE transaction_id = 12;


-- --------------------------------------------------------
-- 4. JOIN QUERIES
-- --------------------------------------------------------
-- INNER JOIN: Fetch complete transaction details along with human-readable category name
SELECT 
    t.transaction_id,
    t.title,
    t.amount,
    t.transaction_type,
    c.category_name,
    t.risk_level,
    t.risk_score,
    t.transaction_date
FROM transactions t
INNER JOIN categories c ON t.category_id = c.category_id
ORDER BY t.transaction_date DESC;

-- LEFT JOIN with Audit Logs: Show transactions and any recorded risk adjustments
SELECT 
    t.transaction_id,
    t.title,
    t.risk_level AS current_risk,
    a.previous_risk,
    a.reason AS audit_reason,
    a.logged_at
FROM transactions t
LEFT JOIN risk_audit_logs a ON t.transaction_id = a.transaction_id;


-- --------------------------------------------------------
-- 5. GROUP BY & AGGREGATE QUERIES (Dashboard Analytics)
-- --------------------------------------------------------
-- A. Income vs Expense Summary
SELECT 
    transaction_type,
    COUNT(*) AS total_count,
    SUM(amount) AS total_amount,
    AVG(amount) AS average_amount
FROM transactions
GROUP BY transaction_type;

-- B. Risk Level Distribution (Count and Total Exposure)
SELECT 
    risk_level,
    COUNT(*) AS transaction_count,
    SUM(amount) AS total_exposure_amount,
    ROUND(AVG(risk_score), 1) AS avg_risk_score
FROM transactions
GROUP BY risk_level
ORDER BY FIELD(risk_level, 'HIGH', 'MEDIUM', 'LOW');

-- C. Category-wise Spending / Inflow Breakdown
SELECT 
    c.category_name,
    t.transaction_type,
    COUNT(t.transaction_id) AS transaction_count,
    SUM(t.amount) AS total_value
FROM categories c
JOIN transactions t ON c.category_id = t.category_id
GROUP BY c.category_name, t.transaction_type
ORDER BY total_value DESC;
