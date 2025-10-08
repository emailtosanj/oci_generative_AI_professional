#!/usr/bin/env python
# coding: utf-8

# In[6]:


# Read the source file and store chunks in an array
import os

def loadFAQs(directory_path):
   faqs = {}

   for filename in os.listdir(directory_path):
      if filename.endswith(".txt") or filename == 'faq.txt':  # assuming FAQs are in .txt files
         file_path = os.path.join(directory_path, filename)

         with open(file_path) as f:
            raw_faq = f.read()

         filename_without_ext = os.path.splitext(filename)[0]  # remove .txt extension
         faqs[filename_without_ext] = [text.strip() for text in raw_faq.split('=====')]

   return faqs


# In[7]:


# Store data from txt-docs
faqs = loadFAQs('./txt-docs')
faqs


# In[8]:


docs = [{'text': filename + ' | ' + section, 'path': filename} for filename, sections in faqs.items() for section in sections]

# Sample the resulting data
docs[:2]


# In[9]:


print(type(faqs))
for k in faqs.keys():
    print(k)


# In[10]:


docs = [{'text': filename + ' | ' + section, 'path': filename} for filename, sections in faqs.items() for section in sections]


# In[21]:


# print(docs)

# format of faq 
# [ {'text': 'faq | <text>, 'path' : 'faq'}, {'text': 'faq | <text>, 'path' : 'faq'}, ...]


# In[11]:


# Connect to the Oracle Database 23ai
#Declare username and password and dsn (data connection string) - Copy from the activity guide.
un = "vector"
pw = "vector"
cs = "localhost/FREEPDB1"

import oracledb

connection = oracledb.connect(user=un, password=pw, dsn=cs)


# In[16]:


table_name = 'faqs'

with connection.cursor() as cursor:
    # Create the table
    create_table_sql = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id NUMBER PRIMARY KEY,
            payload CLOB CHECK (payload IS JSON),
            vector VECTOR
        )"""
    try:
        cursor.execute(create_table_sql)
    except oracledb.DatabaseError as e:
        raise

    connection.autocommit = True


# In[25]:


# help(SentenceTransformer)

# |  Loads or creates a SentenceTransformer model that can be used to map sentences / text to embeddings.
#      Args:
#  |      model_name_or_path (str, optional): If it is a filepath on disk, it loads the model from that path. If it is not a path,
#  |          it first tries to download a pre-trained SentenceTransformer model. If that fails, tries to construct a model
#  |          from the Hugging Face Hub with that name.


# In[26]:


from sentence_transformers import SentenceTransformer
encoder = SentenceTransformer('all-MiniLM-L12-v2')

# all-MiniLM-L12-v2 - Lama BERT based model - encoder Transformer.


# In[34]:


ppp = 2
print(type(ppp))
fff = f"{ppp}"
print(type(fff))

# help(zip)
# Create and return a new object.


# In[35]:


import array

# Define a list to store the data
data = [
   {"id": idx, "vector_source": row['text'], "payload": row} 
   for idx, row in enumerate(docs)
]

# Collect all texts for batch encoding
texts = [f"{row['vector_source']}" for row in data]

# f"{row['vector_source']}" - converts the data type into a string else wrap the value in to a new string.

# Encode all texts in a batch
# The result of this line is that the embeddings variable will contain a list or array of numerical vectors,
# where each vector corresponds to the semantic representation of the corresponding text in the texts list.
# These embeddings can then be used for various downstream tasks like similarity search, clustering, or classification
# in a vector database.

embeddings = encoder.encode(texts, batch_size=32, show_progress_bar=True)

# Assign the embeddings back to your data structure
for row, embedding in zip(data, embeddings):
   # print(type(embedding)) - numpy.ndarray
   row['vector'] = array.array("f", embedding)


# In[36]:


print(table_name)


# In[41]:


# Insert the chunks + vectors in the database
import json

print(type(data[0]))

with connection.cursor() as cursor:
    # Truncate the table
    cursor.execute(f"truncate table {table_name}")

    prepared_data = [(row['id'], json.dumps(row['payload']), row['vector']) for row in data]

    print(type(prepared_data[0]))


    # Insert the data
    cursor.executemany(
        f"""INSERT INTO {table_name} (id, payload, vector)
        VALUES (:1, :2, :3)""",
        prepared_data
    )

    connection.commit()


# In[22]:


with connection.cursor() as cursor:
    # Define the query to select all rows from a table
    query = f"SELECT * FROM {table_name}"

    # Execute the query
    cursor.execute(query)

    # Fetch all rows
    rows = cursor.fetchall()

    # Print the rows
    for row in rows[:5]:
        print(row)


# In[ ]:




