#!/usr/bin/env python
# coding: utf-8

# In[1]:

#This script is a course script for reference
# In realtime prod will need the cert and the other configuration params
# to connect to the oracle cloud

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

import oci #oci package


# In[2]:


# porperties class which loads property values from key of json string from config txt file
# {"model_name":"cohere.command-r-08-2024",
# "embedding_model_name":"cohere.embed-english-v3.0",
# "endpoint":"https://inference.generativeai.eu-frankfurt-1.oci.oraclecloud.com",
# "compartment_ocid":"98737196-C01"
# }

from LoadProperties import LoadProperties 


# In[3]:


props = LoadProperties()


# In[4]:


print(props.getModelName(), props.getEndpoint())


# In[5]:


# help(oci.auth.signers.InstancePrincipalsSecurityTokenSigner)
# class InstancePrincipalsSecurityTokenSigner(oci.auth.signers.security_token_signer.X509FederationClientBasedSecurityTokenSigner)
#  |  InstancePrincipalsSecurityTokenSigner(**kwargs)
#  |  
#  |  A SecurityTokenSigner which uses a security token for an instance principal.  This signer can also
#  |  refresh its token as needed.


# In[6]:


# Use Instance Principals for Authentication
signer = oci.auth.signers.InstancePrincipalsSecurityTokenSigner()



# In[7]:


# Initialize the Generative AI Client
# help(oci.generative_ai_inference.GenerativeAiInferenceClient)


# help documentation
# class GenerativeAiInferenceClient(builtins.object)
#  |  GenerativeAiInferenceClient(config, **kwargs)
#  |  
#  |  OCI Generative AI is a fully managed service that provides a set of state-of-the-art, customizable large language models
#     (LLMs) that cover a wide range of use cases for text generation, summarization, and text embeddings.
#  |  
#  |  Use the Generative AI service inference API to access your custom model endpoints, or to try the out-of-the-box models 
#     to [chat](#/en/generative-ai-inference/latest/ChatResult/Chat), 
#         [generate text](#/en/generative-ai-inference/latest/GenerateTextResult/GenerateText), 
#             [summarize](#/en/generative-ai-inference/latest/SummarizeTextResult/SummarizeText), and 
#                 [create text embeddings](#/en/generative-ai-inference/latest/EmbedTextResult/EmbedText).
#  |  
#  |  To use a Generative AI custom model for inference, you must first create an endpoint for that model. Use the 
#                 [Generative AI service management API](/#/en/generative-ai/latest/) 
#             to [create a custom model](#/en/generative-ai/latest/Model/) by fine-tuning an out-of-the-box model, 
#                 or a previous version of a custom model, using your own data. Fine-tune the custom model on a  
#                     [fine-tuning dedicated AI cluster](#/en/generative-ai/latest/DedicatedAiCluster/). 
#                         Then, create a [hosting dedicated AI cluster](#/en/generative-ai/latest/DedicatedAiCluster/) 
#                             with an [endpoint](#/en/generative-ai/latest/Endpoint/) to host your custom model. 
#                                 For resource management in the Generative AI service, use the 
#                                     [Generative AI service management API](/#/en/generative-ai/latest/).


# generative_ai_inference_client = oci.generative_ai_inference.GenerativeAiInferenceClient(
#     config={},
#     signer=signer,
#     service_endpoint=properties.getEndpoint(),
#     retry_strategy=oci.retry.NoneRetryStrategy(),
#     timeout=(10, 240)
# )


# In[8]:


# Gen AI service client

# '''
# # creates a new service client

# Refer to the above cell for more details on the documentation

# # |      :param dict config:
# # |          Configuration keys and values as per `SDK and Tool Configuration <https://docs.cloud.oracle.com/Content/API/Concepts/sdkconfig.htm>`__.
# # |          The :py:meth:`~oci.config.from_file` method can be used to load configuration from a file. Alternatively, a ``dict`` can be passed. You can validate_config
# # |          the dict using :py:meth:`~oci.config.validate_config`

# # |The connection and read timeouts for the client. The default values are connection timeout 10 seconds and read timeout 
# # 60 seconds. This keyword argument can be provided

# '''

