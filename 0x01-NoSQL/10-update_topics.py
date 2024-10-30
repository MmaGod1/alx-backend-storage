#!/usr/bin/env python3
"""
Changes all topics of a school document based on the name.
"""
import pymongo


def update_topics(mongo_collection, name, topics):
    """
    update document with a new topics.
    """
    mongo_collection.update_many(
        {"name": name},
        {"$set": {"topics": topics}}
    )
