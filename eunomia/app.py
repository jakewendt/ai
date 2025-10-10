# ------------------------------------------------------------------------------------
# A basic Shiny Chat example powered by OpenAI.
# ------------------------------------------------------------------------------------
import os

from app_utils import load_dotenv
from chatlas import ChatOpenAI

from shiny.express import ui

import sqlite3
from openai import OpenAI

# ---------- Setup ----------
#_ = load_dotenv(".dbenv")
_ = load_dotenv()

# This dbenv only needs an OPENAI_API_KEY
# No LANGCHAIN_API_KEY is needed as langchain has been removed

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
def generate_sql(question: str, schema: str) -> str:
    prompt = f"""
Database schema:

{schema}

Write a valid SQLite SQL query that answers:
{question}

Return only SQL, no explanations or code fences.
"""
    sql = chat(prompt, role="SQL expert")
    return clean_sql(sql)


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




# ChatOpenAI() requires an API key from OpenAI.
# See the docs for more information on how to obtain one.
# https://posit-dev.github.io/chatlas/reference/ChatOpenAI.html
#load_dotenv()
chat_client = ChatOpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    model="gpt-4o",
    system_prompt="You are a helpful assistant.",
)


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

	prompt = f"""
Database schema:

{schema}

Write a valid SQLite SQL query that answers:
{user_input}

Return only SQL, no explanations or code fences.
"""
	response = await chat_client.stream_async( prompt )

	full_response=""
	async for text_chunk in response:
		full_response += text_chunk


	await chat.append_message_stream(full_response)

	cursor.execute(clean_sql(full_response))
	rows = cursor.fetchall()
	await chat.append_message_stream(str(rows))





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


#	shiny run --reload --launch-browser app_dir/app.py

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

