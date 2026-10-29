"""
Stage 1 Automated Verification Script
Tests all 7 frontend page routes and the manual DSA algorithm execution endpoint.
"""
from app import app

def test_frontend_routes():
    client = app.test_client()
    routes = [
        ('/', 'Dashboard'),
        ('/accounts', 'Accounts'),
        ('/transactions', 'Transactions'),
        ('/risk-assessment', 'Risk Assessment'),
        ('/fraud-detection', 'Fraud Incidents'),
        ('/reports', 'Reports'),
        ('/algorithms', 'DSA Algorithms')
    ]

    print("Verifying 7 Website Pages:")
    for path, name in routes:
        response = client.get(path)
        assert response.status_code == 200, f"Route {path} failed with code {response.status_code}"
        print(f"  [PASS] {name} ({path}) -> HTTP 200 OK")

    print("\nVerifying DSA Algorithm API Endpoints:")
    algorithms_to_test = [
        ('merge_sort', {'algorithm': 'merge_sort', 'reverse': False}),
        ('quick_sort', {'algorithm': 'quick_sort', 'reverse': True}),
        ('binary_search', {'algorithm': 'binary_search', 'target_id': 103}),
        ('linear_search', {'algorithm': 'linear_search', 'keyword': 'Wire', 'search_field': 'description'}),
        ('hashing_lookup', {'algorithm': 'hashing', 'action': 'lookup', 'lookup_id': 101}),
        ('hashing_duplicates', {'algorithm': 'hashing', 'action': 'duplicates'})
    ]

    for name, payload in algorithms_to_test:
        response = client.post('/api/run-algorithm', json=payload)
        assert response.status_code == 200, f"Algorithm {name} failed"
        data = response.get_json()
        assert data['success'] is True
        print(f"  [PASS] {name} -> Time: {data['execution_time_ms']} ms | Processed: {data['records_processed']} records")

    print("\nStage 1 All 7 pages and DSA endpoints passed successfully!")

if __name__ == '__main__':
    test_frontend_routes()
