#	AI

Documenting my AI learning ...




##	20251004

Waiting to get access to UCSF's Versa API

Got access to the private UCSF git https://git.ucsf.edu/academic-research-systems/azure-openai-demo

It contains `Eunomia_DB_demo.ipynb` and `eunomia.sqlite`.
The notebook was out-of-date and didn't work.

I've created an example `dbenv`, but I use my own hidden and not included `.dbenv`.

I updated the notebook and it is now functioning for me.

Nothing in the database or notebook is private so I've included them here.
Credit to the original author, whoever that might be.

Costs about a nickle to run.

Some of these answers are just wrong.

The most obvious change is model from 'text-davinci-003' to 'gpt-3.5-turbo-instruct' 



'text-davinci-003' was deprecated.

https://community.openai.com/t/text-davinci-003-deprecated/582617/3

To drop into your existing code that was using text-davinci-002 or text-davinci-003 (which can follow instructions), you can just specify the new model gpt-3.5-turbo-instruct.

Your prompt and application may need adjustment, because the model has different skills. However, no code change is necessary.

OpenAI python libraries have recently been significantly changed in November, and especially with langchain, you need a fully-compatible stack and calling code. You can revert to openai < 1.0.0 and langchain version that was previously working before half-hearted attempts to update.


https://stackoverflow.com/questions/75774873/openai-api-error-this-is-a-chat-model-and-not-supported-in-the-v1-completions


/v1/completions (Legacy)

• GPT-3.5
• GPT base

• gpt-3.5-turbo-instruct
• babbage-002
• davinci-002


https://community.openai.com/t/gpt-4-vs-3-5-turbo-instruct/447223

Now that its working, try gpt-4 and newer models



