# ------------------------------------------------------------------------------------
# A basic Shiny Chat example powered by OpenAI.
# ------------------------------------------------------------------------------------

import os
#from pprint import pformat

from app_utils import load_dotenv

from shiny.express import ui

import sqlite3
import pandas as pd


# ---------- Setup ----------
_ = load_dotenv()

# This dbenv only needs an OPENAI_API_KEY
# No LANGCHAIN_API_KEY is needed as langchain has been removed

#	OpenAI
# ChatOpenAI() requires an API key from OpenAI.
# See the docs for more information on how to obtain one.
# https://posit-dev.github.io/chatlas/reference/ChatOpenAI.html
#from chatlas import ChatOpenAI
#chat_client = ChatOpenAI(
#	#api_key=os.environ.get("OPENAI_API_KEY"),
#	model="gpt-4o",
#	#model="gpt-4o-mini",	#	just not as good
#	#system_prompt="You are a helpful assistant.",
#	system_prompt="You are an expert sqlite3 programmer.",
#)


##from openai import OpenAI
##client = OpenAI()

#	Versa API
#from openai import AzureOpenAI
#chat_client = AzureOpenAI(
#	api_key=os.environ.get('API_KEY'),
#	api_version=os.environ.get('API_VERSION'),
#	azure_endpoint=os.environ.get('RESOURCE_ENDPOINT'),
#)



#	The "new" way using Responses instead of ChatCompletions
from openai import OpenAI
client = OpenAI()


DB_PATH = "eunomia.sqlite"
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()


# ---------- Utilities ----------
def get_schema() -> str:
    """Return database schema text for GPT context."""
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    schema = ""
    for (table_name,) in tables:
        cursor.execute(f"PRAGMA table_info({table_name});")
        cols = [c[1] for c in cursor.fetchall()]
        schema += f"Table {table_name}: {cols}\n"
    return schema.strip()


def clean_sql(sql: str) -> str:
    """Remove Markdown fences."""
    sql = sql.strip()
    if sql.startswith("```"):
        sql = sql.split("\n", 1)[-1]
        if sql.endswith("```"):
            sql = sql.rsplit("```", 1)[0]
    return sql.strip()



# ---------- GPT helpers ----------
#def generate_sql(question: str, schema: str) -> str:
#    prompt = f"""
#Database schema:
#
#{schema}
#
#Write a valid SQLite SQL query that answers:
#{question}
#
#Return only SQL, no explanations or code fences.
#"""
#    sql = chat(prompt, role="SQL expert")
#    return clean_sql(sql)


#	def explain_results(question: str, sql: str, rows: list) -> str:
#	    result_text = "\n".join(str(r) for r in rows[:20])
#	    prompt = f"""
#	The user asked: {question}
#	
#	You wrote this SQL:
#	{sql}
#	
#	Results sample:
#	{result_text}
#	
#	Explain the results clearly in everyday language.
#	"""
#	    return chat(prompt, role="data analyst")
#	
#	
#	def summarize_query(question: str, sql: str) -> str:
#	    prompt = f"""
#	The user asked: {question}
#	
#	You wrote this SQL:
#	{sql}
#	
#	Explain briefly, in human-readable terms, what this SQL query is doing
#	and how it answers the question.
#	"""
#	    return chat(prompt, role="SQL explainer")


# ---------- Main entry point ----------
#	def ask_question(
#	    question: str,
#	    include_sql: bool = True,
#	    explain_results_flag: bool = True,
#	    human_summary: bool = True,
#	    max_retries: int = 3,
#	):
#	    """
#	    Generate SQL, run it, retry if needed, and optionally include explanations.
#	    Returns dict with sql, rows, explanation, summary, or error.
#	    """
#	    schema = get_schema()
#	    sql = generate_sql(question, schema)
#	
#	    rows = []
#	    error = None
#	
#	    for attempt in range(1, max_retries + 1):
#	        try:
#	            cursor.execute(sql)
#	            rows = cursor.fetchall()
#	            break  # success
#	        except Exception as e:
#	            error = str(e)
#	            if attempt < max_retries:
#	                # Ask GPT to fix its SQL
#	                fix_prompt = f"""
#	The following SQL caused an error when executed on SQLite:
#	
#	SQL:
#	{sql}
#	
#	Error:
#	{error}
#	
#	Schema:
#	{schema}
#	
#	Please correct the SQL so that it will run successfully on this schema.
#	Return only corrected SQL.
#	"""
#	                sql = clean_sql(chat(fix_prompt, role="SQL debugger"))
#	            else:
#	                return {"error": error, "sql": sql}
#	
#	    result = {"rows": rows}
#	    if include_sql:
#	        print("\n--- SQL ---")
#	        print(sql)
#	        result["sql"] = sql
#	    print("\n--- Rows ---")
#	    print(rows)
#	    if human_summary:
#	        print("\n--- Generating summary ---")
#	        result["summary"] = summarize_query(question, sql)
#	        print("\n--- Summary ---\n", result["summary"])
#	    if explain_results_flag and rows:
#	        print("\n--- Explaining results ---")
#	        result["explanation"] = explain_results(question, sql, rows)
#	        print("\n--- Explanation ---\n", result["explanation"])
#	
#	    print("\n=== Done ===")
#	    
#	    return result




