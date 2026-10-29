"""
Financial Risk Management System
=================================
Flask Web Application for College Problem-Based Learning (PBL) Project
Integrating MySQL Database Management (DBMS) with Data Structures & Algorithms (DSA).
"""

import os
import time
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from dotenv import load_dotenv

# Import manual DSA algorithm implementations
from algorithms import (
    merge_sort,
    quick_sort,
    binary_search,
    linear_search,
    TransactionHashTable,
    find_duplicate_ids
)

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'college-pbl-financial-risk-secret-key-2026')

# ------------------------------------------------------------------------------
# REUSABLE CURRENCY FORMATTING (Indian Numbering System / INR en-IN)
# ------------------------------------------------------------------------------
def format_inr(number, include_symbol=True):
    """
    Formats a numeric value using the Indian numbering system (en-IN),
    e.g. ₹1,000.00, ₹25,500.50, ₹1,00,000.00, ₹10,00,000.00.
    Pure Python implementation with no external dependencies.
    """
    if number is None:
        return f"{'₹' if include_symbol else ''}0.00"
    try:
        val = float(number)
    except (ValueError, TypeError):
        return f"{'₹' if include_symbol else ''}0.00"

    is_negative = val < 0
    val = abs(val)

    # Format with two decimal places
    parts = f"{val:.2f}".split('.')
    integer_part = parts[0]
    decimal_part = parts[1]

    # Indian numbering: last 3 digits, then groups of 2 digits
    if len(integer_part) > 3:
        last_three = integer_part[-3:]
        remaining = integer_part[:-3]
        grouped = []
        while remaining:
            grouped.append(remaining[-2:])
            remaining = remaining[:-2]
        grouped.reverse()
        formatted_int = ",".join(grouped) + "," + last_three
    else:
        formatted_int = integer_part

    prefix = "₹" if include_symbol else ""
    sign = "-" if is_negative else ""
    return f"{sign}{prefix}{formatted_int}.{decimal_part}"


@app.template_filter('format_inr')
def jinja_format_inr(value, include_symbol=True):
    return format_inr(value, include_symbol=include_symbol)


@app.context_processor
def utility_processor():
    return dict(format_inr=format_inr)


# ------------------------------------------------------------------------------
# IN-MEMORY SAMPLE DATASET (Used for Stage 1 Testing & Seamless Fallback)
# In Stages 2-7, database.py connects to live MySQL financial_risk_db
# ------------------------------------------------------------------------------
sample_accounts = [
    {'account_id': 1, 'account_holder': 'Eleanor Vance', 'account_type': 'Savings', 'account_number': 'AC-100234', 'balance': 14500.00, 'created_at': '2026-01-15 10:00:00'},
    {'account_id': 2, 'account_holder': 'David Sterling', 'account_type': 'Checking', 'account_number': 'AC-200456', 'balance': 8200.50, 'created_at': '2026-01-18 11:30:00'},
    {'account_id': 3, 'account_holder': 'Apex Dynamics Corp', 'account_type': 'Business', 'account_number': 'AC-300789', 'balance': 95400.00, 'created_at': '2026-02-01 09:15:00'},
    {'account_id': 4, 'account_holder': 'Maya Lin', 'account_type': 'Investment', 'account_number': 'AC-400912', 'balance': 32000.75, 'created_at': '2026-02-10 14:20:00'},
    {'account_id': 5, 'account_holder': 'Marcus Brody', 'account_type': 'Checking', 'account_number': 'AC-500331', 'balance': 4150.00, 'created_at': '2026-02-14 16:45:00'}
]

sample_transactions = [
    {'transaction_id': 101, 'account_id': 1, 'account_holder': 'Eleanor Vance', 'transaction_type': 'Income', 'amount': 2500.00, 'transaction_date': '2026-03-01 09:10:00', 'description': 'Monthly Salary Direct Deposit', 'transaction_status': 'Completed', 'risk_score': 15, 'risk_level': 'Low'},
    {'transaction_id': 102, 'account_id': 1, 'account_holder': 'Eleanor Vance', 'transaction_type': 'Expense', 'amount': 120.00, 'transaction_date': '2026-03-02 12:45:00', 'description': 'Local Grocery Mart', 'transaction_status': 'Completed', 'risk_score': 10, 'risk_level': 'Low'},
    {'transaction_id': 103, 'account_id': 2, 'account_holder': 'David Sterling', 'transaction_type': 'Expense', 'amount': 6800.00, 'transaction_date': '2026-03-03 14:22:00', 'description': 'Rapid International Wire Transfer', 'transaction_status': 'Completed', 'risk_score': 85, 'risk_level': 'High'},
    {'transaction_id': 104, 'account_id': 3, 'account_holder': 'Apex Dynamics Corp', 'transaction_type': 'Income', 'amount': 45000.00, 'transaction_date': '2026-03-04 10:00:00', 'description': 'Client Milestone Retainer Payment', 'transaction_status': 'Completed', 'risk_score': 25, 'risk_level': 'Low'},
    {'transaction_id': 105, 'account_id': 3, 'account_holder': 'Apex Dynamics Corp', 'transaction_type': 'Expense', 'amount': 8500.00, 'transaction_date': '2026-03-05 16:30:00', 'description': 'Bulk Equipment Purchase Overseas', 'transaction_status': 'Pending', 'risk_score': 55, 'risk_level': 'Medium'},
    {'transaction_id': 106, 'account_id': 4, 'account_holder': 'Maya Lin', 'transaction_type': 'Expense', 'amount': 12000.00, 'transaction_date': '2026-03-06 18:00:00', 'description': 'Crypto Exchange Arbitrage Outflow', 'transaction_status': 'Failed', 'risk_score': 92, 'risk_level': 'High'},
    {'transaction_id': 107, 'account_id': 5, 'account_holder': 'Marcus Brody', 'transaction_type': 'Expense', 'amount': 3900.00, 'transaction_date': '2026-03-07 11:15:00', 'description': 'Sudden High-Volume Cash Withdrawal', 'transaction_status': 'Completed', 'risk_score': 60, 'risk_level': 'Medium'}
]

sample_risk_assessments = [
    {'risk_id': 1, 'transaction_id': 101, 'account_holder': 'Eleanor Vance', 'amount': 2500.00, 'risk_score': 15, 'risk_level': 'Low', 'risk_reason': 'Standard regular payroll deposit matching historical profile', 'assessment_date': '2026-03-01 09:10:05'},
    {'risk_id': 2, 'transaction_id': 102, 'account_holder': 'Eleanor Vance', 'amount': 120.00, 'risk_score': 10, 'risk_level': 'Low', 'risk_reason': 'Routine merchant expense well below threshold', 'assessment_date': '2026-03-02 12:45:02'},
    {'risk_id': 3, 'transaction_id': 103, 'account_holder': 'David Sterling', 'amount': 6800.00, 'risk_score': 85, 'risk_level': 'High', 'risk_reason': 'Transaction amount exceeds ₹5,000 threshold and consumes >80% account balance', 'assessment_date': '2026-03-03 14:22:10'},
    {'risk_id': 4, 'transaction_id': 104, 'account_holder': 'Apex Dynamics Corp', 'amount': 45000.00, 'risk_score': 25, 'risk_level': 'Low', 'risk_reason': 'Commercial business account standard customer revenue', 'assessment_date': '2026-03-04 10:00:04'},
    {'risk_id': 5, 'transaction_id': 105, 'account_holder': 'Apex Dynamics Corp', 'amount': 8500.00, 'risk_score': 55, 'risk_level': 'Medium', 'risk_reason': 'Amount exceeds ₹5,000 threshold; overseas payee pending clearance', 'assessment_date': '2026-03-05 16:30:12'},
    {'risk_id': 6, 'transaction_id': 106, 'account_holder': 'Maya Lin', 'amount': 12000.00, 'risk_score': 92, 'risk_level': 'High', 'risk_reason': 'Transaction failed after large outflow attempt; potential unauthorized credential drain', 'assessment_date': '2026-03-06 18:00:08'},
    {'risk_id': 7, 'transaction_id': 107, 'account_holder': 'Marcus Brody', 'amount': 3900.00, 'risk_score': 60, 'risk_level': 'Medium', 'risk_reason': 'Single cash withdrawal represents 94% of checking portfolio balance', 'assessment_date': '2026-03-07 11:15:09'}
]

sample_fraud_incidents = [
    {'incident_id': 1, 'transaction_id': 103, 'account_holder': 'David Sterling', 'fraud_type': 'Unusual High Value Spike', 'incident_description': 'Rapid international wire of ₹6,800 triggered high-risk audit score (85/100). Customer identity verification requested.', 'incident_status': 'Under Investigation', 'reported_date': '2026-03-03 14:30:00'},
    {'incident_id': 2, 'transaction_id': 106, 'account_holder': 'Maya Lin', 'fraud_type': 'Repeated Transaction Failures', 'incident_description': 'Failed crypto outflow of ₹12,000 flagged for credential stuffing audit. Account placed on temporary security hold.', 'incident_status': 'Open', 'reported_date': '2026-03-06 18:15:00'}
]

# ------------------------------------------------------------------------------
# RULE-BASED RISK SCORING HELPER (Explainable Educational Engine)
# ------------------------------------------------------------------------------
def evaluate_transaction_risk(amount, status, account_balance=10000.0):
    """
    Computes an illustrative, explainable risk score (0-100) and reason.
    - Low Risk:    0 - 29
    - Medium Risk: 30 - 69
    - High Risk:   70 - 100
    """
    score = 10
    reasons = []

    # Rule 1: High-value threshold (₹5,000)
    if amount > 10000:
        score += 50
        reasons.append("Amount significantly exceeds ₹10,000 large-transaction mark")
    elif amount > 5000:
        score += 35
        reasons.append("Amount exceeds ₹5,000 compliance monitoring threshold")

    # Rule 2: High proportion of account balance
    if account_balance > 0 and (amount / account_balance) > 0.75:
        score += 25
        reasons.append("Transaction consumes >75% of available account balance")

    # Rule 3: Transaction status
    if status == 'Failed':
        score += 35
        reasons.append("Transaction failed during execution")
    elif status == 'Pending':
        score += 10
        reasons.append("Transaction is currently awaiting settlement")

    # Clamp score to 0 - 100
    final_score = min(100, max(0, score))

    if final_score >= 70:
        level = 'High'
    elif final_score >= 30:
        level = 'Medium'
    else:
        level = 'Low'

    reason_text = "; ".join(reasons) if reasons else "Routine transaction matching standard profile"
    return final_score, level, reason_text


# ------------------------------------------------------------------------------
# PAGE ROUTES
# ------------------------------------------------------------------------------

@app.route('/')
def index():
    """1. Dashboard Page"""
    total_accounts = len(sample_accounts)
    total_transactions = len(sample_transactions)
    total_volume = sum(float(tx['amount']) for tx in sample_transactions)
    total_income = sum(float(tx['amount']) for tx in sample_transactions if tx['transaction_type'] == 'Income')
    total_expenses = sum(float(tx['amount']) for tx in sample_transactions if tx['transaction_type'] == 'Expense')
    
    low_risk = sum(1 for tx in sample_transactions if tx.get('risk_level') == 'Low')
    med_risk = sum(1 for tx in sample_transactions if tx.get('risk_level') == 'Medium')
    high_risk = sum(1 for tx in sample_transactions if tx.get('risk_level') == 'High')
    open_incidents = sum(1 for inc in sample_fraud_incidents if inc['incident_status'] in ['Open', 'Under Investigation'])

    stats = {
        'total_accounts': total_accounts,
        'total_transactions': total_transactions,
        'total_volume': total_volume,
        'total_income': total_income,
        'total_expenses': total_expenses,
        'low_risk_count': low_risk,
        'med_risk_count': med_risk,
        'high_risk_count': high_risk,
        'open_incidents': open_incidents
    }

    # Latest transactions for dashboard table
    recent = list(reversed(sample_transactions))[:5]
    return render_template('index.html', active_page='dashboard', stats=stats, recent_transactions=recent)


@app.route('/accounts')
def accounts_page():
    """2. Account Management Page"""
    return render_template('accounts.html', active_page='accounts', accounts=sample_accounts)


@app.route('/transactions')
def transactions_page():
    """3. Transaction Management Page"""
    return render_template('transactions.html', active_page='transactions', transactions=sample_transactions, accounts=sample_accounts)


@app.route('/risk-assessment')
def risk_assessment_page():
    """4. Risk Assessment Page"""
    return render_template('risk_assessment.html', active_page='risk_assessment', risk_assessments=sample_risk_assessments)


@app.route('/fraud-detection')
def fraud_detection_page():
    """5. Fraud Detection Page"""
    return render_template('fraud_detection.html', active_page='fraud_detection', fraud_incidents=sample_fraud_incidents)


@app.route('/reports')
def reports_page():
    """6. Reports Page with SQL-like Aggregates"""
    total_income = sum(float(tx['amount']) for tx in sample_transactions if tx['transaction_type'] == 'Income')
    total_expenses = sum(float(tx['amount']) for tx in sample_transactions if tx['transaction_type'] == 'Expense')
    income_tx_count = sum(1 for tx in sample_transactions if tx['transaction_type'] == 'Income')
    expense_tx_count = sum(1 for tx in sample_transactions if tx['transaction_type'] == 'Expense')
    high_risk_count = sum(1 for tx in sample_transactions if tx.get('risk_level') == 'High')
    total_tx = len(sample_transactions) or 1
    high_risk_pct = round((high_risk_count / total_tx) * 100, 1)

    report_summary = {
        'total_income': total_income,
        'total_expenses': total_expenses,
        'income_tx_count': income_tx_count,
        'expense_tx_count': expense_tx_count,
        'net_balance': total_income - total_expenses,
        'high_risk_percentage': high_risk_pct
    }

    # Portfolio-level breakdown
    account_reports = []
    chart_labels = []
    chart_data = []
    for acc in sample_accounts:
        acc_id = acc['account_id']
        acc_txs = [t for t in sample_transactions if t['account_id'] == acc_id]
        acc_income = sum(float(t['amount']) for t in acc_txs if t['transaction_type'] == 'Income')
        acc_expense = sum(float(t['amount']) for t in acc_txs if t['transaction_type'] == 'Expense')
        acc_total = acc_income + acc_expense
        avg_amt = (acc_total / len(acc_txs)) if acc_txs else 0.0

        account_reports.append({
            'account_id': acc_id,
            'account_holder': acc['account_holder'],
            'account_type': acc['account_type'],
            'balance': acc['balance'],
            'tx_count': len(acc_txs),
            'total_income': acc_income,
            'total_expense': acc_expense,
            'avg_amount': avg_amt
        })
        chart_labels.append(acc['account_holder'])
        chart_data.append(acc_total)

    # Incident counts by status
    incident_status_counts = {}
    for inc in sample_fraud_incidents:
        st = inc['incident_status']
        incident_status_counts[st] = incident_status_counts.get(st, 0) + 1

    return render_template(
        'reports.html',
        active_page='reports',
        report_summary=report_summary,
        account_reports=account_reports,
        account_chart_labels=chart_labels,
        account_chart_data=chart_data,
        incident_status_counts=incident_status_counts
    )


@app.route('/algorithms')
def algorithms_page():
    """7. DSA Algorithms Benchmark Page"""
    return render_template('algorithms.html', active_page='algorithms')


# ------------------------------------------------------------------------------
# CRUD OPERATIONS (Accounts, Transactions, Incidents)
# ------------------------------------------------------------------------------

@app.route('/accounts/add', methods=['POST'])
def add_account():
    holder = request.form.get('account_holder', '').strip()
    acc_type = request.form.get('account_type', '').strip()
    acc_num = request.form.get('account_number', '').strip()
    balance = float(request.form.get('balance', 0.0))

    if not holder or not acc_num:
        flash("Account holder name and account number are required.", "danger")
        return redirect(url_for('accounts_page'))

    # Check uniqueness
    if any(a['account_number'] == acc_num for a in sample_accounts):
        flash(f"Account number '{acc_num}' already exists in database.", "warning")
        return redirect(url_for('accounts_page'))

    new_id = (max(a['account_id'] for a in sample_accounts) + 1) if sample_accounts else 1
    new_acc = {
        'account_id': new_id,
        'account_holder': holder,
        'account_type': acc_type,
        'account_number': acc_num,
        'balance': balance,
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    sample_accounts.append(new_acc)
    flash(f"Account #{new_id} for '{holder}' successfully created!", "success")
    return redirect(url_for('accounts_page'))


@app.route('/accounts/update', methods=['POST'])
def update_account():
    acc_id = int(request.form.get('account_id'))
    for acc in sample_accounts:
        if acc['account_id'] == acc_id:
            acc['account_holder'] = request.form.get('account_holder', acc['account_holder']).strip()
            acc['account_type'] = request.form.get('account_type', acc['account_type'])
            acc['account_number'] = request.form.get('account_number', acc['account_number']).strip()
            acc['balance'] = float(request.form.get('balance', acc['balance']))
            flash(f"Account #{acc_id} updated successfully.", "success")
            break
    return redirect(url_for('accounts_page'))


@app.route('/accounts/delete/<int:account_id>', methods=['POST'])
def delete_account(account_id):
    # Foreign key check: Check if transactions exist
    linked_tx = [t for t in sample_transactions if t['account_id'] == account_id]
    if linked_tx:
        flash(f"Cannot delete Account #{account_id}: Referenced by {len(linked_tx)} active transaction record(s) (Foreign Key Constraint).", "danger")
        return redirect(url_for('accounts_page'))

    global sample_accounts
    sample_accounts = [a for a in sample_accounts if a['account_id'] != account_id]
    flash(f"Account #{account_id} removed from system.", "info")
    return redirect(url_for('accounts_page'))


@app.route('/transactions/add', methods=['POST'])
def add_transaction():
    account_id = int(request.form.get('account_id'))
    tx_type = request.form.get('transaction_type')
    amount = float(request.form.get('amount', 0.0))
    status = request.form.get('transaction_status', 'Completed')
    desc = request.form.get('description', '').strip()

    acc = next((a for a in sample_accounts if a['account_id'] == account_id), None)
    holder_name = acc['account_holder'] if acc else "Unknown"
    balance = acc['balance'] if acc else 10000.0

    # Rule-based Risk Scoring
    score, level, reason = evaluate_transaction_risk(amount, status, balance)

    new_tx_id = (max(t['transaction_id'] for t in sample_transactions) + 1) if sample_transactions else 101
    now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    new_tx = {
        'transaction_id': new_tx_id,
        'account_id': account_id,
        'account_holder': holder_name,
        'transaction_type': tx_type,
        'amount': amount,
        'transaction_date': now_str,
        'description': desc,
        'transaction_status': status,
        'risk_score': score,
        'risk_level': level
    }
    sample_transactions.append(new_tx)

    # Automatically log into Risk_Assessments table
    new_risk_id = (max(r['risk_id'] for r in sample_risk_assessments) + 1) if sample_risk_assessments else 1
    sample_risk_assessments.append({
        'risk_id': new_risk_id,
        'transaction_id': new_tx_id,
        'account_holder': holder_name,
        'amount': amount,
        'risk_score': score,
        'risk_level': level,
        'risk_reason': reason,
        'assessment_date': now_str
    })

    # Update account balance in memory
    if acc and status == 'Completed':
        if tx_type == 'Income':
            acc['balance'] += amount
        elif tx_type == 'Expense':
            acc['balance'] = max(0.0, acc['balance'] - amount)

    flash(f"Transaction #TX-{new_tx_id} recorded! Risk evaluated: {score}/100 ({level} Risk).", "success")
    return redirect(url_for('transactions_page'))


@app.route('/transactions/update', methods=['POST'])
def update_transaction():
    tx_id = int(request.form.get('transaction_id'))
    account_id = int(request.form.get('account_id'))
    tx_type = request.form.get('transaction_type')
    amount = float(request.form.get('amount', 0.0))
    status = request.form.get('transaction_status')
    desc = request.form.get('description', '').strip()

    acc = next((a for a in sample_accounts if a['account_id'] == account_id), None)
    holder_name = acc['account_holder'] if acc else "Unknown"

    for tx in sample_transactions:
        if tx['transaction_id'] == tx_id:
            tx['account_id'] = account_id
            tx['account_holder'] = holder_name
            tx['transaction_type'] = tx_type
            tx['amount'] = amount
            tx['transaction_status'] = status
            tx['description'] = desc
            flash(f"Transaction #TX-{tx_id} updated.", "success")
            break
    return redirect(url_for('transactions_page'))


@app.route('/transactions/delete/<int:transaction_id>', methods=['POST'])
def delete_transaction(transaction_id):
    global sample_transactions, sample_risk_assessments, sample_fraud_incidents
    sample_transactions = [t for t in sample_transactions if t['transaction_id'] != transaction_id]
    sample_risk_assessments = [r for r in sample_risk_assessments if r['transaction_id'] != transaction_id]
    sample_fraud_incidents = [f for f in sample_fraud_incidents if f['transaction_id'] != transaction_id]
    flash(f"Transaction #TX-{transaction_id} and related assessments removed.", "info")
    return redirect(url_for('transactions_page'))


@app.route('/fraud-incidents/add', methods=['POST'])
def add_fraud_incident():
    tx_id = int(request.form.get('transaction_id'))
    fraud_type = request.form.get('fraud_type')
    desc = request.form.get('incident_description', '').strip()

    tx = next((t for t in sample_transactions if t['transaction_id'] == tx_id), None)
    holder_name = tx['account_holder'] if tx else "Unknown"

    new_inc_id = (max(i['incident_id'] for i in sample_fraud_incidents) + 1) if sample_fraud_incidents else 1
    sample_fraud_incidents.append({
        'incident_id': new_inc_id,
        'transaction_id': tx_id,
        'account_holder': holder_name,
        'fraud_type': fraud_type,
        'incident_description': desc,
        'incident_status': 'Open',
        'reported_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })
    flash(f"Fraud review incident #INC-{new_inc_id} opened for Transaction #TX-{tx_id}.", "warning")
    return redirect(url_for('fraud_detection_page'))


@app.route('/fraud-incidents/update', methods=['POST'])
def update_fraud_incident():
    inc_id = int(request.form.get('incident_id'))
    status = request.form.get('incident_status')
    desc = request.form.get('incident_description', '').strip()

    for inc in sample_fraud_incidents:
        if inc['incident_id'] == inc_id:
            inc['incident_status'] = status
            inc['incident_description'] = desc
            flash(f"Incident #INC-{inc_id} status updated to '{status}'.", "success")
            break
    return redirect(url_for('fraud_detection_page'))


# ------------------------------------------------------------------------------
# DSA BENCHMARK API ENDPOINT
# ------------------------------------------------------------------------------
@app.route('/api/run-algorithm', methods=['POST'])
def run_algorithm_api():
    """
    Executes explicit manual Python algorithms on transaction records
    and measures actual wall-clock execution time with high resolution.
    """
    payload = request.get_json() or {}
    algo = payload.get('algorithm', 'merge_sort')
    dataset = [dict(t) for t in sample_transactions]

    start_time = time.perf_counter()
    results = []
    comparisons = 0
    message = ""

    if algo == 'merge_sort':
        reverse = payload.get('reverse', False)
        results = merge_sort(dataset, key='amount', reverse=reverse)
        order_text = "Descending (Highest to Lowest)" if reverse else "Ascending (Lowest to Highest)"
        message = f"Merge Sort executed successfully in O(n log n) time. Transactions sorted by amount in {order_text}."

    elif algo == 'quick_sort':
        reverse = payload.get('reverse', True)
        results = quick_sort(dataset, key='risk_score', reverse=reverse)
        order_text = "Highest to Lowest" if reverse else "Lowest to Highest"
        message = f"Quick Sort executed using Lomuto partitioning. Transactions sorted by Risk Score from {order_text}."

    elif algo == 'binary_search':
        target_id = payload.get('target_id', 103)
        # Pre-requisite for binary search: Sort by transaction_id
        sorted_txs = merge_sort(dataset, key='transaction_id', reverse=False)
        search_res = binary_search(sorted_txs, target_id, key='transaction_id')
        comparisons = search_res['comparisons']
        message = search_res['message']
        results = [search_res['record']] if search_res['found'] else []

    elif algo == 'linear_search':
        keyword = payload.get('keyword', '')
        search_field = payload.get('search_field', 'description')
        search_res = linear_search(dataset, keyword, search_field=search_field)
        comparisons = search_res['comparisons']
        message = search_res['message']
        results = search_res['matches']

    elif algo == 'hashing':
        action = payload.get('action', 'duplicates')
        if action == 'lookup':
            lookup_id = payload.get('lookup_id', 101)
            hash_table = TransactionHashTable(capacity=53)
            for tx in dataset:
                hash_table.insert(tx)
            record = hash_table.get(lookup_id)
            comparisons = 1
            if record:
                results = [record]
                message = f"Hash Table O(1) instantaneous lookup: Found Transaction #TX-{lookup_id}."
            else:
                results = []
                message = f"Hash Table O(1) lookup: Transaction #TX-{lookup_id} not present in hash buckets."
        else:
            # Duplicate ID test dataset (inject mock retry attempt)
            test_batch = list(dataset) + [
                {'transaction_id': 103, 'account_id': 2, 'account_holder': 'David Sterling (Duplicate Retry)', 'transaction_type': 'Expense', 'amount': 6800.00, 'description': 'Duplicate Wire Transmission', 'transaction_status': 'Failed', 'risk_score': 85}
            ]
            dup_res = find_duplicate_ids(test_batch)
            comparisons = dup_res['total_scanned']
            results = [tx for tx in test_batch if tx['transaction_id'] in dup_res['duplicate_ids']]
            message = f"Hashing duplicate scan complete: Found {dup_res['duplicate_count']} collision(s). {'; '.join(dup_res['details'])}"

    end_time = time.perf_counter()
    elapsed_sec = end_time - start_time
    elapsed_ms = round(elapsed_sec * 1000, 3)
    elapsed_us = round(elapsed_sec * 1_000_000, 1)

    return jsonify({
        'success': True,
        'algorithm': algo,
        'execution_time_ms': elapsed_ms,
        'execution_time_us': elapsed_us,
        'records_processed': len(dataset),
        'comparisons': comparisons,
        'message': message,
        'results': results
    })


if __name__ == '__main__':
    print("=" * 65)
    print(" FINANCIAL RISK MANAGEMENT SYSTEM - College PBL (DBMS + DSA)")
    print(" Flask Development Server Starting...")
    print(" Access Dashboard at: http://127.0.0.1:5000")
    print("=" * 65)
    app.run(debug=True, port=5000)
