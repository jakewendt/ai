#!/usr/bin/env python3

#	https://platform.openai.com/docs/guides/retrieval

import time
from dotenv import load_dotenv
_ = load_dotenv('.dbenv')

from openai import OpenAI
client = OpenAI()

def format_results(results):
    formatted_results = ''
    for result in results.data:
        formatted_result = f"<result file_id='{result.file_id}' file_name='{result.filename}'>"
        for part in result.content:
            formatted_result += f"<content>{part.text}</content>"
        formatted_results += formatted_result + "</result>"
    return f"<sources>{formatted_results}</sources>"

for vs in client.vector_stores.list():
	print(vs)
	client.vector_stores.delete( vector_store_id=vs.id)

#quit()

vector_store = client.vector_stores.create(        # Create vector store
    name="Support FAQ",
)

client.vector_stores.files.upload_and_poll(        # Upload file
    vector_store_id=vector_store.id,
    file=open("customer_policies.txt", "rb")
)

#print(vector_store.status) 
#print(vector_store.file_counts) 
#vector_store = client.vector_stores.retrieve(vector_store_id=vector_store.id)
time.sleep(1) 
print(vector_store.status) 
print(vector_store.file_counts) 


#	Sometimes this fails. Sound like the vector_store needs more time or refresh / reloaded?
#	completed
#	FileCounts(cancelled=0, completed=0, failed=0, in_progress=0, total=0)
#	SyncPage[VectorStoreSearchResponse](data=[], object='vector_store.search_results.page', search_query=['What is the return policy?'], has_more=False, next_page=None)
#	<sources></sources>
#	
#	I'm sorry, but there are no sources provided to reference the specific return policy. Please provide relevant sources or details about the store or company in question, and I can give you a concise answer.
#
#	Sleeping for a second seems to resolve even though the object still shows no files
#	FileCounts(cancelled=0, completed=0, failed=0, in_progress=0, total=0)





user_query="What is the return policy?"
results = client.vector_stores.search(
    vector_store_id=vector_store.id,
    query=user_query
)
print(results)

#	Can't send .data as the first thing it does is look for it.
formatted_results = format_results(results)	#.data)
print(formatted_results)

#	What's the point of this ...
#'\n'.join('\n'.join(c.text) for c in result.content[0] for result in formatted_results.data)

completion = client.chat.completions.create(
    model="gpt-4.1",
    messages=[
        {
            "role": "developer",
            "content": "Produce a concise answer to the query based on the provided sources."
        },
        {
            "role": "user",
            "content": f"Sources: {formatted_results}\n\nQuery: '{user_query}'"
        }
    ],
)
print()
print()
print(completion.choices[0].message.content)
print()
print()




#	#	sometimes this returns nothing??
#	print(results.data[0].score)	#.content[0].text)
#	#print(results[0].data)
#	
#	results = client.vector_stores.search(
#	    vector_store_id=vector_store.id,
#	    query="How many woodchucks are allowed per passenger?",
#	)
#	
#	print(results.data[0].score)	#.content[0].text)
#	#print(results[0].data)


