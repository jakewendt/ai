#!/usr/bin/env python3

import io

from dotenv import load_dotenv
_ = load_dotenv()

from openai import OpenAI
client = OpenAI()

vector_store = client.vector_stores.create(
	name="Survey Questions",
)

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
			#		add to vector store
			#	client.vector_stores.files.upload_and_poll(        # Upload file
			#	    vector_store_id=vector_store.id,
			#	    file=open("customer_policies.txt", "rb")
			#	)
			# 2. Create a BytesIO object from the text
			#file_like_object = io.BytesIO(text_content.encode('utf-8'))
			#file_like_object.name = "my_text_document.txt" # Give it a name for the API

			file_like_object = io.BytesIO(processed_line.encode('utf-8'))
			file_like_object.name = str(i)+".txt"
			uploaded_file = client.files.create(
				file=file_like_object,
				purpose='assistants'
			)
			#client.vector_stores.files.upload_and_poll(
			#	vector_store_id=vector_store.id,
			#	file=file_like_object.name
			#)
			client.vector_stores.files.create(
				vector_store_id=vector_store.id,
				file_id=uploaded_file.id
			)