#messages=[
#	# The system content below shapes the behavior of the model. For instance, you could instruct the model to only answer in French.
#	{"role": "system", "content": 'You are a helpful AI assistant'}, 
#	{"role": "user", "content": 'This is a test'}  # The content contains your prompt
#]



# Set some Shiny page options
ui.page_opts(
    title="Hello OpenAI Chat. Your question will be converted to SQL to query the Eunomia database",
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

	schema = get_schema()
	#sql = generate_sql(question, schema)
	#response = await chat_client.stream_async( user_input )

#sqlite_prefix = '''You are an agent designed to interact with a SQLite database.
#Given an input question, create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
#Always limit your query to at most {top_k} results.
#You can order the results by a relevant column to return the most interesting examples in the database.
#Only query for all the columns from a specific table if asked--otherwise, only ask for the relevant columns given the question.
#You have access to tools for interacting with the database. 
#
#If you get an error while executing a query, rewrite the query and try again.
#DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.
#If the question does not seem related to the database, just return "I don\'t know" as the answer.
#Do not surround the sql query with quotes.
#The data is standardized to OMOP 5.3.
#All table names should be converted to upper case in this database
#Do NOT quote table names when passing as action input


	prompt = f"""
Database schema:

{schema}

Write a valid SQLite SQL query that correctly answers:

{user_input}

Always limit your query to at most 25 results.

Return only SQL, no explanations or code fences.
"""


	#	OpenAI
	#response = await chat_client.stream_async( prompt )
	#full_response=""
	#async for text_chunk in response:
	#	full_response += text_chunk
	
	#	Versa API
	#full_response = chat_client.chat.completions.create(
	#	#model = 'gpt-4o-mini-2024-07-18',
	#	model = 'gpt-5-mini-2025-08-07',
	#	messages=[
	#		{"role": "system", "content": "You are an expert sqlite3 programmer."},
	#		{"role": "user", "content": prompt }
	#	]
	#).choices[0].message.content

	#	The "new" way using Responses instead of ChatCompletions
	full_response = client.responses.create(
		model = "gpt-4.1",
		#input="You are an expert sqlite3 programmer.",
		instructions = "You are a helpful assistant.",
		input = prompt,
		#input = [
		#	{ "role": "system", "content": "You are a helpful assistant." },
		#	{ "role": "user", "content": prompt }
		#]
	).output_text

	#	The SQL is "pretty" because it SOMETIMES includes ```sql
	print(full_response)
	full_response=clean_sql(full_response)
	await chat.append_message_stream("```sql\n"+full_response+"\n```")
	#print(full_response)
	cursor.execute(full_response)
	rows = cursor.fetchall()
	#print(str(rows))

	#await chat.append_message_stream(pformat(rows))
	#await chat.append_message_stream("```"+str(rows)+"```")
	#await chat.append_message_stream(str(rows.to_markdown(index=False)))
	#await chat.append_message_stream(str(pd.DataFrame(rows).to_markdown(index=False)))
	await chat.append_message_stream(str(pd.DataFrame(rows).to_markdown()))





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
#	Not sure what purpose "--name eunomia" serves but apparently something is required
#		-n, --name TEXT                 The nickname of the Posit Connect server to deploy to.
#	rsconnect add --account jakewendt --name eunomia --token $( cat ../MYTOKEN )  --secret $( cat ../MYSECRET )
#
#	touch requirements.txt 
#	Not sure what purpose "-n eunomia" serves but apparently something is required
#		-n, --name TEXT                 The nickname of the Posit Connect server to deploy to.
#	rsconnect deploy shiny -n eunomia .


#			What is the number of males and females that are prescribed the top 10 prescribed drugs




