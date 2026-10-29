"""
Algorithms Package for Financial Risk Management System.
Implements manual DSA algorithms for educational college PBL project:
- Merge Sort (Sorting transactions by amount)
- Quick Sort (Sorting transactions by risk score)
- Binary Search (Searching transactions by ID)
- Linear Search (Searching transactions by keyword/description)
- Hashing (O(1) transaction lookup & duplicate ID detection)
"""
from .merge_sort import merge_sort
from .quick_sort import quick_sort
from .binary_search import binary_search
from .linear_search import linear_search
from .hashing import TransactionHashTable, find_duplicate_ids

__all__ = [
    'merge_sort',
    'quick_sort',
    'binary_search',
    'linear_search',
    'TransactionHashTable',
    'find_duplicate_ids'
]
