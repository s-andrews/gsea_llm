import requests

def fetch_go_info(go_id):
    """
    Fetch GO term info from QuickGO API.
    Returns a tuple (short_desc, long_desc) or None if not found.
    """
    url = f"https://www.ebi.ac.uk/QuickGO/services/ontology/go/terms/{go_id}"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error fetching {go_id}: {response.status_code}")
        return None

    data = response.json().get("results", [{}])[0]

    # Short description is stored under "name"
    short_desc = data.get("name", "N/A")

    # Long description
    definition = data.get("definition")
    if isinstance(definition, dict) and "text" in definition:
        long_desc = definition["text"]
    else:
        long_desc = definition or "N/A"

    return short_desc, long_desc


def save_go_info(go_list, filename="go_info.txt"):
    """
    Saves multiple GO terms into a text file.
    """
    with open(filename, "w") as f:
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
    print(f"All information saved to {filename}")

if __name__ == "__main__":
    go_ids = input("Enter GO IDs separated by commas (e.g., GO:0019955,GO:0008150): ")
    go_list = [gid.strip() for gid in go_ids.split(",")]
    save_go_info(go_list)
