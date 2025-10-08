#!/usr/bin/env python
# coding: utf-8

# In[1]:


from pypdf import PdfReader
import oracledb
import oci
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores.oraclevs import OracleVS
from langchain_community.embeddings import OCIGenAIEmbeddings
from langchain_community.vectorstores.utils import DistanceStrategy
from langchain_core.documents import BaseDocumentTransformer, Document
from LoadProperties import LoadProperties
print("Successfully imported libraries and modules")


# In[2]:


# Setup basic variables
properties = LoadProperties()

#Declare username and password and dsn (data connection string) - Copy from the activity guide.
un = "vector"
pw = "vector"
cs = "localhost/FREEPDB1"

# Connect to the database
try:
    conn23c = oracledb.connect(user=un, password=pw, dsn=cs)
    print("Connection successful!")
except Exception as e:
    print("Connection failed!")


# In[3]:


# RAG Step 1 - Load the document and create pdf reader object

pdf = PdfReader('./pdf-docs/oci-ai-foundations.pdf')

# RAG Step 2 - Transform the document to text

text=""
for page in pdf.pages:
    text += page.extract_text()
print("You have transformed the PDF document to text format")

# RAG Step 3 - Chunk the text document into smaller chunks
text_splitter = CharacterTextSplitter(separator=".",chunk_size=2000,chunk_overlap=100)
chunks = text_splitter.split_text(text)


# In[4]:


# Function to format and add metadata to Oracle 23ai Vector Store

def chunks_to_docs_wrapper(row: dict) -> Document:
    """
    Converts text into a Document object suitable for ingestion into Oracle Vector Store.
    - row (dict): A dictionary representing a row of data with keys for 'id', 'link', and 'text'.
    """
    metadata = {'id': row['id'], 'link': row['link']}
    return Document(page_content=row['text'], metadata=metadata)

# RAG Step 4 - Create metadata wrapper to store additional information in the vector store
"""
Converts a row from a DataFrame into a Document object suitable for ingestion into Oracle Vector Store.
- row (dict): A dictionary representing a row of data with keys for 'id', 'link', and 'text'.
"""
docs = [chunks_to_docs_wrapper({'id': str(page_num), 'link': f'Page {page_num}', 'text': text}) for page_num, text in enumerate(chunks)]


# In[5]:


# RAG Step 5 - Using an embedding model, embed the chunks as vectors into Oracle Database 23ai.

embed_model = OCIGenAIEmbeddings(
    model_id=properties.getEmbeddingModelName(),
    service_endpoint=properties.getEndpoint(),
    compartment_id=properties.getCompartment(),
    auth_type="INSTANCE_PRINCIPAL",
)

# RAG Step 6 - Configure the vector store with the model, table name, and using the indicated distance strategy for the similarity search and vectorize the chunks
# he OracleVS class is a LangChain abstraction that allows you to interact with an Oracle Database 
# configured to store and search vector embeddings.

knowledge_base = OracleVS.from_documents(docs, embed_model, client=conn23c, table_name="DEMO_TABLE", distance_strategy=DistanceStrategy.DOT_PRODUCT)

print("Chunks are stored in the DEMO_TABLE")


# In[ ]:




