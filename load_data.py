
from pymongo import MongoClient
import os


products = [
    {
        "product_id": "SKU789012",
        "name": "E-commerce Product Navigator",
        "category": "Software",
        "brand": "Innovate AI Co.",
        "price": 499.99,
        "stock_quantity": 150,
        "features": ["natural_language_query", "data_integration", "query_generation"],
        "ratings": { "average": 4.5, "review_count": 85 }
    },
    {
        "product_id": "SKU123456",
        "name": "SmartHome Hub",
        "category": "Electronics",
        "brand": "Connective Living",
        "price": 129.99,
        "stock_quantity": 250,
        "features": ["voice_control", "multi-device_support"],
        "ratings": { "average": 4.8, "review_count": 1200 }
    },
    {
        "product_id": "SKU987654",
        "name": "Quantum Laptop",
        "category": "Electronics",
        "brand": "Innovate AI Co.",
        "price": 1899.99,
        "stock_quantity": 75,
        "features": ["AI_assistant", "biometric_security", "oled_display"],
        "ratings": { "average": 4.9, "review_count": 450 }
    },
    {
        "product_id": "SKU456789",
        "name": "Data Analytics Suite",
        "category": "Software",
        "brand": "DataCorp",
        "price": 899.00,
        "stock_quantity": 100,
        "features": ["data_visualization", "predictive_modeling"],
        "ratings": { "average": 4.2, "review_count": 210 }
    },
    {
        "product_id": "SKU112233",
        "name": "Wireless Noise-Cancelling Headphones",
        "category": "Electronics",
        "brand": "AudioPhonic",
        "price": 249.99,
        "stock_quantity": 300,
        "features": ["active_noise_cancellation", "30_hour_battery", "bluetooth_5.0"],
        "ratings": { "average": 4.7, "review_count": 2580 }
    }
]


MONGO_URI = "mongodb+srv://aadarshraj4321_db_user:SB4tQI7jS0mLELMn@cluster0.bbcpmws.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"


try:
    client = MongoClient(MONGO_URI)
    
    client.admin.command('ismaster')
    print("MongoDB connection successful.")


    db = client['ecommerce_catalog']
    collection = db['products']

    collection.delete_many({})
    result = collection.insert_many(products)
    
    print(f"Successfully inserted {len(result.inserted_ids)} documents.")
    print("\n--- Verification ---")
    print(f"Found {collection.count_documents({})} documents in the 'products' collection.")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    if 'client' in locals():
        client.close()
        print("MongoDB connection closed.")