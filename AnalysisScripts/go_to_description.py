import requests
import os

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

def save_go_info(go_list, filename):
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

def read_go_ids_from_file(file_path):
    go_ids = []
    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                go_ids.extend([gid.strip() for gid in line.split(",")])
    return go_ids

if __name__ == "__main__":
    # Let the user specify which file to read
    input_file = input("Enter the path to the GO ID file you want to read: ").strip()
    
    if not os.path.exists(input_file):
        print(f"File not found: {input_file}")
    else:
        go_list = read_go_ids_from_file(input_file)
        output_file = os.path.splitext(input_file)[0] + "_go_info.txt"
        save_go_info(go_list, output_file)
