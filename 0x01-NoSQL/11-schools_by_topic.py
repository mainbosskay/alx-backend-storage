#!/usr/bin/env python3
"""Module for function list of school with a specific topic"""


def schools_by_topic(mongo_collection, topic):
    """Getting the list of school having a specific topic"""
    topic_query = {
        'topics': {
            '$elemMatch': {
                '$eq': topic,
            },
        },
    }
    return [doc_list for doc_list in mongo_collection.find(topic_query)]
