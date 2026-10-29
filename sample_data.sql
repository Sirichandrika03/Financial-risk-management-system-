-- ========================================================
-- Financial Risk Management System (PBL)
-- Sample Data Insertion Script
-- ========================================================

USE financial_risk_db;

-- Clear previous data in correct order to respect foreign key constraints
DELETE FROM risk_audit_logs;
DELETE FROM transactions;
DELETE FROM categories;

-- Reset Auto Increment values
ALTER TABLE categories AUTO_INCREMENT = 1;
ALTER TABLE transactions AUTO_INCREMENT = 1;
ALTER TABLE risk_audit_logs AUTO_INCREMENT = 1;

-- 1. Insert Categories
INSERT INTO categories (category_name, category_type, default_risk_level) VALUES
('Salary', 'INCOME', 'LOW'),
('Consulting / Freelance', 'INCOME', 'MEDIUM'),
('Crypto Returns', 'INCOME', 'HIGH'),
('Office Rent', 'EXPENSE', 'LOW'),
('Utilities & Bills', 'EXPENSE', 'LOW'),
('Groceries & Supplies', 'EXPENSE', 'LOW'),
('Marketing & Ads', 'EXPENSE', 'MEDIUM'),
('Hardware Equipment', 'EXPENSE', 'MEDIUM'),
('Unverified Wire Transfer', 'EXPENSE', 'HIGH'),
('Speculative Derivatives', 'EXPENSE', 'HIGH');

-- 2. Insert Realistic Transactions
INSERT INTO transactions (title, amount, transaction_type, category_id, risk_level, risk_score, description, transaction_date) VALUES
('Monthly Corporate Salary', 85000.00, 'INCOME', 1, 'LOW', 10, 'Standard monthly salary credit via direct deposit', '2026-10-01'),
('Office Space Rent', 28000.00, 'EXPENSE', 4, 'LOW', 15, 'Monthly commercial lease payment for main office', '2026-10-02'),
('Electricity & Water Bill', 4200.00, 'EXPENSE', 5, 'LOW', 5, 'Municipal utility bill settlement', '2026-10-03'),
('Grocery Store Vendor', 6500.00, 'EXPENSE', 6, 'LOW', 10, 'Pantry supplies and weekly groceries', '2026-10-04'),
('Freelance UI/UX Project', 32000.00, 'INCOME', 2, 'MEDIUM', 45, 'Payment received for design consultation', '2026-10-06'),
('Digital Ad Campaign', 18500.00, 'EXPENSE', 7, 'MEDIUM', 50, 'Social media targeted customer acquisition campaign', '2026-10-08'),
('High-Spec Workstations', 145000.00, 'EXPENSE', 8, 'MEDIUM', 60, 'Purchased 2 developer laptops and monitors', '2026-10-10'),
('Overseas Crypto Arbitrage', 210000.00, 'INCOME', 3, 'HIGH', 88, 'Large lump sum transfer from unregulated offshore exchange', '2026-10-12'),
('Unverified Vendor Payment', 175000.00, 'EXPENSE', 9, 'HIGH', 92, 'Urgent offshore invoice payment lacking PO approval', '2026-10-15'),
('High Leverage Derivative Trade', 95000.00, 'EXPENSE', 10, 'HIGH', 85, 'Margin account allocation for option volatility hedge', '2026-10-18'),
('Consulting Retainer Fee', 45000.00, 'INCOME', 2, 'MEDIUM', 40, 'Bi-weekly business strategy retainer', '2026-10-20'),
('Cloud Server Infrastructure', 12500.00, 'EXPENSE', 5, 'LOW', 20, 'Monthly AWS cloud hosting infrastructure fee', '2026-10-22');

-- 3. Insert Initial Audit Logs
INSERT INTO risk_audit_logs (transaction_id, previous_risk, updated_risk, reason) VALUES
(8, 'MEDIUM', 'HIGH', 'Transaction exceeds INR 2,00,000 threshold from non-banking channel'),
(9, 'MEDIUM', 'HIGH', 'Flagged by automated rule: overseas recipient not in verified whitelist');
