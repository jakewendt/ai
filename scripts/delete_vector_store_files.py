#!/usr/bin/env python3

from dotenv import load_dotenv
_ = load_dotenv('.dbenv')

from openai import OpenAI
client = OpenAI()


for vs in client.vector_stores.list():
	print(vs)
	for f in client.vector_stores.files.list(vector_store_id=vs.id):
		print(f)
		print(client.vector_stores.files.delete(
			vector_store_id=vs.id,
			file_id=f.id
		))
		print(client.files.delete(f.id))
	print(client.vector_stores.delete(vector_store_id=vs.id))


#	Delete all files.
#
for f in client.files.list():
	print(f)
	client.files.delete(f.id)

