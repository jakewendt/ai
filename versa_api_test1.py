#!/usr/bin/env python3

import os

from dotenv import load_dotenv
_ = load_dotenv('.dbenv')

from openai import AzureOpenAI
client = AzureOpenAI(
	api_key=os.environ.get('API_KEY'),
	api_version=os.environ.get('API_VERSION'),
	azure_endpoint=os.environ.get('RESOURCE_ENDPOINT'),
)

print(client)


# messages must be a list of dicts in the following format. The system role is optional, but a user role is required.
messages=[
	# The system content below shapes the behavior of the model. For instance, you could instruct the model to only answer in French.
	{"role": "system", "content": 'You are a helpful AI assistant'}, 
	{"role": "user", "content": 'This is a test'}  # The content contains your prompt
]

# Define an Azure deployment ID, which implies a model id, and assign it to the model parameter below
deployment = 'gpt-4o-mini-2024-07-18'

# Using the client, create a chat completions API call. This will send the prompt when you run this cell.
response = client.chat.completions.create(
	model=deployment,
	messages=messages,
)

# The response is an OpenAI ChatCompletion object, from which we can extract various content and metadata
print(type(response))

print(response)




system_prompt = """You are an AI assistant whose job is to analyze clinical notes and infer all relevant ICD9 and ICD10 codes from the note. 
Take a deep breath and carefully review each note before responding, as mistakes may result in inaccurate billing or even fatal medical errors.
Return a JSON object containing your results using the format in the following example:

{
    "ICD9": {
        "codes": [
            {"123.4": "Example Description 1"},
            {"567.8": "Example Description 2"},
            {"910.11": "Example Description 3"}
        ],
    "ICD10": {
        "codes": [
            {"ABC12": "Example Description A"},
            {"DEF34": "Example Description B"},
            {"GHI56": "Example Description C"},
        ]
    }
}

where count is an integer count of unique codes, and codes is an list of codes paired with matching descriptions.

Do not return any comments outside the above JSON data structure.
"""

# This is an LLM generated clinical note
test_note = '''EXTREMITY WITH CONTRAST: 01/01/2030    COMPARISON:  Pelvic MRI dated 01/01/2028    CLINICAL HISTORY: 45-year-old woman with suspected uterine fibroid. This is a follow-up examination.

TECHNIQUE: Multiple sequences were obtained according to the standard pelvic MRI protocol before and after intravenous administration of contrast.

FINDINGS:
Well-defined, oval-shaped T1 hypointense and T2 hyperintense mass within the myometrium measuring 5 cm x 4 cm x 3.8 cm (AP x CL x CC). The mass enhances heterogeneously after gadolinium administration with central areas showing more intense enhancement. There is a small amount of surrounding edema noted in the adjacent myometrium. No other significant abnormalities are seen in the pelvic organs.

IMPRESSION:
1. Compared to prior examination, there has been no significant interval change in the size and imaging characteristics of the suspected uterine fibroid within the myometrium, measuring approximately 5 cm x 4 cm x 3.8 cm.
2. No additional masses or abnormalities identified in the pelvic organs.

END OF IMPRESSION:'''

messages=[
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": f"Please extract BOTH ICD9 and ICD10 codes from this clinical note: {test_note}"}
]

#deployment = 'gpt-4'
n = 3

response = client.chat.completions.create(
    model=deployment,
    messages=messages,
    n=n,
)
print(response)

response.model_dump()


