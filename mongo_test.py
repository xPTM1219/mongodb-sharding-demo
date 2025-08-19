from pymongo import MongoClient

# Connect to the MongoDB server
client = MongoClient('mongodb://localhost:6000/')

# Select the database
db = client['db']

# Insert data into the xlogs collection
def insert_data():
    data = {
        "log_id": 12345,
        "timestamp": 1630789600,  # Example timestamp
        "expire": 1634976000,     # Expire after 1 day (in seconds)
        "data": "Sample data"
    }
    result = db.xlogs.insert_one(data)
    print(f"Inserted document with ID: {result.inserted_id}")

# Read data from the xlogs collection
def read_data():
    query = {"log_id": 12345}
    documents = db.xlogs.find(query)
    for doc in documents:
        print(doc)

# Delete data from the xlogs collection
def delete_data():
    query = {"log_id": 12345}
    result = db.xlogs.delete_one(query)
    if result.deleted_count > 0:
        print("Document deleted successfully")
    else:
        print("No document found to delete")

# Example usage
insert_data()
read_data()
delete_data()

# Close the connection
client.close()
