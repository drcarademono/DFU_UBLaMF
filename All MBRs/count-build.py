import os
import json
import re
import csv
from collections import defaultdict

def sanitize_json_string(json_string):
    # Replace any improper escape sequences
    json_string = re.sub(r'\\([^"\\/bfnrt]|u[0-9a-fA-F]{0,4})', r'\\\\\1', json_string)
    return json_string

def count_exterior_entries_and_model_ids(directory, output_csv):
    total_exterior_count = 0
    model_id_counts = defaultdict(int)
    
    # Iterate over every file in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            file_path = os.path.join(directory, filename)
            
            # Open and load the JSON file
            with open(file_path, 'r') as file:
                try:
                    json_string = file.read()
                    sanitized_string = sanitize_json_string(json_string)
                    data = json.loads(sanitized_string)
                    
                    # Navigate to 'RmbBlock' and then 'SubRecords'
                    rmb_block = data.get('RmbBlock', {})
                    sub_records = rmb_block.get('SubRecords', [])
                    
                    # Count the 'Exterior' entries in 'SubRecords'
                    for sub_record in sub_records:
                        exterior = sub_record.get('Exterior')
                        if exterior:
                            total_exterior_count += 1
                            block_3d_object_records = exterior.get('Block3dObjectRecords', [])
                            if block_3d_object_records:
                                # Extract the first ModelId and count it
                                first_model_id = block_3d_object_records[0].get('ModelIdNum')
                                if first_model_id is not None:
                                    model_id_counts[first_model_id] += 1
                
                except json.JSONDecodeError:
                    print(f"Error decoding JSON in file {filename} even after sanitizing")
                except KeyError as e:
                    print(f"Missing key {e} in file {filename}")
    
    # Sort the model_id_counts dictionary by count in descending order
    sorted_model_id_counts = sorted(model_id_counts.items(), key=lambda x: x[1], reverse=True)
    
    # Write to CSV
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["ModelIdNum", "Count"])
        for model_id, count in sorted_model_id_counts:
            csvwriter.writerow([model_id, count])
    
    print(f"Total 'Exterior' entries: {total_exterior_count}")
    print(f"ModelId counts have been written to {output_csv}")

# Set the directory to the current working directory and define the output CSV
directory = os.getcwd()
output_csv = "exterior_model_id_counts.csv"

# Process the files and export the CSV
count_exterior_entries_and_model_ids(directory, output_csv)

