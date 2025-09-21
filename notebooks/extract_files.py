import os
import json
from tqdm import tqdm

def extract_reports_streaming(root_folder, output_path="mimic_cxr_reports.jsonl"):
    with open(output_path, "w", encoding="utf-8") as outfile:
        for root, _, files in os.walk(root_folder):

            for file in tqdm(files, desc="Streaming reports..."):
                if file.endswith(".txt"):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            text = f.read().strip()
                            if text:
                                report = {
                                    "id": file.replace(".txt", ""),
                                    "text": text
                                }
                                outfile.write(json.dumps(report) + "\n")
                    except Exception as e:
                        print(f"Error reading {file_path}: {e}")


extract_reports_streaming("../files")