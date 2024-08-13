#!/usr/bin/env python3
"""Module that provides stats about Nginx logs in MongoDB"""


def nginx_log_statistics(nginx_collection):
    """Getting and print some stats about Nginx logs in MongoDB"""
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


if __name__ == "__main__":
    with MongoClient() as client:
        db = client.logs
        collection = db.nginx
        nginx_log_statistics(collection)
