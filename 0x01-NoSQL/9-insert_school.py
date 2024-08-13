#!/usr/bin/env python3
"""Module for function that inserts a new doc in collection"""


def insert_school(mongo_collection, **kwargs):
    """Inserting a doc in a collection based on kwargs"""
    new_doc = mongo_collection.insert_one(kwargs)
    return new_doc.inserted_d
