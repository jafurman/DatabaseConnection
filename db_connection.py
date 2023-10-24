# -------------------------------------------------------------------------
# AUTHOR: Joshua Furman
# FILENAME: dc_connection.py
# SPECIFICATION: database connection
# FOR: CS 4250- Assignment #2
# TIME SPENT:
# -----------------------------------------------------------*/

# IMPORTANT NOTE: DO NOT USE ANY ADVANCED PYTHON LIBRARY TO COMPLETE THIS CODE SUCH AS numpy OR pandas. You have to
# work here only with standard arrays

# importing some Python libraries
import psycopg2
from psycopg2.extras import RealDictCursor
import re


def connectDataBase():
    # Create a database connection object using psycopg2
    DB_name = "4250HM2"
    DB_user = "postgres"  # You might want to check if this is the correct username
    DB_pass = "123"
    DB_host = "localhost"
    DB_port = "5432"
    try:
        connection = psycopg2.connect(database=DB_name, user=DB_user, password=DB_pass, host=DB_host, port=DB_port, cursor_factory=RealDictCursor)
        return connection
    except Exception as e:
        print(f"Connection error: {e}")
        return None


def createCategory(cur, catId, catName):
    # Insert a category in the database
    sql = "Insert into categories (id, name) Values (%s, %s)"
    recset = [catId, catName]
    cur.execute(sql, recset)


def createDocument(cur, docId, docText, docTitle, docDate, docCat):
    # 1 Get the category id based on the informed category name
    sql = 'Select id from categories where name = %s'
    recset = [docCat]
    cur.execute(sql, recset)
    id = cur.fetchall()[0]["id"]

    sql = 'Select title from documents'
    recset = [docText]
    cur.execute(sql, recset)
    string = recset[0]
    cstring = re.sub(r'[!.?\s]', '', string)
    numchars = len(cstring)

    # 2 Insert the document in the database. For num_chars, discard the spaces and punctuation marks.
    sql = "Insert into documents (docnum, text, title, numchars, date, category_id) Values (%s, %s, %s, %s, %s, %s)"
    recset = [docId, docText, docTitle, numchars, docDate, id]
    cur.execute(sql, recset)

    # 3 Update the potential new terms.
    cstring2 = re.sub(r'[?!.]', '', string)
    theTerm = cstring2.lower().split()
    sql = 'Select * from terms where term = %s'
    for i in theTerm:
        recset = [i]
        cur.execute(sql, recset)
        if cur.fetchall():
            hello = 0
        else:
            num_charTerm = len(i)
            sql2 = 'Insert into terms (term, numchars) Values (%s, %s)'
            recset = [i, num_charTerm]
            cur.execute(sql2, recset)
    tc = {}
    for word in theTerm:
        if word in tc:
            tc[word] += 1
        else:
            tc[word] = 1

    for term, count in tc.items():
        newTerm = term
        newCount = count
        sql = 'Insert into index (docnum, term, count) Values (%s, %s, %s)'
        recset = [docId, newTerm, newCount]
        cur.execute(sql, recset)


def deleteDocument(cur, docId):
    # 1 Query the index based on the document to identify terms 1.1 For each term identified, delete its occurrences
    # in the index for that document 1.2 Check if there are no more occurrences of the term in another document. If
    # this happens, delete the term from the database.
    sql = 'Select term from index where docNum = %s'
    recset = [docId]
    cur.execute(sql, recset)
    test = cur.fetchall()
    for term in test:
        delete_term = term["term"]
        sql2 = 'Delete from index where term = %s'
        recset = [delete_term]
        cur.execute(sql2, recset)

    # 2 Delete the document from the database
    sql = "Delete from documents where docnum = %(docId)s"
    cur.execute(sql, {'docId': docId})


def updateDocument(cur, docId, docText, docTitle, docDate, docCat):
    # 1 Delete the document
    deleteDocument(cur, docId)

    # 2 Create the document with the same id
    createDocument(cur, docId, docText, docTitle, docDate, docCat)


def getIndex(cur):
    sql = 'SELECT index.term, documents.title, count(*) AS count FROM index INNER JOIN documents ON index.docNum = ' \
          'documents.docnum GROUP BY term, title'
    cur.execute(sql)
    result = cur.fetchall()
    term_occur = {}
    for row in result:
        term = row['term']
        doc = row['title']
        count = row['count']
        if term in term_occur:
            term_occur[term] += f',{doc}:{count}'
        else:
            term_occur[term] = f'{doc}:{count}'

    for term, occurrences in term_occur.items():
        print(f"'{term}':'{occurrences}'")
