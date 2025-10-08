#!/usr/bin/env python
# coding: utf-8

# In[20]:


#Demonstration of Embedding LLM model
# Import the necessary libraries
import oci
from LoadProperties import LoadProperties

# Setup basic variables
properties = LoadProperties()


# In[8]:


#For script to run in prod environment.

#-- Start needed params for authentication & authorization

# This 
# METADATA_URL_BASE_ENV_VAR = 'OCI_METADATA_BASE_URL'
# DEFAULT_METADATA_URL_BASE = 'http://169.254.169.254/opc/v2'
# METADATA_URL_BASE = os.environ.get(METADATA_URL_BASE_ENV_VAR, DEFAULT_METADATA_URL_BASE)
# GET_REGION_URL = '{}/instance/region'.format(METADATA_URL_BASE)
# LEAF_CERTIFICATE_URL = '{}/identity/cert.pem'.format(METADATA_URL_BASE)
# LEAF_CERTIFICATE_PRIVATE_KEY_URL = '{}/identity/key.pem'.format(METADATA_URL_BASE)
# INTERMEDIATE_CERTIFICATE_URL = '{}/identity/intermediate.pem'.format(METADATA_URL_BASE)
# METADATA_AUTH_HEADERS = {'Authorization': 'Bearer Oracle'}

# (OR)

# check class oci.generative_ai_inference.GenerativeAiInferenceClient dict. config object
# having the required configuration to connect 
# https://docs.oracle.com/en-us/iaas/Content/API/Concepts/sdkconfig.htm

                # tenancy=config["tenancy"],
                # user=config["user"],
                # fingerprint=config["fingerprint"],
                # private_key_file_location=config.get("key_file"),
                # pass_phrase=get_config_value_or_default(config, "pass_phrase"),
                # private_key_content=config.get("key_content")

#-- End needed params for authentication & authorization


# In[4]:


# Use Instance Principals for Authentication
signer = oci.auth.signers.InstancePrincipalsSecurityTokenSigner()


# In[9]:


# Initialize the Generative AI Client
# Gen AI client which 
generative_ai_inference_client = oci.generative_ai_inference.GenerativeAiInferenceClient(
    config={},
    signer=signer,
    service_endpoint=properties.getEndpoint(),
    retry_strategy=oci.retry.NoneRetryStrategy(),
    timeout=(10, 240)
)


# In[15]:


#Setting up the embedding reqyestr

inputs = ["france"]
embed_text_detail = oci.generative_ai_inference.models.EmbedTextDetails()

# compartment_id
# inputs list of string , words, phrases - each one to be max. of 512 tokens.
# input_types - allowed values are
    ## allowed_values = ["SEARCH_DOCUMENT", "SEARCH_QUERY", "CLASSIFICATION", "CLUSTERING", "IMAGE"]
# serving_mode: null, - OnDemandServingMode or DedicatedServingMode
# truncate - values NONE, START or END

embed_text_detail.serving_mode = oci.generative_ai_inference.models.OnDemandServingMode(
    model_id=properties.getEmbeddingModelName()
)
embed_text_detail.inputs=inputs
embed_text_detail.truncate = "END"
embed_text_detail.compartment_id = properties.getCompartment()


print(embed_text_detail)
# embed_text_detail = oci.generative_ai_inference.models.EmbedTextDetails()


# In[10]:


# # Set up Embedding Request
# # inputs = ["What is the capital of France?"]
# inputs = ["France"]
# embed_text_detail = oci.generative_ai_inference.models.EmbedTextDetails()
# embed_text_detail.serving_mode = oci.generative_ai_inference.models.OnDemandServingMode(
#     model_id=properties.getEmbeddingModelName()
# )
# embed_text_detail.inputs = inputs
# embed_text_detail.truncate = "NONE"
# embed_text_detail.compartment_id = properties.getCompartment()


# In[19]:


# 
embed_text_response = generative_ai_inference_client.embed_text(embed_text_detail)

print('****************Embed Text Result*******************')
# print(type(embed_text_response)) # oci.response.Response

print(embed_text_response.data)


# In[ ]:




