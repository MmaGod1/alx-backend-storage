#!/usr/bin/env python3
"""
list students with average score
"""


def top_students(mongo_collection):
    """ returns all students sorted by average score.
    """
    return mongo_collection.aggregate([
        {
            "$project":
                {
                    "name": "$name",
                    "averageScore": {"$avg": "$topics.score"}
                }
        },
        {
            "$sort":
                {
                    "averageScore": -1
                }
        }
    ])
