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
    client = MongoClient()
    db = client.logs
    collection = db.nginx

    total_logs = collection.count_documents({})
    print(f"{total_logs: logs}")
    print("Methods:")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        count = collection.count_documents({"method": method})
        print(f"\tmethod {method}: {count}")

    status_check_count = collection.count_documents({"method": "GET", "path": "/status"})
    print(f"{status_check_count} status check")

    # Aggregate top 10 IPs
    print("IPs:")
    ip_counts = collection.aggregate([
        {
            "$group": {
                "_id": "$ip",
                "count": {"$sum": 1}
            }
        },
        {
            "$sort": {
                "count": -1  # Sort by count in descending order
            }
        },
        {
            "$limit": 10  # Limit to top 10 IPs
        }
    ])

    # Print top 10 IPs
    for ip in ip_counts:
        print(f"\t{ip['_id']}: {ip['count']}")

if __name__ == "__main__":
    log_stats()
