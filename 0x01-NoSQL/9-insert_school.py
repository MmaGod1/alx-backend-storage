#!/usr/bin/env python3
"""
Insert a new document
"""
import pymongo


def insert_school(mongo_collection, **kwargs):
    """
    insert a documents into a collection
    """
    doc = mongo_collection.insert_one(kwargs)
    return doc.inserted_id
