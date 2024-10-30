#!/usr/bin/env python3
"""
List all MongoDB documents in Python
"""
import pymongo


def list_all(mongo_collection):
    """Create a list to hold the documents"""
    documents = []
    
    for doc in mongo_collection.find():
        documents.append(doc)

    return documents
