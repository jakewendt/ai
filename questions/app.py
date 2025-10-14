# ------------------------------------------------------------------------------------
# A basic Shiny Chat example powered by OpenAI.
# ------------------------------------------------------------------------------------

import os
from dotenv import load_dotenv

from shiny.express import ui

import pandas as pd

import openai
from supabase import create_client, Client


# ---------- Setup ----------
_ = load_dotenv()


#	The "new" way using Responses instead of ChatCompletions
#	https://platform.openai.com/docs/api-reference/responses
#from openai import OpenAI
#client = OpenAI()


# Initialize Supabase client
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)



#vector_store = client.vector_stores.retrieve(vector_store_id="vs_68ee6b86db5c8191b7008830991e9657")


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
	#	results = client.vector_stores.search(
	#		vector_store_id=vector_store.id,
	#		query=user_input,
	#		max_num_results=5,		# Defaults to 10
	#		#ranking_options={
	#		#	'ranker': 'auto',
	#		#	'score_threshold': 0.7 # Exclude results with a score below 0.8 default is 0
	#		#},
	#	)
	#	print(results)
	#	print(results.data)
	#
	#	rows=[]
	#	for result in results.data:
	#		print(result.file_id)
	#		print(result.filename)
	#		print(result.score)
	#		all_content=""
	#		for content in result.content:
	#			all_content += content.text
	#		print(all_content)
	#		rows.append([result.score,result.filename,all_content])
	#
	#	await chat.append_message_stream(str(pd.DataFrame(rows).to_markdown(index=False)))

	embedding = openai.embeddings.create(input=user_input, model="text-embedding-3-small", encoding_format="float")
	
	response = supabase.rpc("query_questions", {"query_embedding": embedding.data[0].embedding}).execute()
	#print(response.data)

	await chat.append_message_stream(str(pd.DataFrame(response.data).to_markdown(index=False)))





#	shiny create ......

#	- Install required dependencies:
#	    cd questions
#	    pip install -r requirements.txt
#	- Open and edit the app file: questions/app.py
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


