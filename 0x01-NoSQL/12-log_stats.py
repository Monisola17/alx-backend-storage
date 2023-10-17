#!/usr/bin/env python3
""" 12. Log stats
"""


from pymongo import MongoClient


mongo_uri = "mongodb://localhost:27017"
database_name = "logs"
collection_name = "nginx"

# Connect to MongoDB and access the collection
client = MongoClient(mongo_uri)
db = client[database_name]
collection = db[collection_name]

# Count the total number of logs
total_logs = collection.count_documents({})

# Count the number of logs for each HTTP method
http_methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
method_counts = {}

for method in http_methods:
    method_count = collection.count_documents({"method": method})
    method_counts[method] = method_count

# Count the number of logs with method=GET and path=/status
status_logs = collection.count_documents({"method": "GET", "path": "/status"})

# Display the statistics
print(f"{total_logs} logs")

print("Methods:")
for method in http_methods:
    print(f"\t{method}: {method_counts[method]}")

print(f"{status_logs} logs with method=GET and path=/status")

