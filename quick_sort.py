"""
Quick Sort Implementation for Risk Scores
==========================================
Purpose:
    Sort financial transaction or risk assessment records based on the
    'risk_score' field from highest to lowest (descending) or ascending order.

Time Complexity:
    - Best Case:    O(n log n)  [Balanced partitions]
    - Average Case: O(n log n)  [Randomized/typical distribution]
    - Worst Case:   O(n^2)      [Already sorted with poor pivot selection]

Space Complexity:
    - O(log n) call stack auxiliary space.

Why Quick Sort:
    Quick Sort has low memory overhead and very small constant factors,
    making it widely preferred in practice for prioritizing critical risk alerts.
"""

def partition(arr, low, high, key='risk_score', reverse=True):
    """
    Lomuto partition scheme.
    Selects the last element as pivot and places it in its correct sorted position.
    """
    pivot_val = float(arr[high].get(key, 0))
    i = low - 1

    for j in range(low, high):
        curr_val = float(arr[j].get(key, 0))
        # reverse=True means highest to lowest (descending)
        if reverse:
            condition = (curr_val >= pivot_val)
        else:
            condition = (curr_val <= pivot_val)

        if condition:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def _quick_sort_helper(arr, low, high, key='risk_score', reverse=True):
    """
    Recursive helper function for in-place quick sort.
    """
    if low < high:
        pi = partition(arr, low, high, key=key, reverse=reverse)
        _quick_sort_helper(arr, low, pi - 1, key=key, reverse=reverse)
        _quick_sort_helper(arr, pi + 1, high, key=key, reverse=reverse)


def quick_sort(records, key='risk_score', reverse=True):
    """
    Manual Quick Sort wrapper that returns a new sorted list without mutating
    the original records.
    """
    if not records:
        return []
    records_copy = [dict(r) for r in records]
    _quick_sort_helper(records_copy, 0, len(records_copy) - 1, key=key, reverse=reverse)
    return records_copy
