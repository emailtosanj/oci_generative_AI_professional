#!/usr/bin/env python
# coding: utf-8

# In[11]:


table_name = 'faqs'
topK = 3

sql = f"""select payload, vector_distance(vector, :vector, COSINE) as score
from {table_name}
order by score
fetch approx first {topK} rows only"""


# In[12]:


# Define the query
question = 'What is Always Free?'


# In[13]:


# Connect to the Oracle Database 23ai
#Declare username and password and dsn (data connection string) - Copy from the activity guide.
un = "vector"
pw = "vector"
cs = "localhost/FREEPDB1"

import oracledb

connection = oracledb.connect(user=un, password=pw, dsn=cs)


# In[15]:


from sentence_transformers import SentenceTransformer
encoder = SentenceTransformer('all-MiniLM-L12-v2')


# In[16]:


# Retrieval Code
import array
import json

with connection.cursor() as cursor:
  embedding = list(encoder.encode(question))
  vector = array.array("f", embedding)

  results  = []

  for (info, score, ) in cursor.execute(sql, vector=vector):
      text_content = info.read()
      results.append((score, json.loads(text_content)))


# In[18]:


# Check results
import pprint
pprint.pp(results)


# In[19]:


from transformers import LlamaTokenizerFast
import sys

tokenizer = LlamaTokenizerFast.from_pretrained("hf-internal-testing/llama-tokenizer")


tokenizer.model_max_length = sys.maxsize

def truncate_string(string, max_tokens):
    # Tokenize the text and count the tokens
    tokens = tokenizer.encode(string, add_special_tokens=True) 
    # Truncate the tokens to a maximum length
    truncated_tokens = tokens[:max_tokens]
    # transform the tokens back to text
    truncated_text = tokenizer.decode(truncated_tokens)
    return truncated_text


# In[20]:


import os

def loadFAQs(directory_path):
   faqs = {}

   for filename in os.listdir(directory_path):
      if filename.endswith(".txt"):  # assuming FAQs are in .txt files
         file_path = os.path.join(directory_path, filename)

         with open(file_path) as f:
            raw_faq = f.read()

         filename_without_ext = os.path.splitext(filename)[0]  # remove .txt extension
         faqs[filename_without_ext] = [text.strip() for text in raw_faq.split('=====')]

   return faqs

faqs = loadFAQs('./txt-docs')

docs = [{'text': filename + ' | ' + section, 'path': filename} for filename, sections in faqs.items() for section in sections]


# In[21]:


# Transform docs into a string array using the "paylod" key
docs_as_one_string = "\n=========\n".join([doc["text"] for doc in docs])
docs_truncated = truncate_string(docs_as_one_string, 1000)


# In[22]:


# Create the LLM Prompt
prompt = f"""\
    <s>[INST] <<SYS>>
    You are a helpful assistant named Oracle chatbot. 
    USE ONLY the sources below and ABSOLUTELY IGNORE any previous knowledge.
    Use Markdown if appropriate.
    Assume the customer is highly technical.
    <</SYS>> [/INST]

    [INST]
    Respond to PRECISELY to this question: "{question}.",  USING ONLY the following information and IGNORING ANY PREVIOUS KNOWLEDGE.
    Include code snippets and commands where necessary.
    NEVER mention the sources, always respond as if you have that knowledge yourself. Do NOT provide warnings or disclaimers.
    =====
    Sources: {docs_truncated}
    =====
    Answer (Three paragraphs, maximum 50 words each, 90% spartan):
    [/INST]
    """


# In[23]:


import oci
from LoadProperties import LoadProperties

# Setup basic variables
properties = LoadProperties()

# Use Instance Principals for Authentication
signer = oci.auth.signers.InstancePrincipalsSecurityTokenSigner()

generative_ai_inference_client = oci.generative_ai_inference.GenerativeAiInferenceClient(config={}, signer=signer, service_endpoint=properties.getEndpoint(), retry_strategy=oci.retry.NoneRetryStrategy(), timeout=(10,240))
chat_detail = oci.generative_ai_inference.models.ChatDetails()
chat_request = oci.generative_ai_inference.models.CohereChatRequest()
chat_request.message = prompt
chat_request.max_tokens = 1000
chat_request.temperature = 0.0
chat_request.frequency_penalty = 0
chat_request.top_p = 0.75
chat_request.top_k = 0

chat_detail.serving_mode = oci.generative_ai_inference.models.OnDemandServingMode(model_id=properties.getModelName())
chat_detail.chat_request = chat_request
chat_detail.compartment_id = properties.getCompartment()
chat_response = generative_ai_inference_client.chat(chat_detail)


# In[24]:


pprint.pp(
    chat_response.data.chat_response.chat_history[1].message
)


# In[ ]:




