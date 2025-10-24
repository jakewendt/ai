#!/usr/bin/env python3


"""
fictional_virus_demo.py
Demonstration of OpenAI Responses API with and without retrieval context.
"""

from dotenv import load_dotenv
_ = load_dotenv()



#!/usr/bin/env python3
import time
import openai
from openai import OpenAI

client = OpenAI()

# ----------------------------
# 1. Create a temporary file
# ----------------------------
DOCUMENT_TEXT = """\
The Morava Virus is a fictional virus described in this document.
It causes a disease known as Morava Hemorrhagic Fever.
Transmission occurs through contact with infected bodily fluids.
Symptoms include fever, vomiting, muscle pain, and bleeding.
There is currently no treatment or vaccine for this disease.
"""

with open("morava_virus.txt", "w") as f:
    f.write(DOCUMENT_TEXT)

print("Created local file: morava_virus.txt")

# ----------------------------
# 2. Upload file
# ----------------------------
file_obj = client.files.create(file=open("morava_virus.txt", "rb"), purpose="assistants")
file_id = file_obj.id
print(f"Uploaded file ID: {file_id}")

# ----------------------------
# 3. Create vector store and attach file
# ----------------------------
vector_store = client.vector_stores.create(name="MoravaVirusDemo")
vector_store_id = vector_store.id
print(f"Created vector store ID: {vector_store_id}")

client.vector_stores.file_batches.create(
    vector_store_id=vector_store_id,
    file_ids=[file_id],
)
print("Added file to vector store.")

# ----------------------------
# 4. Wait for indexing to finish
# ----------------------------
def wait_for_vector_store(client, vector_store_id, timeout=120, interval=5):
    print("Waiting for vector store files to finish processing...")
    start = time.time()
    while time.time() - start < timeout:
        vs = client.vector_stores.retrieve(vector_store_id)
        counts = vs.file_counts
        if counts.completed == counts.total:
            print("✅ Vector store is ready.")
            return
        time.sleep(interval)
        print("Still processing...")
    raise TimeoutError("Vector store did not become ready in time.")

wait_for_vector_store(client, vector_store_id)

# ----------------------------
# 5. Strict factual prompt
# ----------------------------
SYSTEM_PROMPT = """\
You are a factual assistant. 
You must never speculate or assume information.
If you don't find information explicitly stated in the uploaded files or in reliable knowledge, respond clearly that you have no verified information.

Rules:
- If the virus or disease is not mentioned in the provided document, say so plainly.
- Do not guess, infer, or fill in gaps.
- If asked about something fictitious not found in the text, respond:
  "I have no verified information about that."

Example:
Q: What is the Morava Virus?
A: I have no verified information about that.
"""

# ----------------------------
# 6. Questions
# ----------------------------
questions = [
    "What is the Morava Virus and the disease it causes?",
    "How is the Morava Virus transmitted between humans?",
    "What are the symptoms of Morava Hemorrhagic Fever?",
    "Is there a treatment or vaccine for Morava Hemorrhagic Fever?",
]

def ask_questions(client, questions, vector_store_id=None):
    phase = "PHASE 2: Asking WITH vector store" if vector_store_id else "PHASE 1: Asking WITHOUT background file"
    print(f"\n=== {phase} ===\n")

    tools = []
    if vector_store_id:
        tools = [{"type": "file_search", "vector_store_ids": [vector_store_id]}]

    for q in questions:
        response = client.responses.create(
            model="gpt-4.1",
            input=[{"role": "system", "content": SYSTEM_PROMPT},
                   {"role": "user", "content": q}],
            tools=tools,
        )
        answer = response.output_text.strip()
        print(f"Q: {q}\nA: {answer}\n{'-'*60}")

# ----------------------------
# 7. Run both phases
# ----------------------------
ask_questions(client, questions)  # Phase 1: no background file
ask_questions(client, questions, vector_store_id)  # Phase 2: with file_search

print("\n✅ Demo complete.")


