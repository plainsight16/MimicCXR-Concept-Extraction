import json
import csv
from collections import Counter, defaultdict
import os

def entity_stats(jsonl_path, output_dir):
    counter = Counter()
    per_label_entities = defaultdict(set)
    per_label_counter = defaultdict(Counter)

    os.makedirs(output_dir, exist_ok=True)

    # Read all JSONL lines
    with open(jsonl_path, "r") as f:
        for line in f:
            record = json.loads(line)
            text = record["text"]
            for ann in record["annotations"]:
                entity_text = text[ann["start_offset"]:ann["end_offset"]].strip()
                label = ann["label"]
                counter[(entity_text, label)] += 1
                per_label_entities[label].add(entity_text)
                per_label_counter[label][entity_text] += 1

    # --- Write frequency CSV (all entities) ---
    sorted_entities = sorted(counter.items(), key=lambda x: x[1], reverse=True)
    with open(os.path.join(output_dir, "entity_frequency.csv"), "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Entity", "Label", "Frequency"])
        for (entity_text, label), freq in sorted_entities:
            writer.writerow([entity_text, label, freq])

    # --- Write per-label CSV (unique entity lists) ---
    with open(os.path.join(output_dir, "entities_per_label.csv"), "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Label", "Entities"])
        for label, entities in sorted(per_label_entities.items(), key=lambda x: x[0]):
            writer.writerow([label, "; ".join(sorted(entities))])

    # --- Write separate CSV for each label ---
    for label, entity_counter in per_label_counter.items():
        sorted_label_entities = sorted(entity_counter.items(), key=lambda x: x[1], reverse=True)
        filename = f"{label}_entities.csv"
        with open(os.path.join(output_dir, filename), "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Entity", "Frequency"])
            for entity_text, freq in sorted_label_entities:
                writer.writerow([entity_text, freq])

# Example usage
entity_stats(
    "../data/doccano_input.jsonl",   # Input JSONL file
    "../data/vocabulary/"    # Output directory
)
