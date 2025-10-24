#!/usr/bin/env python3


"""
fictional_virus_demo.py
Demonstration of OpenAI Responses API with and without retrieval context.
"""

from dotenv import load_dotenv
_ = load_dotenv()




"""
fictional_virus_demo_fixed.py

- Demonstrates Responses API calls before and after providing a factual file.
- Avoids ambiguous built-in tools by performing deterministic local retrieval
  (manual RAG). Also uploads the file to OpenAI so you can inspect it via your account.
- Explicitly instructs the model NOT to assume images or hidden context.
"""

import os
import tempfile
import textwrap
import heapq
from openai import OpenAI

# --------------------------
# Configuration
# --------------------------
API_KEY_ENV = "OPENAI_API_KEY"
MODEL = "gpt-4.1-mini"  # use whatever model you have access to
# You can set OPENAI_API_KEY in your environment before running:
# export OPENAI_API_KEY="sk-..."
client = OpenAI()  # uses env var OPENAI_API_KEY

# --------------------------
# Test questions
# --------------------------
questions = [
    "What is the name of the virus and what disease does it cause?",
    "How is this virus transmitted between humans?",
    "What are the main symptoms of infection?",
    "Is there a known treatment or vaccine?",
]

# System instruction to prevent hallucination about images or unseen context
SYSTEM_INSTR = (
    "You are a helpful assistant. IMPORTANT: Do not assume that any image or external "
    "media has been provided. Only use information explicitly supplied in the textual "
    "messages or files. If you do not have enough information to answer, say 'I don't know' "
    "and explain what information would be needed."
)

# --------------------------
# Helper: ask the model
# --------------------------
def ask_model(prompt_text):
    """
    Create a response from the Responses API with a defensive system message.
    Return the raw text.
    """
    # The SDK's response structure can vary by version. The call below is
    # intentionally simple and passes the system + user messages as a single input list.
    resp = client.responses.create(
        model=MODEL,
        input=[
            {"role": "system", "content": SYSTEM_INSTR},
            {"role": "user", "content": prompt_text},
        ],
    )
    # Safe extraction of text: prefer output_text if present, otherwise navigate structure
    if hasattr(resp, "output_text") and resp.output_text:
        return resp.output_text.strip()
    # Newer SDKs return resp.output[0].content[0].text or similar; try to extract robustly:
    try:
        # resp.output is often a list of content blocks
        blocks = resp.output
        if isinstance(blocks, list) and len(blocks) > 0:
            # blocks[0] is often a dict with 'content' which is a list
            content = blocks[0].get("content") if isinstance(blocks[0], dict) else None
            if isinstance(content, list) and len(content) > 0:
                # content[0] could be {"type":"output_text","text":"..."} or similar
                first = content[0]
                # Attempt several common keys
                for k in ("text", "text_content", "output_text"):
                    if isinstance(first, dict) and k in first:
                        return first[k].strip()
                # Fallback: stringify
                return str(first)
    except Exception:
        pass
    # Fallback: stringify the whole response
    return str(resp)

# --------------------------
# Phase 1: Ask before providing the file
# --------------------------
print("\n=== PHASE 1: Asking WITHOUT background file ===\n")
for q in questions:
    ans = ask_model(q)
    print("Q:", q)
    print("A:", ans, "\n")

# --------------------------
# Create a temporary fictional knowledge file
# --------------------------
fictional_text = textwrap.dedent(
    """
    Document: Morava Virus (MORV) and Morava Hemorrhagic Fever (MHF)

    Overview:
    The Morava Virus (MORV) is a fictional single-stranded RNA virus discovered in the
    imaginary region of Valoria. It causes Morava Hemorrhagic Fever (MHF).

    Transmission:
    Transmission occurs primarily via respiratory droplets, contact with contaminated
    surfaces, and in rare cases through prolonged skin contact. Close prolonged exposure
    increases risk; casual brief encounters are less likely to transmit.

    Clinical features:
    Incubation period: 3-7 days.
    Common symptoms: fever, muscle aches, nosebleeds, fatigue.
    Severe presentations: shortness of breath, confusion, dehydration.
    Mortality (untreated): ~5% (fictional estimate).

    Treatment and vaccine:
    There is no licensed vaccine. Supportive care (fluid replacement, fever control)
    is standard. Experimental antivirals 'moravir' and 'valovir' showed partial
    benefit when given early in small trials (fictional).
    """
).strip()

# Write to a temporary file
with tempfile.NamedTemporaryFile("w+", suffix=".txt", delete=False, encoding="utf-8") as tmp:
    tmp.write(fictional_text)
    tmp_path = tmp.name

print("Created temporary file:", tmp_path)

# --------------------------
# Upload file to OpenAI (optional but shown)
# --------------------------
try:
    print("\nUploading file to OpenAI...")
    file_upload = client.files.create(file=open(tmp_path, "rb"), purpose="assistants")
    file_id = getattr(file_upload, "id", None) or file_upload.get("id")
    print("Uploaded. File ID:", file_id)
except Exception as e:
    file_upload = None
    file_id = None
    print("File upload failed or not available in this SDK/environment. Error:", e)
    print("Script will continue using local retrieval only.")

# --------------------------
# Manual RAG: simple keyword-based chunk scoring
# (This ensures deterministic, auditable context.)
# --------------------------
# Break the document into simple chunks (paragraph-level)
chunks = [c.strip() for c in fictional_text.split("\n\n") if c.strip()]

def score_chunk_for_query(chunk, query):
    # Simple heuristic: count shared words (case-insensitive), give small weight to proximity
    q_words = set(w.lower().strip(".,?") for w in query.split())
    c_words = set(w.lower().strip(".,?") for w in chunk.split())
    return len(q_words & c_words)

def retrieve_top_chunks(query, k=2):
    # Return top-k chunks by score; ties broken by chunk order
    scored = []
    for idx, chunk in enumerate(chunks):
        score = score_chunk_for_query(chunk, query)
        # small bias for earlier chunks to stabilize tie-breaking
        scored.append((score, -idx, chunk))
    top = heapq.nlargest(k, scored)
    return [t[2] for t in top if t[0] > 0]  # only return chunks with score > 0

# --------------------------
# Phase 2: Ask WITH appended retrieved chunks (manual RAG)
# --------------------------
print("\n=== PHASE 2: Asking WITH local retrieval (manual RAG) ===\n")
for q in questions:
    retrieved = retrieve_top_chunks(q, k=3)
    # Build a prompt that tells the model the retrieved context is authoritative
    if retrieved:
        context_text = "\n\n".join(retrieved)
        prompt = (
            f"The following passages are authoritative excerpts from a document you were given:\n\n"
            f"{context_text}\n\n"
            f"Using ONLY the passages above (do not assume anything else), answer this question:\n\n{q}"
        )
    else:
        prompt = (
            "You have no relevant passages available. Answer honestly and say you don't know.\n\nQuestion: "
            + q
        )

    ans = ask_model(prompt)
    print("Q:", q)
    print("Retrieved chunks:", bool(retrieved))
    if retrieved:
        print("Context passed to model:\n", context_text, "\n")
    print("A:", ans, "\n")

# --------------------------
# Optional cleanup
# --------------------------
try:
    os.remove(tmp_path)
    print("Temporary file removed.")
except Exception:
    pass

# Optional: if you uploaded the file and want to delete it from OpenAI:
# if file_id:
#     client.files.delete(file_id)
#     print("Deleted uploaded file from OpenAI.")

