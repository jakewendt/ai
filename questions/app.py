# ------------------------------------------------------------------------------------
# A basic Shiny Chat example powered by OpenAI.
# ------------------------------------------------------------------------------------

import os
from dotenv import load_dotenv

from shiny.express import ui

import pandas as pd


# ---------- Setup ----------
_ = load_dotenv()


#	The "new" way using Responses instead of ChatCompletions
#	https://platform.openai.com/docs/api-reference/responses
from openai import OpenAI
client = OpenAI()

#	vector_store = client.vector_stores.retrieve(vector_store_id=vector_store.id)



# Set some Shiny page options
ui.page_opts(
    title="Hello OpenAI Chat. Your input will be compared to questions in the current vector store",
    fillable=True,
    fillable_mobile=True,
)

# Create and display a Shiny chat component
chat = ui.Chat( id="chat" )
chat.ui(
	messages=["Hello! How can I help you today?"]
)

# Store chat state in the url when an "assistant" response occurs
#chat.enable_bookmarking(chat_client, bookmark_store="url")


# Generate a response when the user submits a message
@chat.on_user_submit
async def handle_user_input(user_input: str):
	#
	#	prompt = f"""
	#Database schema:
	#
	#{schema}
	#
	#Write a valid SQLite SQL query that correctly answers:
	#
	#{user_input}
	#
	#Always limit your query to at most 25 results.
	#
	#Return only SQL, no explanations or code fences.
	#"""
	#
	#
	#	#	The "new" way using Responses instead of ChatCompletions
	#	full_response = client.responses.create(
	#		model = "gpt-4.1",
	#		instructions = "You are a helpful assistant.",
	#		input = prompt,
	#		temperature=0,	#	0-2, default is 1.
	#	).output_text
	#
	#	#	The SQL is "pretty" because it SOMETIMES includes ```sql
	#	print(full_response)
	#	full_response=clean_sql(full_response)
	#	await chat.append_message_stream("```sql\n"+full_response+"\n```")
	#	cursor.execute(full_response)
	#	rows = cursor.fetchall()
	#await chat.append_message_stream(str(pd.DataFrame(rows).to_markdown(index=False)))

	response = await chat_client.stream_async(user_input)
	await chat.append_message_stream(response)

#user_query="What is the return policy?"
#results = client.vector_stores.search(
#    vector_store_id=vector_store.id,
#    query=user_query
#max_num_results integer Optional Defaults to 10
#    ranking_options={
#        'ranker': 'auto',
#        'score_threshold': 0.7 # Exclude results with a score below 0.8 default is 0
#    },
#)
#print(results)
#completion = client.chat.completions.create(
#    model="gpt-4.1",
#    messages=[
#        { "role": "developer",
#            "content": "Produce a concise answer to the query based on the provided sources."
#        },
#        { "role": "user",
#            "content": f"Sources: {formatted_results}\n\nQuery: '{user_query}'"
#        }
#    ],
#)
#print(completion.choices[0].message.content)






#	shiny create ......

#	- Install required dependencies:
#	    cd eunomia
#	    pip install -r requirements.txt
#	- Open and edit the app file: eunomia/app.py
#	- Put your OpenAI API key in the `template.env` file and rename it to `.env`.
#	- Run the app with `shiny run app.py`.
#	
#	ℹ Need help obtaining an API key?
#	→ Learn how to obtain one at https://posit-dev.github.io/chatlas/reference/ChatOpenAI.html
#	ℹ Want to learn more about AI chatbots?
#	→ Visit https://shiny.posit.co/py/docs/genai-chatbots.html


#	shiny run --reload --launch-browser ./app.py

#	pip install rsconnect-python
#
#	Not sure what purpose "--name questions" serves but apparently something is required
#		-n, --name TEXT                 The nickname of the Posit Connect server to deploy to.
#	rsconnect add --account jakewendt --name questions --token $( cat ../MYTOKEN )  --secret $( cat ../MYSECRET )
#
#	touch requirements.txt 
#	Not sure what purpose "-n questions" serves but apparently something is required
#		-n, --name TEXT                 The nickname of the Posit Connect server to deploy to.
#	rsconnect deploy shiny -n questions .


