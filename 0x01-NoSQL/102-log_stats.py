#!/usr/bin/env python3
"""Module for IPs in the collection nginx of the database logs"""
from pymongo import MongoClient



def nginx_log_statistics(nginx_collection):
    """Getting and prints IPs in collection nginx of database logs"""
    all_logs = nginx_collection.count_documents({})
    print(f"{all_logs} logs")
    print("Methods:")
    http_methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in http_methods:
        method_count = nginx_collection.count_documents({"method": method})
        print(f"\tmethod {method}: {method_count}")
    status_route_count = nginx_collection.count_documents({"method": "GET",
                                                           "path": "/status"})
    print(f"{status_route_count} status check")
    print("IPs:")
    top_ips = nginx_collection.aggregate([
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ])
    for ip in top_ips:
        print(f"\t{ip['_id']}: {ip['count']}")


if __name__ == "__main__":
    with MongoClient() as client:
        db = client.logs
        collection = db.nginx
        nginx_log_statistics(collection)
