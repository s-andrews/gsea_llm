import sys
from pathlib import Path
import requests


def fetch_go_info(go_id):
    url = f"https://www.ebi.ac.uk/QuickGO/services/ontology/go/terms/{go_id}"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error fetching {go_id}: {response.status_code}")
        return None

    data = response.json().get("results", [{}])[0]
    short_desc = data.get("name", "N/A")

    definition = data.get("definition")
    if isinstance(definition, dict) and "text" in definition:
        long_desc = definition["text"]
    else:
        long_desc = definition or "N/A"

    return short_desc, long_desc


def save_go_info(go_list, output_file):
    """
    Saves multiple GO terms into a text file.
    """
    with open(output_file, "w") as f:
        for go_id in go_list:
            result = fetch_go_info(go_id)
            if result:
                short_desc, long_desc = result
                f.write(f"ID: {go_id}\n")
                f.write(f"Short Description: {short_desc}\n")
                f.write(f"Long Description: {long_desc}\n")
                f.write("-" * 50 + "\n")
            else:
                f.write(f"GO ID: {go_id} - Not Found\n")
                f.write("-" * 50 + "\n")
    # print(f"All information saved to {output_file}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python go_to_description.py <job_folder>")
        sys.exit(1)

    job_folder = Path(__file__).parent.parent/("WebFrontEnd/Jobs/"+sys.argv[1])
    go_ids_file = job_folder / "go_ids.txt"
    output_file = job_folder / "go_info.txt"

    with open(go_ids_file, "r") as f:
        f.readline()
        go_list = [line.strip() for line in f if line.strip()]
    save_go_info(go_list, output_file)