gen_ai_inf_clnt = oci.generative_ai_inference.GenerativeAiInferenceClient(
    config={},
    signer=signer,
    service_endpoint=props.getEndpoint(),
    retry_strategy=oci.retry.NoneRetryStrategy(),
    timeout=(10, 240) #in secs
)


# In[9]:


print(' props endpoint', {props.getEndpoint()})
print(' props model_name', {props.getModelName()})


# In[10]:


# 
# help(oci.generative_ai_inference.models.ChatDetails)
 # |  Details of the conversation for the model to respond.

# help(oci.generative_ai_inference.models.CohereChatRequest())
# |  Details for the chat request for Cohere models.


# '''

# # Parameters of ChatRequest to be known to tune LLM response

# # |  Data descriptors defined here:
# #  |  
# #  |  chat_history
# #  |      Gets the chat_history of this CohereChatRequest.
# #  |      The list of previous messages between the user and the model. The chat history gives the model context for responding to the user's inputs.
# #  |      
# #  |      
# #  |      :return: The chat_history of this CohereChatRequest.
# #  |      :rtype: list[oci.generative_ai_inference.models.CohereMessage]
# #  |  
# #  |  citation_quality
# #  |      Gets the citation_quality of this CohereChatRequest.
# #  |      When FAST is selected, citations are generated at the same time as the text output and the request will be completed sooner. May result in less accurate citations.
# #  |      
# #  |      Allowed values for this property are: "ACCURATE", "FAST"
# #  |      
# #  |      
# #  |      :return: The citation_quality of this CohereChatRequest.
# #  |      :rtype: str
# #  |  
# #  |  documents
# #  |      Gets the documents of this CohereChatRequest.
# #  |      A list of relevant documents that the model can refer to for generating grounded responses to the user's requests.
# #  |      Some example keys that you can add to the dictionary are "text", "author", and "date". Keep the total word count of the strings in the dictionary to 300 words or less.
# #  |      
# #  |      Example:
# #  |      `[
# #  |        { "title": "Tall penguins", "snippet": "Emperor penguins are the tallest." },
# #  |        { "title": "Penguin habitats", "snippet": "Emperor penguins only live in Antarctica." }
# #  |      ]`
# #  |      
# #  |      
# #  |      :return: The documents of this CohereChatRequest.
# #  |      :rtype: list[object]
# #  |  
# #  |  frequency_penalty
# #  |      Gets the frequency_penalty of this CohereChatRequest.
# #  |      To reduce repetitiveness of generated tokens, this number penalizes new tokens based on their frequency in the generated text so far. Greater numbers encourage the model to use new tokens, while lower numbers encourage the model to repeat the tokens. Set to 0 to disable.
# #  |      
# #  |      
# #  |      :return: The frequency_penalty of this CohereChatRequest.
# #  |      :rtype: float
# #  |  
# #  |  is_echo
# #  |      Gets the is_echo of this CohereChatRequest.
# #  |      Returns the full prompt that was sent to the model when True.
# #  |      
# #  |      
# #  |      :return: The is_echo of this CohereChatRequest.
# #  |      :rtype: bool
# #  |  
# #  |  is_force_single_step
# #  |      Gets the is_force_single_step of this CohereChatRequest.
# #  |      When enabled, the model will issue (potentially multiple) tool calls in a single step, before it receives the tool responses and directly answers the user's original message.
# #  |      
# #  |      
# #  |      :return: The is_force_single_step of this CohereChatRequest.
# #  |      :rtype: bool
# #  |  
# #  |  is_raw_prompting
# #  |      Gets the is_raw_prompting of this CohereChatRequest.
# #  |      When enabled, the user’s `message` will be sent to the model without any preprocessing.
# #  |      
# #  |      
# #  |      :return: The is_raw_prompting of this CohereChatRequest.
# #  |      :rtype: bool
# #  |  
# #  |  is_search_queries_only
# #  |      Gets the is_search_queries_only of this CohereChatRequest.
# #  |      When set to true, the response contains only a list of generated search queries without the search results and the model will not respond to the user's message.
# #  |      
# #  |      
# #  |      :return: The is_search_queries_only of this CohereChatRequest.
# #  |      :rtype: bool
# #  |  
# #  |  is_stream
# #  |      Gets the is_stream of this CohereChatRequest.
# #  |      Whether to stream the partial progress of the model's response. When set to true, as tokens become available, they are sent as data-only server-sent events.
# #  |      
# #  |      
# #  |      :return: The is_stream of this CohereChatRequest.
# #  |      :rtype: bool
# #  |  
# #  |  max_tokens
# #  |      Gets the max_tokens of this CohereChatRequest.
# #  |      The maximum number of output tokens that the model will generate for the response.
# #  |      
# #  |      
# #  |      :return: The max_tokens of this CohereChatRequest.
# #  |      :rtype: int
# #  |  
# #  |  message
# #  |      **[Required]** Gets the message of this CohereChatRequest.
# #  |      The text that the user inputs for the model to respond to.
# #  |      
# #  |      
# #  |      :return: The message of this CohereChatRequest.
# #  |      :rtype: str
# #  |  
# #  |  preamble_override
# #  |      Gets the preamble_override of this CohereChatRequest.
# #  |      If specified, the default Cohere preamble is replaced with the provided preamble. A preamble is an initial guideline message that can change the model's overall chat behavior and conversation style. Default preambles vary for different models.
# #  |      
# #  |      Example: `You are a travel advisor. Answer with a pirate tone.`
# #  |      
# #  |      
# #  |      :return: The preamble_override of this CohereChatRequest.
# #  |      :rtype: str
# #  |  
# #  |  presence_penalty
# #  |      Gets the presence_penalty of this CohereChatRequest.
# #  |      To reduce repetitiveness of generated tokens, this number penalizes new tokens based on whether they've appeared in the generated text so far. Greater numbers encourage the model to use new tokens, while lower numbers encourage the model to repeat the tokens.
# #  |      
# #  |      Similar to frequency penalty, a penalty is applied to previously present tokens, except that this penalty is applied equally to all tokens that have already appeared, regardless of how many times they've appeared. Set to 0 to disable.
# #  |      
# #  |      
# #  |      :return: The presence_penalty of this CohereChatRequest.
# #  |      :rtype: float
# #  |  
# #  |  prompt_truncation
# #  |      Gets the prompt_truncation of this CohereChatRequest.
# #  |      Defaults to OFF. Dictates how the prompt will be constructed. With `prompt_truncation` set to AUTO_PRESERVE_ORDER, some elements from `chat_history` and `documents` will be dropped to construct a prompt that fits within the model's context length limit. During this process the order of the documents and chat history will be preserved. With `prompt_truncation` set to OFF, no elements will be dropped.
# #  |      
# #  |      Allowed values for this property are: "OFF", "AUTO_PRESERVE_ORDER"
# #  |      
# #  |      
# #  |      :return: The prompt_truncation of this CohereChatRequest.
# #  |      :rtype: str
# #  |  
# #  |  seed
# #  |      Gets the seed of this CohereChatRequest.
# #  |      If specified, the backend will make a best effort to sample tokens deterministically, such that repeated requests with the same seed and parameters should return the same result. However, determinism cannot be totally guaranteed.
# #  |      
# #  |      
# #  |      :return: The seed of this CohereChatRequest.
# #  |      :rtype: int
# #  |  
# #  |  stop_sequences
# #  |      Gets the stop_sequences of this CohereChatRequest.
# #  |      Stop the model generation when it reaches a stop sequence defined in this parameter.
# #  |      
# #  |      
# #  |      :return: The stop_sequences of this CohereChatRequest.
# #  |      :rtype: list[str]
# #  |  
# #  |  temperature
# #  |      Gets the temperature of this CohereChatRequest.
# #  |      A number that sets the randomness of the generated output. A lower temperature means less random generations.
# #  |      Use lower numbers for tasks such as question answering or summarizing. High temperatures can generate hallucinations or factually incorrect information. Start with temperatures lower than 1.0 and increase the temperature for more creative outputs, as you regenerate the prompts to refine the outputs.
# #  |      
# #  |      
# #  |      :return: The temperature of this CohereChatRequest.
# #  |      :rtype: float
# #  |  
# #  |  tool_results
# #  |      Gets the tool_results of this CohereChatRequest.
# #  |      A list of results from invoking tools recommended by the model in the previous chat turn.
# #  |      
# #  |      
# #  |      :return: The tool_results of this CohereChatRequest.
# #  |      :rtype: list[oci.generative_ai_inference.models.CohereToolResult]
# #  |  
# #  |  tools
# #  |      Gets the tools of this CohereChatRequest.
# #  |      A list of available tools (functions) that the model may suggest invoking before producing a text response.
# #  |      
# #  |      
# #  |      :return: The tools of this CohereChatRequest.
# #  |      :rtype: list[oci.generative_ai_inference.models.CohereTool]
# #  |  
# #  |  top_k
# #  |      Gets the top_k of this CohereChatRequest.
# #  |      A sampling method in which the model chooses the next token randomly from the top k most likely tokens. A higher value for k generates more random output, which makes the output text sound more natural. The default value for k is 0 which disables this method and considers all tokens. To set a number for the likely tokens, choose an integer between 1 and 500.
# #  |      
# #  |      If also using top p, then the model considers only the top tokens whose probabilities add up to p percent and ignores the rest of the k tokens. For example, if k is 20 but only the probabilities of the top 10 add up to the value of p, then only the top 10 tokens are chosen.
# #  |      
# #  |      
# #  |      :return: The top_k of this CohereChatRequest.
# #  |      :rtype: int
# #  |  
# #  |  top_p
# #  |      Gets the top_p of this CohereChatRequest.
# #  |      If set to a probability 0.0 < p < 1.0, it ensures that only the most likely tokens, with total probability mass of p, are considered for generation at each step.
# #  |      
# #  |      To eliminate tokens with low likelihood, assign p a minimum percentage for the next token's likelihood. For example, when p is set to 0.75, the model eliminates the bottom 25 percent for the next token. Set to 1.0 to consider all tokens and set to 0 to disable. If both k and p are enabled, p acts after k.
# #  |      
# #  |      
# #  |      :return: The top_p of this CohereChatRequest.
# #  |      :rtype: float

