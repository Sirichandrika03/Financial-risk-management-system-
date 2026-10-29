/**
 * Financial Risk Management System - Interactive Frontend Script
 * Handles UI interactions, modal controllers, client search/filter,
 * toast notifications, dynamic charts, and DSA execution sandbox.
 */

document.addEventListener('DOMContentLoaded', () => {
  initSidebarToggle();
  initModals();
  initTableSearchAndFilters();
  initToasts();
});

/**
 * Formats a numeric value using the Indian numbering system (en-IN)
 * e.g. ₹1,000.00, ₹25,500.50, ₹1,00,000.00, ₹10,00,000.00
 */
function formatINR(amount, includeSymbol = true) {
  const val = parseFloat(amount) || 0;
  const formatted = val.toLocaleString('en-IN', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  });
  return includeSymbol ? `₹${formatted}` : formatted;
}

/* ==========================================================================
   Sidebar Toggle (Mobile)
   ========================================================================== */
function initSidebarToggle() {
  const menuBtn = document.getElementById('menuToggleBtn');
  const sidebar = document.querySelector('.sidebar');

  if (menuBtn && sidebar) {
    menuBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      sidebar.classList.toggle('open');
    });

    document.addEventListener('click', (e) => {
      if (!sidebar.contains(e.target) && !menuBtn.contains(e.target)) {
        sidebar.classList.remove('open');
      }
    });
  }
}

/* ==========================================================================
   Toast Notification System
   ========================================================================== */
function showToast(message, type = 'info') {
  let container = document.querySelector('.toast-container');
  if (!container) {
    container = document.createElement('div');
    container.className = 'toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.innerHTML = `
    <span>${message}</span>
    <button style="background:none;border:none;cursor:pointer;color:#94a3b8;font-size:1.1rem;margin-left:0.5rem;" onclick="this.parentElement.remove()">×</button>
  `;

  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(100%)';
    toast.style.transition = 'all 0.3s ease';
    setTimeout(() => toast.remove(), 300);
  }, 4000);
}

function initToasts() {
  // Automatically bind flash messages if present in DOM
  const flashAlerts = document.querySelectorAll('.flash-message-data');
  flashAlerts.forEach(el => {
    const msg = el.getAttribute('data-message');
    const cat = el.getAttribute('data-category') || 'info';
    if (msg) showToast(msg, cat);
  });
}

/* ==========================================================================
   Modal Controllers
   ========================================================================== */
function openModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.add('show');
    document.body.style.overflow = 'hidden';
  }
}

function closeModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.remove('show');
    document.body.style.overflow = '';
  }
}

function initModals() {
  // Close modals when clicking backdrop
  document.querySelectorAll('.modal-backdrop').forEach(modal => {
    modal.addEventListener('click', (e) => {
      if (e.target === modal) {
        closeModal(modal.id);
      }
    });
  });

  // Close modals with Escape key
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      document.querySelectorAll('.modal-backdrop.show').forEach(m => closeModal(m.id));
    }
  });
}

/* ==========================================================================
   Client-Side Table Search & Filter
   ========================================================================== */
function initTableSearchAndFilters() {
  const searchInputs = document.querySelectorAll('[data-table-search]');
  searchInputs.forEach(input => {
    const tableId = input.getAttribute('data-table-search');
    const table = document.getElementById(tableId);
    if (!table) return;

    input.addEventListener('input', () => {
      const query = input.value.trim().toLowerCase();
      const rows = table.querySelectorAll('tbody tr');

      rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        row.style.display = text.includes(query) ? '' : 'none';
      });
    });
  });

  // Filter selects
  const filterSelects = document.querySelectorAll('[data-table-filter]');
  filterSelects.forEach(select => {
    const tableId = select.getAttribute('data-table-filter');
    const filterKey = select.getAttribute('data-filter-col'); // column index
    const table = document.getElementById(tableId);
    if (!table) return;

    select.addEventListener('change', () => {
      const selectedValue = select.value.toLowerCase();
      const rows = table.querySelectorAll('tbody tr');

      rows.forEach(row => {
        if (!selectedValue || selectedValue === 'all') {
          row.style.display = '';
          return;
        }

        const cell = row.children[filterKey];
        if (cell) {
          const cellText = cell.textContent.trim().toLowerCase();
          row.style.display = cellText.includes(selectedValue) ? '' : 'none';
        }
      });
    });
  });
}

/* ==========================================================================
   Account Modal Edit Populate Helper
   ========================================================================== */
function populateAccountEdit(accountId, holder, type, number, balance) {
  document.getElementById('edit_account_id').value = accountId;
  document.getElementById('edit_account_holder').value = holder;
  document.getElementById('edit_account_type').value = type;
  document.getElementById('edit_account_number').value = number;
  document.getElementById('edit_balance').value = balance;
  openModal('editAccountModal');
}

/* ==========================================================================
   Transaction Modal Edit Populate Helper
   ========================================================================== */
function populateTransactionEdit(txId, accountId, type, amount, status, desc) {
  document.getElementById('edit_tx_id').value = txId;
  document.getElementById('edit_tx_account_id').value = accountId;
  document.getElementById('edit_tx_type').value = type;
  document.getElementById('edit_tx_amount').value = amount;
  document.getElementById('edit_tx_status').value = status;
  document.getElementById('edit_tx_description').value = desc;
  openModal('editTransactionModal');
}

/* ==========================================================================
   Fraud Incident Modal Edit Populate Helper
   ========================================================================== */
function populateIncidentEdit(incidentId, status, desc) {
  document.getElementById('edit_incident_id').value = incidentId;
  document.getElementById('edit_incident_status').value = status;
  document.getElementById('edit_incident_description').value = desc;
  openModal('editIncidentModal');
}

/* ==========================================================================
   Interactive DSA Sandbox Controller
   ========================================================================== */
let activeAlgo = 'merge_sort';

function switchAlgoTab(algoName) {
  activeAlgo = algoName;
  document.querySelectorAll('.algo-tab-btn').forEach(btn => {
    btn.classList.remove('active');
    if (btn.getAttribute('data-algo') === algoName) {
      btn.classList.add('active');
    }
  });

  // Toggle control panels
  const sortControls = document.getElementById('sortControls');
  const binarySearchControls = document.getElementById('binarySearchControls');
  const linearSearchControls = document.getElementById('linearSearchControls');
  const hashingControls = document.getElementById('hashingControls');

  const algoTitle = document.getElementById('algoTitle');
  const algoDescription = document.getElementById('algoDescription');
  const algoTheoryComplexity = document.getElementById('algoTheoryComplexity');
  const algoSpaceComplexity = document.getElementById('algoSpaceComplexity');

  // Hide all specific controls first
  if (sortControls) sortControls.style.display = 'none';
  if (binarySearchControls) binarySearchControls.style.display = 'none';
  if (linearSearchControls) linearSearchControls.style.display = 'none';
  if (hashingControls) hashingControls.style.display = 'none';

  if (algoName === 'merge_sort') {
    if (sortControls) sortControls.style.display = 'flex';
    algoTitle.textContent = 'Merge Sort Algorithm';
    algoDescription.textContent = 'Divide-and-Conquer sorting algorithm. Recursively splits transaction array into halves and merges them in sorted order based on transaction amount. Stable and guaranteed O(n log n).';
    algoTheoryComplexity.textContent = 'O(n log n)';
    algoSpaceComplexity.textContent = 'O(n)';
  } else if (algoName === 'quick_sort') {
    if (sortControls) sortControls.style.display = 'flex';
    algoTitle.textContent = 'Quick Sort Algorithm';
    algoDescription.textContent = 'Partition-based sorting algorithm using Lomuto partitioning. Sorts risk assessments from highest risk score to lowest to prioritize urgent threats.';
    algoTheoryComplexity.textContent = 'Avg: O(n log n) | Worst: O(n²)';
    algoSpaceComplexity.textContent = 'O(log n)';
  } else if (algoName === 'binary_search') {
    if (binarySearchControls) binarySearchControls.style.display = 'flex';
    algoTitle.textContent = 'Binary Search Algorithm';
    algoDescription.textContent = 'Fast search on sorted transaction records by Transaction ID. Halves the search space on each comparison. Pre-requisite: Transactions sorted by ID.';
    algoTheoryComplexity.textContent = 'O(log n)';
    algoSpaceComplexity.textContent = 'O(1)';
  } else if (algoName === 'linear_search') {
    if (linearSearchControls) linearSearchControls.style.display = 'flex';
    algoTitle.textContent = 'Linear Search Algorithm';
    algoDescription.textContent = 'Sequential search through transaction records. Ideal for keyword and substring queries on descriptions or statuses without needing pre-sorting.';
    algoTheoryComplexity.textContent = 'O(n)';
    algoSpaceComplexity.textContent = 'O(k)';
  } else if (algoName === 'hashing') {
    if (hashingControls) hashingControls.style.display = 'flex';
    algoTitle.textContent = 'Hash Table & Duplicate ID Detection';
    algoDescription.textContent = 'Demonstrates in-memory hash table lookup with separate chaining and single-pass duplicate key detection. Note: The MySQL Primary Key enforces database integrity.';
    algoTheoryComplexity.textContent = 'O(1) Avg Lookup | O(n) Duplicate Scan';
    algoSpaceComplexity.textContent = 'O(n)';
  }
}

async function executeCurrentAlgorithm() {
  const resultCard = document.getElementById('algoResultSection');
  const resultTbody = document.getElementById('algoResultTbody');
  const measuredTimeEl = document.getElementById('measuredExecutionTime');
  const recordsProcessedEl = document.getElementById('recordsProcessedCount');
  const comparisonsEl = document.getElementById('comparisonsCount');
  const statusMsgEl = document.getElementById('algoStatusMessage');

  // Payload construction
  const payload = {
    algorithm: activeAlgo
  };

  if (activeAlgo === 'merge_sort' || activeAlgo === 'quick_sort') {
    const orderSelect = document.getElementById('sortOrderSelect');
    payload.reverse = orderSelect ? orderSelect.value === 'desc' : false;
  } else if (activeAlgo === 'binary_search') {
    const targetInput = document.getElementById('binarySearchTarget');
    payload.target_id = targetInput ? targetInput.value : '';
  } else if (activeAlgo === 'linear_search') {
    const keywordInput = document.getElementById('linearSearchKeyword');
    const fieldSelect = document.getElementById('linearSearchField');
    payload.keyword = keywordInput ? keywordInput.value : '';
    payload.search_field = fieldSelect ? fieldSelect.value : 'description';
  } else if (activeAlgo === 'hashing') {
    const hashAction = document.getElementById('hashingActionSelect');
    const hashIdInput = document.getElementById('hashingLookupId');
    payload.action = hashAction ? hashAction.value : 'duplicates';
    payload.lookup_id = hashIdInput ? hashIdInput.value : '';
  }

  showToast(`Running ${activeAlgo.replace('_', ' ').toUpperCase()}...`, 'info');

  try {
    const response = await fetch('/api/run-algorithm', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    const data = await response.json();

    if (!data.success) {
      showToast(data.error || 'Algorithm execution failed', 'danger');
      return;
    }

    if (resultCard) resultCard.style.display = 'block';
    if (measuredTimeEl) measuredTimeEl.textContent = `${data.execution_time_ms} ms (${data.execution_time_us} µs)`;
    if (recordsProcessedEl) recordsProcessedEl.textContent = data.records_processed;
    if (comparisonsEl) comparisonsEl.textContent = data.comparisons !== undefined ? data.comparisons : 'N/A';
    if (statusMsgEl) statusMsgEl.innerHTML = data.message || 'Execution completed successfully.';

    // Populate results table
    if (resultTbody) {
      resultTbody.innerHTML = '';
      const records = data.results || [];

      if (records.length === 0) {
        resultTbody.innerHTML = `<tr><td colspan="7" style="text-align:center;color:#64748b;padding:2rem;">No matching records found.</td></tr>`;
      } else {
        records.forEach(tx => {
          const tr = document.createElement('tr');
          const riskScore = tx.risk_score !== undefined ? tx.risk_score : 20;
          let riskBadgeClass = 'badge-low';
          let riskLabel = 'Low Risk';
          if (riskScore >= 70) {
            riskBadgeClass = 'badge-high';
            riskLabel = 'High Risk';
          } else if (riskScore >= 30) {
            riskBadgeClass = 'badge-medium';
            riskLabel = 'Medium Risk';
          }

          tr.innerHTML = `
            <td><strong>#TX-${tx.transaction_id}</strong></td>
            <td>${tx.account_holder || `Account #${tx.account_id}`}</td>
            <td><span class="badge ${tx.transaction_type === 'Income' ? 'badge-type-income' : 'badge-type-expense'}">${tx.transaction_type}</span></td>
            <td><strong>${formatINR(tx.amount)}</strong></td>
            <td>${tx.description || '-'}</td>
            <td><span class="badge ${riskBadgeClass}">${riskScore}/100 (${riskLabel})</span></td>
            <td><span class="badge badge-${(tx.transaction_status || 'completed').toLowerCase()}">${tx.transaction_status || 'Completed'}</span></td>
          `;
          resultTbody.appendChild(tr);
        });
      }
    }

    showToast(`Execution finished in ${data.execution_time_ms} ms!`, 'success');
  } catch (err) {
    console.error('Error executing algorithm:', err);
    showToast('Failed to connect to backend algorithm runner', 'danger');
  }
}
