import csv
import os
from collections import defaultdict

# --- existing lists ---
FINDINGS = [
    "pneumothorax", "pleural effusion", "effusion", "pulmonary edema", "consolidation",
    "atelectasis", "opacity", "infiltrate", "collapse", "interstitial markings",
    "fibrosis", "emphysema", "calcification", "nodule", "mass", "hyperinflation",
    "cardiomegaly", "airspace disease", "vascular congestion", "ground-glass opacity",
    "volume loss", "interstitial thickening", "vascular redistribution",
    "azygos vein distension", "pulmonary vascularity", "fluid overload",
    "congestive changes", "lobar consolidation", "lung infiltrates", "scarring", "pneumonia"
    "granulomatous", "varicella", "intrathoracic process", "pancreatic cancer", "air bronchograms",
    "aortosclerosis", "atelectactic", "atelectases", "atrium", "bronchiectasis", "cephalization"
    "edema", "effusions", "esophageal", "fractures", "hemorrhage", "lymphademopathy", "mediastinal"
    "metastatic", "opacification", "pneumomediastinax", "pneumopericardium", "pneumoperitoneum",
    "pneumothoraces", "sarcoidosis", "thoracentesis", "thoracocentsis", "osteopenia", "kyphosis"
    "acute cardiopulmonary", "atelectatic change", "scar", "fracture", "rib fracture", "spinal deformity",
    "scoliosis","osteoarthritis", "vascular congestion", "lung markings", "vascular redistribution", "azygos vein",
]

ANATOMY = [
    "lung", "lungs", "left lung", "right lung", "heart", "cardiac silhouette",
    "costophrenic angle", "costophrenic sulcus", "diaphragm", "hilar region", "hilum",
    "mediastinum", "trachea", "bronchus", "bronchi", "chest wall", "soft tissue",
    "upper lobe", "lower lobe", "middle lobe", "apex", "base", "ribs", "spine",
    "pleura", "retrocardiac region", "aorta", "pulmonary arteries", "hemithorax", "hernia", "hila"
    "bronchovascular", "hemidiaphragm", "carotrial junction", "cardiomediastinal silhouette", "hilar"
    "esophagogastric junction", "endotracheal", "nipple"
]

DEVICE = [
    "pacemaker", "endotracheal tube", "et tube", "central line", "chest tube", 
    "pigtail catheter", "NG tube", "nasoenteric tube", "ECG leads", "monitoring leads", 
    "electrodes", "IV line", "catheter", "clip", "wire", "line", "swan ganz catheter",
    "medical device", "implant", "drain", "port", "picc line", "icd lead", "monitoring leads", "iv catheter",
    "hardware", "port", "defibrillator", "nasogastric", "orogastric"
]
LABEL_MAP = {
    "FINDING": FINDINGS,
    "ANATOMY": ANATOMY,
    "DEVICE": DEVICE
}

def merge_target_rules(label_csv_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    for label, base_list in LABEL_MAP.items():
        # Load CSV if exists
        csv_path = os.path.join(label_csv_dir, f"{label}_entities.csv")
        csv_entities = {}
        if os.path.exists(csv_path):
            with open(csv_path, newline="") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    csv_entities[row["Entity"].strip()] = int(row["Frequency"])

        # Merge
        merged = {}
        # Add from CSV first
        for entity, freq in csv_entities.items():
            merged[entity] = freq
        # Add from base list (with freq=0 if not in CSV)
        for entity in base_list:
            if entity not in merged:
                merged[entity] = 0

        # Sort by frequency (desc)
        sorted_entities = sorted(merged.items(), key=lambda x: x[1], reverse=True)

        # Write merged CSV
        out_path = os.path.join(output_dir, f"{label}_merged.csv")
        with open(out_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Entity", "Frequency"])
            writer.writerows(sorted_entities)

        print(f"Merged file written: {out_path}")

# Example usage
merge_target_rules(
    label_csv_dir="entity_stats_output",   # where FINDING_entities.csv etc. are stored
    output_dir="merged_target_rules"       # output merged files
)
