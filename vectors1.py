#!/usr/bin/env python3


#	Very loosely from https://python.langchain.com/docs/tutorials/rag/


from dotenv import load_dotenv
import langchain
import openai
import os
import urllib
_ = load_dotenv('.dbenv')


from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

from langchain_core.vectorstores import InMemoryVectorStore

vector_store = InMemoryVectorStore(embeddings)

from langchain_core.documents import Document

documents=[
	Document(id="1", page_content="cat", metadata={"baz": "bar"}),
	Document(id="2", page_content="pet store", metadata={"bar": "baz"}),
	Document(id="3", page_content="i will be deleted :("),
	Document(id="4", page_content="Ice cream sundae"),
]

#documents = [document_1, document_2, document_3]
vector_store.add_documents(documents=documents)

import pprint

print("Kitten")
pprint.pprint(vector_store.similarity_search_with_score("kitten"))

print("Milk")
pprint.pprint(vector_store.similarity_search_with_score("milk"))



