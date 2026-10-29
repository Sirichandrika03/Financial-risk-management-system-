"""
Linear Search Implementation for Transaction Keyword Lookup
===========================================================
Purpose:
    Search through transaction records sequentially to match keywords in
    'description', 'transaction_status', 'transaction_type', or account holder name.

Time Complexity:
    - Best Case:    O(1) [Target located at index 0]
    - Average Case: O(n)
    - Worst Case:   O(n) [Target at the end or not present]

Space Complexity:
    - O(k) where k is the count of matched records.

Why Linear Search:
    Unlike Binary Search, Linear Search does not require the dataset to be sorted
    and can perform partial string matches across non-indexed attributes.
"""

def linear_search(transactions, keyword, search_field='description'):
    """
    Manually scans every transaction record in sequence.
    Performs case-insensitive substring matching.

    Returns:
        dict: {
            'matches': list of matched dicts,
            'match_count': int,
            'total_scanned': int,
            'comparisons': int,
            'message': str
        }
    """
    query = str(keyword).strip().lower()
    matches = []
    comparisons = 0

    for record in transactions:
        comparisons += 1
        
        # Check specific field or search across all text attributes if 'all'
        if search_field == 'all':
            combined_text = " ".join(str(v) for v in record.values()).lower()
            if query in combined_text:
                matches.append(record)
        else:
            val = str(record.get(search_field, '')).lower()
            if query in val:
                matches.append(record)

    return {
        'matches': matches,
        'match_count': len(matches),
        'total_scanned': len(transactions),
        'comparisons': comparisons,
        'message': f"Found {len(matches)} matching transaction(s) after scanning {comparisons} records."
    }
