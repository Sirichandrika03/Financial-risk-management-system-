"""
Binary Search Implementation for Transaction ID Lookup
======================================================
Purpose:
    Quickly locate a specific financial transaction record by its unique
    'transaction_id' in a pre-sorted dataset.

Prerequisite:
    The dataset MUST be sorted in ascending order by 'transaction_id'.

Time Complexity:
    - Search Time:  O(log n)
    - Prerequisite Sort Time (if needed): O(n log n)
    - Best Case:    O(1) [Target located at the midpoint]

Space Complexity:
    - O(1) iterative space.

Algorithm Steps:
    1. Define search bounds: low = 0, high = len(arr) - 1.
    2. Compute midpoint mid = (low + high) // 2.
    3. If target == arr[mid], return the record and number of comparisons.
    4. If target < arr[mid], search the left half (high = mid - 1).
    5. If target > arr[mid], search the right half (low = mid + 1).
    6. If low > high, record does not exist.
"""

def binary_search(sorted_transactions, target_id, key='transaction_id'):
    """
    Performs manual iterative binary search for target_id on a sorted list.
    
    Returns:
        dict: {
            'found': bool,
            'record': dict or None,
            'index': int or -1,
            'comparisons': int,
            'search_path': list of ints (indices checked)
        }
    """
    try:
        target = int(target_id)
    except (ValueError, TypeError):
        return {
            'found': False,
            'record': None,
            'index': -1,
            'comparisons': 0,
            'search_path': [],
            'message': f"Invalid target ID: '{target_id}'. Must be an integer."
        }

    low = 0
    high = len(sorted_transactions) - 1
    comparisons = 0
    search_path = []

    while low <= high:
        comparisons += 1
        mid = (low + high) // 2
        search_path.append(mid)

        current_id = int(sorted_transactions[mid].get(key, -1))

        if current_id == target:
            return {
                'found': True,
                'record': sorted_transactions[mid],
                'index': mid,
                'comparisons': comparisons,
                'search_path': search_path,
                'message': f"Transaction ID #{target} found at index {mid} after {comparisons} comparison(s)."
            }
        elif current_id < target:
            low = mid + 1
        else:
            high = mid - 1

    return {
        'found': False,
        'record': None,
        'index': -1,
        'comparisons': comparisons,
        'search_path': search_path,
        'message': f"Transaction ID #{target} was NOT found after {comparisons} comparison(s)."
    }
