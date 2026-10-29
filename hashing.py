"""
Hashing Implementation for O(1) Transaction Lookup & Duplicate ID Detection
============================================================================
Purpose:
    Provide instantaneous O(1) record retrieval using a hash table structure
    and demonstrate duplicate key detection in incoming batch feeds.

Educational Distinction:
    - In our MySQL database, the PRIMARY KEY constraint on `transaction_id`
      is strictly responsible for enforcing database-level uniqueness and integrity.
    - This software hashing module simulates an in-memory verification layer
      (e.g., verifying a batch of records before issuing database inserts).
    - Note: In financial processing, a repeated transaction ID in raw input feeds
      indicates a data collision, retry attempt, or submission duplicate—it is NOT
      by itself standalone proof of fraud.

Time Complexity:
    - Lookup:    O(1) average, O(n) worst-case (in case of total hash collisions)
    - Insertion: O(1) average
    - Duplicate Detection: O(n) single-pass scan

Space Complexity:
    - O(n) for the hash table buckets / dictionary storage.
"""

class TransactionHashTable:
    """
    Demonstration of an in-memory Hash Table using separate chaining
    to illustrate foundational DSA concepts.
    """
    def __init__(self, capacity=101):
        self.capacity = capacity
        self.size = 0
        self.buckets = [[] for _ in range(self.capacity)]

    def _hash_function(self, key):
        """
        Computes bucket index using modulo arithmetic on integer key.
        """
        return int(key) % self.capacity

    def insert(self, transaction):
        """
        Inserts a transaction into the hash table.
        Key is transaction['transaction_id'].
        Returns True if newly inserted, False if key already existed (updated).
        """
        t_id = int(transaction['transaction_id'])
        index = self._hash_function(t_id)
        bucket = self.buckets[index]

        for i, (k, v) in enumerate(bucket):
            if k == t_id:
                bucket[i] = (t_id, transaction)
                return False  # Updated existing

        bucket.append((t_id, transaction))
        self.size += 1
        return True

    def get(self, transaction_id):
        """
        O(1) average lookup for a transaction by ID.
        """
        t_id = int(transaction_id)
        index = self._hash_function(t_id)
        bucket = self.buckets[index]

        for k, v in bucket:
            if k == t_id:
                return v
        return None

    def contains(self, transaction_id):
        return self.get(transaction_id) is not None


def find_duplicate_ids(transaction_list):
    """
    Identifies duplicate transaction IDs in an incoming transaction list
    using an in-memory hash set / dictionary in a single O(n) pass.

    Returns:
        dict: {
            'duplicate_ids': list of duplicate IDs found,
            'duplicate_count': int,
            'unique_count': int,
            'details': list of diagnostic messages
        }
    """
    seen = {}
    duplicates = {}

    for idx, tx in enumerate(transaction_list):
        t_id = tx.get('transaction_id')
        if t_id in seen:
            if t_id not in duplicates:
                duplicates[t_id] = [seen[t_id]]
            duplicates[t_id].append(idx)
        else:
            seen[t_id] = idx

    duplicate_list = list(duplicates.keys())
    details = [
        f"Transaction ID #{tid} occurs {len(indices)} times (indices: {indices})"
        for tid, indices in duplicates.items()
    ]

    return {
        'duplicate_ids': duplicate_list,
        'duplicate_count': len(duplicate_list),
        'unique_count': len(seen),
        'total_scanned': len(transaction_list),
        'details': details
    }
