#!/usr/bin/env python3

#	https://www.aispaceship.io/docs/category/rag-application

import openai
import os
from supabase import create_client, Client
from dotenv import load_dotenv

_ = load_dotenv('.dbenv')

#openai.api_key = os.environ.get("OPENAI_API_KEY")

def create_embedding_openai(text: str):
	response = openai.embeddings.create(input=text, model="text-embedding-3-small", encoding_format="float")
	return response.data[0].embedding


#	needs to be run
#CREATE EXTENSION vector;
#
#CREATE TABLE docs (
#    doc_name TEXT NOT NULL,
#    embedding vector(1536),
#    PRIMARY KEY (doc_name)
#);


# Initialize Supabase client
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def insert_embedding(doc_name: str, embedding: list[float]):
	supabase.table("docs").upsert({"doc_name": doc_name, "embedding": embedding}).execute()

#def get_embedding(doc_name: str) -> list[float]:
#	response = supabase.table("embeddings").select("embedding").eq("doc_name", doc_name).execute()
#	return response.data[0]["embedding"]

def create_embedding_from_files(files: list[str]):
	for file in files:
		with open(file, "r") as f:
			text = f.read()
			embedding = create_embedding_openai(text)
			insert_embedding(file, embedding)


#	needs to be run
#CREATE OR REPLACE FUNCTION query_documents(query_embedding vector(1536))
#RETURNS TABLE (doc_name TEXT, similarity FLOAT) AS $$
#BEGIN
#    RETURN QUERY
#    SELECT d.doc_name, 1 - (d.embedding <=> query_embedding) AS similarity
#    FROM docs d;
#END;
#$$ LANGUAGE plpgsql;

def query_embedding(query: str):
	embedding = create_embedding_openai(query)
	response = supabase.rpc("query_documents", {"query_embedding": embedding}).execute()
	return response



def main():
	#create_embedding_from_files(["doc1.txt", "doc2.txt"])
	response = query_embedding("dog")
	print(response)

main()

#	Enabling RLS breaks this. Not sure why or how to fix. Supabase seems to think I need it.

#	Think I need to add a policy after enabling this.

