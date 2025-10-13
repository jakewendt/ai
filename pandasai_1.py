#!/usr/bin/env python3

import os
from dotenv import load_dotenv
_ = load_dotenv('.dbenv')

import pandasai as pai
from pandasai_litellm.litellm import LiteLLM

# Initialize LiteLLM with your OpenAI model
llm = LiteLLM(model="gpt-4.1-mini", api_key=os.environ.get("OPENAI_API_KEY") )

# Configure PandasAI to use this LLM
pai.config.set({
    "llm": llm
})

# Load your data
df = pai.read_csv("GICC_qx_data_documentation_2016-12-21/Background.csv")
#print(df.head())

print("Which questions are about ethnicity?")
response = df.chat("Which questions are about ethnicity?")

#	not real sure how this is AI?
#	SELECT Question, Section, Subject, VariableName, `ReferenceName - Code(s) (0=No input)`
#	FROM table_background
#	WHERE LOWER(Question) LIKE '%ethnicity%'

print(response)


print("Which questions are about race?")
response = df.chat("Which questions are about race?")
print(response)


#Which questions are about ethnicity?
#                                            Question Section               ReferenceName - Code(s) (0=No input)
#0  Do you consider yourself to be Hispanic or Lat...       A  Ethnicity - No input 0 \nEthnicity - Hispanic ...

#Which questions are about race?
#                                            Question Section               ReferenceName - Code(s) (0=No input)
#0                                               None    None  (text of other race is entered here: F:\brain\...
#1  Which best describes your racial or ancestral ...       A  Race - No input 0 \nRace - White 1 \nRace - Bl...