# '''


# In[11]:


# The OCID string format is ocid1...[REGION][.FUTURE USE]., 
# where ocid1 is the literal string indicating the version of the OCID, resource 
# type is the type of resource, realm is the realm the resource is in, region is the region the 
# resource is in, and unique ID is the unique portion of the ID. The format may vary depending 
# on the type of resource or service. For example, a tenancy OCID looks like ocid1.tenancy.oc1.., 
# and an instance OCID looks like ocid1.instance.oc1.phx.abuw4ljrlsfiqw6vzzxb43vyypt4pkodawglp3wqxjqofakrwvou52gb6s5a.



# In[12]:


# Set Up Chat Request Details
chat_detail = oci.generative_ai_inference.models.ChatDetails()
chat_request = oci.generative_ai_inference.models.CohereChatRequest()

chat_request.message = "How does a telescope work" #input to the model
chat_request.max_tokens = 600 #max output tokens - 600
chat_request.temperature = 1 # lower number represents lower random generations
chat_request.frequency_penalty = 0 #disabled
chat_request.top_p = 0.75 #drop 25% lower output tokens or text of LLM output
chat_request.top_k = 0 #disable the top k "number" of tokens


# Configure Chat Details

# serving mode is either dedicated / on_demand - refer to the below cell for more detail.
chat_detail.serving_mode = oci.generative_ai_inference.models.OnDemandServingMode(model_id=props.getModelName())

chat_detail.chat_request = chat_request 
chat_detail.compartment_id = props.getCompartment() #chat_detail - OCI IAM account.

# print(props.getCompartment()) # 98737196-C01


# In[13]:


# 
# help(oci.generative_ai_inference.models.OnDemandServingMode)

# '''
#  |  The model's serving mode is on-demand serving on a shared infrastructure.

# One of the serving mode is applicable 

#   Data and other attributes inherited from oci.generative_ai_inference.models.serving_mode.ServingMode:
#  |  
#  |  SERVING_TYPE_DEDICATED = 'DEDICATED'
#  |  
#  |  SERVING_TYPE_ON_DEMAND = 'ON_DEMAND'

#  '''
# print(props.getCompartment()) # 98737196-C01


# In[14]:


# Make the Chat Request and Retrieve the Response
chat_response = gen_ai_inf_clnt.chat(chat_detail)

# Print result
print("******************ChatResult******************")
print(vars(chat_response))


# In[ ]:




