#!python

import sys
from pathlib import Path
import ollama
import truststore
import ssl


job_id = sys.argv[1]
job_folder = job_id
'''
job_folder = Path(__file__).parent / "WebFrontEnd/Jobs/"+job_id
'''

''' 
# For MAC/Windows
client = ollama.Client(
    host="https://capstone.babraham.ac.uk/ollama/XGYXYIITAEVTMPVZZGQD/",
    verify=truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
)
'''
# For LINUX
client = ollama.Client(
    host="https://capstone.babraham.ac.uk/ollama/CYLVVWWXZRHDQLRVJEKB/",
    verify=False)

p_path = Path(job_folder + "/prompts.txt")

try:
    my_path = p_path.resolve(strict=True)
except FileNotFoundError:
    print("default prompt used, please set a prompt for better performance")
    prompt = "Provided below is a list of descriptions of biological processes. First identify the broad categories that these processes are involved in and provide these as a list. Then, in a seperate paragraph, identify the core biological processes highlighted in these descriptions for each broad category."
else:
    with open(p_path, "r") as text_file1:
        prompt = text_file1.read()

with open(job_folder + "/go_info.txt", "r") as text_file2:
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

with open(job_folder +'/LLMresponse.txt', 'w') as output:
    output.write(response.message.content)

print(response.message.content)
