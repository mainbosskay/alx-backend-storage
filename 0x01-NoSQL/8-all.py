#!/usr/bin/env python3
"""Module for function that lists all documents in a collection"""


def list_all(mongo_collection):
    """Getting lists all document in a collection"""
    return [doc_list for doc_list in mongo_collection.find()]
