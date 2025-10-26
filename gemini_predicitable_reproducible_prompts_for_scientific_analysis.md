
Creating predictable, reproducible prompts for scientific analysis requires a systematic approach to structure, clarity, and context. Unlike casual use, scientific prompting should follow a formal framework that minimizes ambiguity and explicitly outlines the desired process and output. This helps to overcome the inherent non-determinism of large language models (LLMs). 

Best practices for reproducible scientific prompting

A prompt for scientific analysis should contain several key elements to ensure replicability. 

Specify a persona or role: Set the AI's identity to activate domain-specific knowledge and ensure the appropriate tone.

Example: "You are a senior data scientist specializing in epidemiology. Your task is to analyze the provided dataset."

Clearly define the task: Use strong action verbs to state the precise objective. Break down complex tasks into a sequence of smaller, manageable steps to avoid broad and unfocused results.

Example: "Task: Perform a descriptive statistical analysis. Step 1: Calculate the mean, median, and standard deviation for each numerical column. Step 2: Identify any outliers in the 'PatientAge' column."

Provide full context and background: Include all relevant information necessary for the analysis. This can involve uploading text, pasting a data schema, or describing the study's purpose.

Example: "The attached CSV file contains anonymized patient data. The study aims to investigate the correlation between patient age and recovery time for a novel antiviral treatment. Columns include 'PatientAge', 'RecoveryTime_Days', and 'TreatmentGroup'."

Structure the desired output: Specify the exact format for the AI's response, such as tables, code snippets, or markdown. Use delimiters like triple quotes to cleanly separate different parts of the prompt.

Example: "Output format: Provide the results in a markdown table. Include the statistical measure, the value for the treatment group, and the value for the control group."

Establish constraints and rules: Tell the AI what to include and what to avoid. This helps to minimize irrelevant or speculative content.

Example: "Rules: Do not speculate on causation. Base conclusions only on the provided data. Do not use external information. Exclude any commentary on the 'PatientID' column."

Define variables and parameters: If applicable, explicitly define all variables and settings the AI should use, such as statistical parameters or specific timeframes.

Example: "Variables: Analyze 'RecoveryTime_Days' as the dependent variable and 'TreatmentGroup' as the independent variable."

Provide examples for few-shot prompting: If you need a very specific style or structure, include examples of the desired output. This can help the AI emulate the correct format and tone.

Example: "Here is an example of a good summary: 'Summary Example: Patients in the treatment group showed a statistically significant reduction in recovery time (mean = 7.2 days, SD = 1.5) compared to the control group (mean = 10.1 days, SD = 2.0).' Produce your summary in the same style." 

Prompt examples for different analysis tasks

Literature review

This prompt helps synthesize current research on a specific topic, identifying key findings and gaps in the literature. 

Prompt Structure

```
You are an expert academic librarian. Your task is to perform a systematic literature review synthesis based on the provided abstracts.

**Task:**
1.  Identify the primary research question or hypothesis of each study.
2.  Summarize the key findings of each study.
3.  Compare and contrast the methodologies used across the studies.
4.  Identify any conflicting results or gaps in the literature.
5.  Suggest at least three potential areas for future research based on these gaps.

**Reference Text (Abstracts):**
"""
[Paste relevant abstracts from papers]
"""

**Output Format:**
-   **Summary Table:** Create a markdown table with columns for Study ID, Research Question, Key Findings, and Methodology.
-   **Contradictions & Gaps:** Provide a bulleted list of any noted conflicts or gaps.
-   **Future Research:** Provide a numbered list of potential research areas.
-   **Citations:** Use the format [Author, Year] to cite specific studies within your analysis.
```

Data analysis and interpretation

This prompt directs the AI to conduct a specific statistical analysis and present the results in a structured, easy-to-read format. 

Prompt Structure

```
You are a senior biostatistician. Your task is to analyze the provided clinical trial data to assess the treatment's effectiveness.

**Context:**
-   **Data:** [Paste a schema or description of your dataset, e.g., "The dataset is a CSV with columns: `PatientID`, `TreatmentGroup` (A or B), `PreTreatment_Score`, `PostTreatment_Score`."]
-   **Objective:** Determine if there is a statistically significant difference in scores between `TreatmentGroup` A and `TreatmentGroup` B after the treatment.

**Task:**
1.  Perform a paired t-test on the `PreTreatment_Score` and `PostTreatment_Score` for each group to see if individual scores changed significantly.
2.  Perform an independent samples t-test to compare the `PostTreatment_Score` between Group A and Group B.
3.  Calculate the effect size (Cohen's d) for the independent samples t-test.

**Output Format:**
-   **Summary Report:** Provide a concise summary of the statistical results.
-   **Statistical Table:** Create a markdown table showing the t-statistic, p-value, and Cohen's d for each test.
-   **Interpretation:** Briefly explain the findings in plain language, suitable for a journal abstract.

**Rules:**
-   Assume a significance level ($$\alpha$$) of 0.05.
-   State the null and alternative hypotheses before each test result.
-   Do not interpret the clinical significance, only the statistical significance.
```

Hypothesis generation

This prompt helps to find potential research questions and explore under-researched areas within a specific scientific field. 

Prompt Structure

```
You are a research scientist specializing in materials engineering. Your task is to generate and evaluate research hypotheses based on the attached research paper.

**Context:**
-   **Research Paper:** [Paste the full text or key sections of the paper]
-   **Background:** The paper explores the synthesis of a new polymer, [Polymer X], but does not extensively test its thermal properties.

**Task:**
1.  Based on the paper's findings, suggest three plausible research questions related to the unexplored thermal properties of [Polymer X].
2.  For each question, propose a specific, testable hypothesis.
3.  Outline a high-level experimental approach to test each hypothesis.
4.  Identify any limitations mentioned in the original paper that could impact the proposed experiments.

**Output Format:**
-   Use clear headers for each section: `Research Question`, `Hypothesis`, `Experimental Approach`.
-   Use bullet points for the experimental steps and limitations.
-   Do not include any information not derived from the original text.
```

