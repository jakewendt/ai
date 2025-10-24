#!/usr/bin/env python3

from dotenv import load_dotenv
_ = load_dotenv()

"""
Reliable demonstration of OpenAI Responses API with vector store + file_search.

- Phase 1: Ask questions without knowledge file (hallucination expected)
- Phase 2: Ask questions with vector store (grounded)
- Includes polling to wait until vector store files are ready
"""

import tempfile
import time
import os
from openai import OpenAI

# --------------------------
# Configuration
# --------------------------
client = OpenAI()  # Ensure OPENAI_API_KEY is set
MODEL = "gpt-4.1-mini"

SYSTEM_INSTR = (
    "You are a helpful assistant. Answer questions using only information "
    "from uploaded knowledge files. Do not assume any external content."
)

# Specific questions anchored to "Morava Virus"
questions = [
    "What is the name of the virus and the disease it causes (Morava Virus)?",
    "How is the Morava Virus transmitted between humans?",
    "What are the main symptoms of Morava Hemorrhagic Fever?",
    "Is there a treatment or vaccine for Morava Hemorrhagic Fever?"
]

# --------------------------
# Phase 1: Ask WITHOUT knowledge file
# --------------------------
print("\n=== PHASE 1: Asking WITHOUT background file ===\n")
for q in questions:
    response = client.responses.create(
        model=MODEL,
        input=[
            {"role": "system", "content": SYSTEM_INSTR},
            {"role": "user", "content": q}
        ]
    )
    answer_text = getattr(response, "output_text", str(response))
    print("Q:", q)
    print("A:", answer_text.strip())
    print("\n" + "-"*60 + "\n")

# --------------------------
# Phase 2: Upload knowledge file and create vector store
# --------------------------

# 1. Create a temporary knowledge file
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

print("Temporary knowledge file created:", tmp_path)

# 2. Upload file to OpenAI
file_upload = client.files.create(file=open(tmp_path, "rb"), purpose="assistants")
file_id = file_upload.id
print("Uploaded file ID:", file_id)

# 3. Create vector store
vector_store = client.vector_stores.create(name="fictional-virus-store")
vector_store_id = vector_store.id
print("Created vector store ID:", vector_store_id)

# 4. Add file to vector store
client.vector_stores.files.create(vector_store_id=vector_store_id, file_id=file_id)
print("Added file to vector store.")

# 5. Poll until the vector store file is ready
def wait_for_vector_store(vector_store_id, timeout=60, interval=2):
    start_time = time.time()
    while True:
        files = client.vector_stores.files.list(vector_store_id=vector_store_id)
        all_ready = all(f.status == "ready" for f in files.data)
        if all_ready:
            print("All files ready in vector store.")
            return True
        if time.time() - start_time > timeout:
            raise TimeoutError("Vector store files did not become ready in time.")
        print("Waiting for vector store files to finish processing...")
        time.sleep(interval)

wait_for_vector_store(vector_store_id)

# --------------------------
# Phase 3: Ask questions WITH file_search
# --------------------------
print("\n=== PHASE 2: Asking WITH file_search vector store ===\n")
for q in questions:
    response = client.responses.create(
        model=MODEL,
        input=[
            {"role": "system", "content": SYSTEM_INSTR},
            {"role": "user", "content": q}
        ],
        tools=[{
            "type": "file_search",
            "vector_store_ids": [vector_store_id]
        }]
    )
    answer_text = getattr(response, "output_text", None)
    if not answer_text:
        try:
            blocks = response.output
            answer_text = blocks[0]["content"][0]["text"]
        except Exception:
            answer_text = str(response)
    print("Q:", q)
    print("A:", answer_text.strip())
    print("\n" + "-"*60 + "\n")

# --------------------------
# Cleanup
# --------------------------
os.remove(tmp_path)
print("Temporary file removed.")

