#!python

import sys
from pathlib import Path
import ollama
import ssl


job_id = sys.argv[1]
job_folder = Path(__file__).parent.parent / ("WebFrontEnd/Jobs/"+job_id)

# For LINUX
client = ollama.Client(verify=False)

p_path = Path(job_folder) / "prompts.txt"

try:
    my_path = p_path.resolve(strict=True)
except FileNotFoundError:
    print("default prompt used")
    prompt = "You are given a list of biological process descriptions. Analyze them to determine whether a unifying theme exists. If no unifying theme is present among the majority, return only this exact sentence: “There is no unifying theme among the provided biological processes.” If a unifying theme does exist, return a structured response exactly 5 lines long: Line 1: State the broad biological categories the processes fall into. Lines 2–3: Summarize the key processes, grouped by those categories. Lines 4–5: Suggest a shared biological pathway or mechanism linking them. Do not define terms or add explanations. Be concise, structured, and return only the required output." + 'After generating the structured response to the biological process analysis prompt, do the following: Identify a subset of the general themes present in the structured output (e.g., category grouping, process summarization, pathway identification). For each identified theme:     a. List the terms from the output that belong to that theme.     b. Suggest a label that can represent those terms in the context of that theme.     c. Retrieve and include the corresponding Gene Ontology (GO) IDs for each term. Present the result as a 4-column table with the following headers: Theme, Terms from Output, Label to Represent These Terms, GO IDs. Be concise. Do not define the terms or add explanations. Return only the table.'
else:
    with open(p_path, "r") as text_file1:
        prompt = text_file1.read()

with open(job_folder / "go_info.txt", "r") as text_file2:
    GO_descriptions = text_file2.read()

response = client.chat(
    model="gpt-oss:20b",
    messages=[
        {
            "role":"user",
            "content": prompt + "Follow the instructions above, descriptions to summarise start after this sentence." + GO_descriptions
        }
    ]
)

with open(job_folder /'LLMresponse.txt', 'w') as output:
    output.write(response.message.content)

print(response.message.content)
