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
    print("default prompt used", flush=True)
    prompt = "Provided after these instructions is a list of biological process descriptions. Analyse them to determine whether a unifying theme exists. If no unifying theme is present among the majority, return only this exact sentence: There is no unifying theme among the provided biological processes. If a unifying theme does exist, return a list of broad categories that these processes are involved in, ranked by the number of descriptions that fit into each category. In a following table, assign each category a row and and list all the GO IDs that contribute to that category in the adjacent column. In a final paragraph, maximum 100 words, hypothesise if there is a shared biological process or pathway that is common to all the biological process descriptions provided."
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
