#!/usr/bin/env python3
"""
Provide some stats about Nginx logs stored in MongoDB
"""
from pymongo import MongoClient


def log_stats():
    """
    Database: logs, Collection: nginx,
    Methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    """
    # Connect to the MongoDB server
    client = MongoClient()
    # Access the logs database and the nginx collection
    db = client.logs
    collection = db.nginx

    # Count the total number of logs
    total_logs = collection.count_documents({})
    print(f"{total_logs} logs")

    # Count the occurrences of each HTTP method
    print("Methods:")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        count = collection.count_documents({"method": method})
        print(f"\tmethod {method}: {count}")

    # Count documents with method=GET and path=/status
    status_check_count = collection.count_documents({"method": "GET", "path": "/status"})
    print(f"{status_check_count} status check")

if __name__ == "__main__":
    log_stats()
