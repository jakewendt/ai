#!/usr/bin/env python3


#	allow_dangerous_code ???



from dotenv import load_dotenv
_ = load_dotenv('.dbenv')

from langchain_openai import ChatOpenAI
from langchain_experimental.agents import create_csv_agent
from langchain.agents.agent_types import AgentType

# Initialize your OpenAI LLM
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo") # Or your preferred OpenAI model

# Define the paths to your CSV files
#csv_files = ["path/to/your/file1.csv", "path/to/your/file2.csv"]
#GICC_qx_data_documentation_2016-12-21/Background.csv
#GICC_qx_data_documentation_2016-12-21/Family_History.csv
#GICC_qx_data_documentation_2016-12-21/Height_and_Weight.csv
#GICC_qx_data_documentation_2016-12-21/Interview_Summary.csv
#GICC_qx_data_documentation_2016-12-21/Medical_Medication_History.csv
#GICC_qx_data_documentation_2016-12-21/Radiation.csv
#GICC_qx_data_documentation_2016-12-21/Tobacco_and_Alcohol.csv
#GICC_qx_data_documentation_2016-12-21/Work_Occupation_Radiation_Expos.csv
#Series_4_qx_documentation_2012-02-25/ABCASE4.csv
#Series_4_qx_documentation_2012-02-25/Bloodqx.csv
#Series_4_qx_documentation_2012-02-25/DEMO4.csv
#Series_4_qx_documentation_2012-02-25/DRUGS.csv
#Series_4_qx_documentation_2012-02-25/HOBBY4.csv
#Series_4_qx_documentation_2012-02-25/KID516.csv
#Series_4_qx_documentation_2012-02-25/PMED4.csv
#Series_4_qx_documentation_2012-02-25/SIB516.csv
#Series_4_qx_documentation_2012-02-25/SIBKID.csv

csv_files = [
"GICC_qx_data_documentation_2016-12-21/Medical_Medication_History.csv",
"Series_4_qx_documentation_2012-02-25/DRUGS.csv",
]

# Create the CSV agent with multiple files
multi_agent = create_csv_agent(
    llm,
    csv_files,
    verbose=True,  # Set to True to see the agent's thought process
    agent_type=AgentType.OPENAI_FUNCTIONS, # Or AgentType.ZERO_SHOT_REACT_DESCRIPTION
)

# Run queries against the agent
query = "Are there any common rows in both datasets? What is the average value of 'column_name' in file1.csv?"
response = multi_agent.run(query)

print(response)


