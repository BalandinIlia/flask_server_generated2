import os
import tempfile
from functools import reduce

from bson import ObjectId
from pymongo import MongoClient

#connection string for mongoDB database
connection_string = "mongodb+srv://iliabalandin:qzoupnBmnDKzKvcF@cluster0.8ajxt.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(connection_string)
db = client['students_db']
students_collection = db['students']

def add(student=None):
    query = {
        "first_name": student.first_name,
        "last_name": student.last_name
    }
    res = students_collection.find_one(query)
    if res:
        return 'already exists', 409

    student_data = student.to_dict()
    result = students_collection.insert_one(student_data)
    student.student_id = str(result.inserted_id)
    return student.student_id


def get_by_id(student_id=None, subject=None):
    student = students_collection.find_one({"_id": ObjectId(student_id)})
    if not student:
        return 'not found', 404
    return student


def delete(student_id=None):
    result = students_collection.delete_one({"_id": ObjectId(student_id)})
    if result.deleted_count == 0:
        return 'not found', 404
    return student_id