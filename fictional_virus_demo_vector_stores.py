#!/usr/bin/env python3


"""
fictional_virus_demo.py
Demonstration of OpenAI Responses API with and without retrieval context.
"""

from dotenv import load_dotenv
_ = load_dotenv()


"""
Demonstration of the OpenAI Responses API using file_search and vector stores.

- Uploads a fictional virus file.
- Creates a vector store and adds the file.
- Asks multiple questions via Responses API using the vector store for retrieval.
- Prints questions and grounded answers.
"""

import tempfile
import time
from openai import OpenAI

# --------------------------
# Configuration
# --------------------------
client = OpenAI()  # Make sure OPENAI_API_KEY is in your environment
MODEL = "gpt-4.1-mini"  # or gpt-4.1

SYSTEM_INSTR = (
    "You are a helpful assistant. Answer questions using only information "
    "from the attached knowledge files. Do not assume any external content."
)

# Questions about the fictional virus
questions = [
    "What is the name of the virus and what disease does it cause?",
    "How is this virus transmitted between humans?",
    "What are the main symptoms of infection?",
    "Is there a known treatment or vaccine?",
]

# --------------------------
# Step 1: Create temporary knowledge file
# --------------------------
fictional_text = """
Document: Morava Virus (MORV) and Morava Hemorrhagic Fever (MHF)

The Morava Virus (MORV) is a fictional single-stranded RNA virus discovered
in the imaginary region of Valoria. It causes Morava Hemorrhagic Fever (MHF).

Transmission:
Respiratory droplets, contaminated surfaces, and rare prolonged skin contact.

Symptoms:
Fever, muscle aches, nosebleeds, fatigue. Severe: shortness of breath, confusion.

Treatment and vaccine:
No licensed vaccine. Supportive care standard. Experimental antivirals 'moravir'
and 'valovir' show partial benefit early (fictional).
"""

with tempfile.NamedTemporaryFile("w+", suffix=".txt", delete=False) as tmp:
    tmp.write(fictional_text)
    tmp_path = tmp.name

print("Temporary file created:", tmp_path)

# --------------------------
# Step 2: Upload file to OpenAI vector store
# --------------------------
file_upload = client.files.create(file=open(tmp_path, "rb"), purpose="assistants")
file_id = file_upload.id
print("Uploaded file ID:", file_id)

# --------------------------
# Step 3: Create vector store
# --------------------------
vector_store = client.vector_stores.create(name="fictional-virus-store")	#, type="openai")
vector_store_id = vector_store.id
print("Created vector store ID:", vector_store_id)

# --------------------------
# Step 4: Add file to vector store
# --------------------------
#client.vector_stores.add(id=vector_store_id, files=[file_id])
client.vector_stores.files.create(vector_store_id=vector_store_id, file_id=file_id)
print("Added file to vector store. Waiting a few seconds for processing...")
time.sleep(2)  # give vector store time to index

# --------------------------
# Step 5: Ask questions using file_search
# --------------------------
print("\n=== ASKING QUESTIONS USING VECTOR STORE FILE_SEARCH ===\n")

for q in questions:
    response = client.responses.create(
        model=MODEL,
        input=[
            {"role": "system", "content": SYSTEM_INSTR},
            {"role": "user", "content": q},
        ],
        tools=[{
            "type": "file_search",
            "vector_store_ids": [vector_store_id]
        }]
    )

    # Extract text safely
    answer_text = getattr(response, "output_text", None)
    if not answer_text:
        # fallback for newer SDK versions
        try:
            blocks = response.output
            answer_text = blocks[0]["content"][0]["text"]
        except Exception:
            answer_text = str(response)

    print("Q:", q)
    print("A:", answer_text.strip())
    print("\n" + "-"*60 + "\n")

# --------------------------
# Optional cleanup
# --------------------------
import os
os.remove(tmp_path)
print("Temporary file removed.")

# Optional: delete vector store or file if desired
# client.vector_stores.delete(vector_store_id)
# client.files.delete(file_id)

