#!/usr/bin/env python3

import io

from dotenv import load_dotenv
_ = load_dotenv()

#from openai import OpenAI
#client = OpenAI()

#	https://www.aispaceship.io/docs/category/rag-application

import openai
import os
from supabase import create_client, Client


def create_embedding_openai(text: str):
	response = openai.embeddings.create(input=text, model="text-embedding-3-small", encoding_format="float")
	return response.data[0].embedding


#	needs to be run
#CREATE EXTENSION vector;
#
#CREATE TABLE questions (
#	id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
#	question TEXT NOT NULL,
#	embedding vector(1536),
#);
#
#CREATE OR REPLACE FUNCTION query_questions(query_embedding vector(1536))
#RETURNS TABLE (id BIGINT, question TEXT, similarity FLOAT) AS $$
#BEGIN
#	RETURN QUERY
#	SELECT q.question, 1 - (q.embedding <=> query_embedding) AS similarity
#	FROM questions q;
#END;
#$$ LANGUAGE plpgsql;



# Initialize Supabase client
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def insert_embedding(question: str, embedding: list[float]):
	supabase.table("questions").upsert({"question": question, "embedding": embedding}).execute()



filename="GICC_qx_data_documentation_2016-12-21.txt"

with open(filename, 'r') as file:
	# Iterate over each line in the file object
	i=0
	for line in file:
		# Process each line
		# The 'line' variable will contain the line including the newline character '\n'
		# To remove the newline character, use .strip() or .rstrip()
		processed_line = line.strip()
		if processed_line:
			i+=1
			print(processed_line)
			embedding = create_embedding_openai(processed_line)
			insert_embedding(processed_line, embedding)
			#print(embedding)

