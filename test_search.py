import requests
import json

# test the electronics search
def test_electronics_search():
    url = "http://localhost:8080/query"
    
    test_queries = [
        "show me electronics under 300 dollars",
        "electronics under $300",
        "cheap electronics",
        "electronics less than 300"
    ]
    
    for query in test_queries:
        print(f"\n--- Testing: '{query}' ---")
        
        payload = {"query": query}
        
        try:
            response = requests.post(url, json=payload)
            
            if response.status_code == 200:
                data = response.json()
                print(f" Success!")
                print(f"Summary: {data.get('summary', 'N/A')}")
                print(f"Result count: {data.get('result_count', 0)}")
                
                if data.get('results'):
                    print("Found products:")
                    for result in data['results']:
                        print(f"  - {result.get('name', 'Unknown')} - ${result.get('price', 'N/A')}")
                else:
                    print("No products found")
            else:
                print(f" Error {response.status_code}: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print(" Could not connect to server. Make sure your Flask app is running!")
        except Exception as e:
            print(f" Unexpected error: {e}")

if __name__ == "__main__":
    test_electronics_search()