# Financial Risk Management System
**College Problem-Based Learning (PBL) Project for Database Management Systems (DBMS) and Data Structures & Algorithms (DSA)**

---

## 📌 Project Overview
The **Financial Risk Management System** is a full-featured web application designed to monitor bank accounts, record and analyze financial transactions, execute explainable rule-based risk assessments, audit potential fraud incidents, and benchmark core manual DSA algorithms against financial datasets.

---

## 🛠️ Technology Stack
- **Frontend:** HTML5, CSS3 (Custom Financial Dashboard Theme: Navy Blue / Light Grey), JavaScript (Vanilla ES6), Chart.js
- **Backend:** Python 3, Flask Web Framework
- **Database:** MySQL 8.0 / MariaDB (Database: `financial_risk_db`) with PyMySQL & mysql-connector-python
- **Data Structures & Algorithms:** Manual Python implementations of Merge Sort, Quick Sort, Binary Search, Linear Search, and Hash Tables.

---

## 📂 Project Structure
```text
financial_risk_management_system/
│
├── app.py                      # Main Flask application and routing
├── database.py                 # MySQL database connection helpers & parameterized queries
├── schema.sql                  # Database creation, 4 relational tables, constraints & sample data
├── requirements.txt            # Python dependencies (Flask, PyMySQL, etc.)
├── .env.example                # Environment variable template
├── .env                        # Local database credentials configuration
├── README.md                   # Project documentation and PBL guide
│
├── algorithms/                 # Manual DSA Algorithm Implementations
│   ├── __init__.py             # Exports all algorithms
│   ├── merge_sort.py           # O(n log n) sorting by transaction amount
│   ├── quick_sort.py           # O(n log n) sorting by risk score (Lomuto partition)
│   ├── binary_search.py        # O(log n) transaction lookup by ID
│   ├── linear_search.py        # O(n) transaction lookup by keyword/description
│   └── hashing.py              # O(1) hash table lookup & duplicate ID detection
│
├── templates/                  # Jinja2 HTML Templates
│   ├── base.html               # Shared layout, sidebar navigation, top header & toasts
│   ├── index.html              # 1. Executive Dashboard with metrics & Chart.js
│   ├── accounts.html           # 2. Account Management (CRUD, filters & modals)
│   ├── transactions.html       # 3. Transaction Management (CRUD & risk evaluation)
│   ├── risk_assessment.html    # 4. Rule-Based Explainable Risk Assessment
│   ├── fraud_detection.html    # 5. Fraud Incident Auditing & Workflow Status
│   ├── reports.html            # 6. Aggregate Financial & Risk Reports
│   └── algorithms.html         # 7. Dedicated DSA Benchmark Sandbox
│
└── static/
    ├── css/
    │   └── style.css           # Professional responsive CSS styling
    └── js/
        └── script.js           # Client-side search, modals, toasts & DSA runner
```

---

## 📊 Database Design (4 Main Relational Tables)
1. **`Accounts`**: Stores account portfolios, holders, account numbers, and current balances.
2. **`Transactions`**: Stores financial inflow/outflow entries linked to accounts via `account_id` (Foreign Key).
3. **`Risk_Assessments`**: Stores calculated risk scores (0-100), risk levels (Low, Medium, High), and explainable reasons linked to transactions via `transaction_id` (Foreign Key).
4. **`Fraud_Incidents`**: Tracks flagged suspicious transactions requiring human review linked via `transaction_id` (Foreign Key).

---

## 🚀 Quick Start (Stage 1)

### 1. Install Dependencies
```bash
python -m pip install -r requirements.txt
```

### 2. Start the Flask Server
```bash
python app.py
```

### 3. Open in Browser
Visit [http://127.0.0.1:5000](http://127.0.0.1:5000) to view and test all 7 pages.
