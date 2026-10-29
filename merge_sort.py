"""
Merge Sort Implementation for Transactions
===========================================
Purpose:
    Sort financial transaction records based on the 'amount' field in
    ascending or descending order using the Divide-and-Conquer paradigm.

Time Complexity:
    - Best Case:    O(n log n)
    - Average Case: O(n log n)
    - Worst Case:   O(n log n)

Space Complexity:
    - O(n) auxiliary space due to temporary arrays in the merge step.

Why Merge Sort:
    Merge Sort is a stable sorting algorithm that guarantees O(n log n) performance
    regardless of initial ordering, making it ideal for financial record auditing.
"""

def merge(left, right, key='amount', reverse=False):
    """
    Merges two sorted lists (left and right) into one sorted list.
    """
    merged = []
    i = 0
    j = 0

    while i < len(left) and j < len(right):
        val_left = float(left[i].get(key, 0))
        val_right = float(right[j].get(key, 0))

        if not reverse:
            # Ascending order
            if val_left <= val_right:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1
        else:
            # Descending order
            if val_left >= val_right:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1

    # Append any remaining elements
    while i < len(left):
        merged.append(left[i])
        i += 1

    while j < len(right):
        merged.append(right[j])
        j += 1

    return merged


def merge_sort(transactions, key='amount', reverse=False):
    """
    Recursively divides the transaction list in half and merges sorted halves.
    Returns a new sorted list without mutating the original input.
    """
    if len(transactions) <= 1:
        return list(transactions)

    mid = len(transactions) // 2
    left_half = merge_sort(transactions[:mid], key=key, reverse=reverse)
    right_half = merge_sort(transactions[mid:], key=key, reverse=reverse)

    return merge(left_half, right_half, key=key, reverse=reverse)
