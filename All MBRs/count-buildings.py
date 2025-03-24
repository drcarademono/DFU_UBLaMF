import os
import json
import csv

def count_model_ids(directory, output_file):
    """
    Counts the occurrences of each ModelId under 1000 in all RMB.json files' SubRecords > Exterior sections.
    Outputs the results as a CSV file.
    """
    model_id_counts = {}

    # Iterate through all RMB.json files in the directory
    for file_name in os.listdir(directory):
        if file_name.endswith(".RMB.json"):
            file_path = os.path.join(directory, file_name)

            # Load the JSON data
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)

                # Navigate to SubRecords > Exterior > Block3dObjectRecords
                sub_records = data.get("RmbBlock", {}).get("SubRecords", [])
                for sub_record in sub_records:
                    exterior = sub_record.get("Exterior", {})
                    block_3d_objects = exterior.get("Block3dObjectRecords", [])
                    
                    # Count ModelId occurrences under 1000
                    for obj in block_3d_objects:
                        model_id = obj.get("ModelId")
                        if isinstance(model_id, int) and model_id < 1000:
                            model_id_counts[model_id] = model_id_counts.get(model_id, 0) + 1

            except Exception as e:
                print(f"Error processing file {file_name}: {e}")

    # Write results to a CSV file
    with open(output_file, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["ModelId", "Count"])
        for model_id, count in sorted(model_id_counts.items()):
            writer.writerow([model_id, count])

    print(f"ModelId counts have been written to {output_file}")

# Directory with RMB.json files and the output CSV file
directory = "."
output_file = "model_id_counts.csv"
count_model_ids(directory, output_file)

