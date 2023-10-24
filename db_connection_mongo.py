# -------------------------------------------------------------------------
# AUTHOR: Joshua Furman
# FILENAME: db_connection.py
# SPECIFICATION: connecting a new database via MongoDB and Mongocompass
# FOR: CS 4250- Assignment #2
# TIME SPENT: 
# -----------------------------------------------------------*/

# IMPORTANT NOTE: DO NOT USE ANY ADVANCED PYTHON LIBRARY TO COMPLETE THIS CODE SUCH AS numpy OR pandas. You have to work here only with
# standard arrays

# importing some Python libraries
import pprint

# IMPORTANT NOTE: DO NOT USE ANY ADVANCED PYTHON LIBRARY TO COMPLETE THIS CODE SUCH AS numpy OR pandas. You have to
# work here only with standard arrays

# importing some Python libraries
from pymongo import MongoClient
import re


def connectDataBase():
    DB_NAME = "corpus"
    DB_HOST = "localhost"
    DB_PORT = 27017
    try:
        client = MongoClient(host=DB_HOST, port=DB_PORT)
        db = client[DB_NAME]
        return db
    except:
        print("Database not connected successfully")


def createDocument(col, docId, docText, docTitle, docDate, docCat):
    # Create a dictionary to count how many times each term appears in the document.
    # Use space " " as the delimiter character for terms and remember to lowercase them.
    term_count = {}
    terms = docText.lower().split()

    for term in terms:
        if term in term_count:
            term_count[term] += 1
        else:
            term_count[term] = 1

    # Create a list of dictionaries to include term objects.
    term_objects = []
    for term, count in term_count.items():
        term_objects.append({"term": term, "count": count})

    # Producing a final document as a dictionary including all the required document fields
    document = {
        "docId": docId,
        "docText": docText,
        "docTitle": docTitle,
        "docDate": docDate,
        "docCat": docCat,
        "terms": term_objects
    }

    # Insert the document into the collection
    col.insert_one(document)


def deleteDocument(col, docId):
    # Delete the document from the database
    result = col.delete_one({"docId": docId})

    if result.deleted_count == 1:
        print(f"Document with docId {docId} has been deleted.")
    else:
        print(f"No document with docId {docId} found for deletion.")


def updateDocument(col, docId, docText, docTitle, docDate, docCat):
    # Delete the document
    # --> add your Python code here
    deleteDocument(col, docID)

    createDocument(col, docID, docText, doctTitle, docDate, docCat)

    # Create the document with the same id
    # --> add your Python code here


def getIndex(col):
    col = connectDataBase().get_collection("documents")

    # empty dictionary of res
    res = {}

    # Retrieve all documents from the collection
    documents = col.find()

    # Iterate through the documents and update term counts
    for doc in documents:
        title = doc.get("title", "")
        text = doc.get("text", "").lower()
        cleaned_text = re.sub(r'[?!.,]', '', text)
        terms = cleaned_text.split()
        for term in terms:
            if term not in result:
                res[term] = {}
            if title in result[term]:
                res[term][title] += 1
            else:
                res[term][title] = 1

    # Iterate through the term counts and format the output
    formatted_res = {term: {doc: count for doc, count in doc_counts.items()} for term, doc_counts in res.items()}
    for term, doc_counts in formatted_res.items():
        print(f"'{term}': {', '.join([f'{doc}:{count}' for doc, count in doc_counts.items()])}")
    # Query the database to return the documents where each term occurs with their corresponding count. Output example:
    # {'baseball':'Exercise:1','summer':'Exercise:1,California:1,Arizona:1','months':'Exercise:1,Discovery:3'}
    # ...
    # --> add your Python code here
