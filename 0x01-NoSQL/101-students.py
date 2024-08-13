#!/usr/bin/env python3
"""Module for function that returns all students sorted by avg score"""


def top_students(mongo_collection):
    """Getting and print all students sorted by avg score"""
    avg_student = mongo_collection.aggregate(
        [
            {
                '$project': {
                    '_id': 1,
                    'name': 1,
                    'averageScore': {
                        '$avg': {
                            '$avg': '$topics.score',
                        },
                    },
                    'topics': 1,
                },
            },
            {
                '$sort': {'averageScore': -1},
            },
        ]
    )
    return avg_student
