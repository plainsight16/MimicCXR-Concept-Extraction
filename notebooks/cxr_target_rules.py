from medspacy.ner import TargetRule
import csv

def load_target_rules_from_csv(merged_csv, label):
    rules = []
    with open(merged_csv, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rules.append(TargetRule(row["Entity"], label))
    return rules

finding_rules = load_target_rules_from_csv(merged_csv="Vocabulary/output/merged_target_rules/FINDING_merged.csv", label="FINDING")
anatomy_rules = load_target_rules_from_csv(merged_csv="Vocabulary/output/merged_target_rules/ANATOMY_merged.csv", label="ANATOMY")
device_rules = load_target_rules_from_csv(merged_csv="Vocabulary/output/merged_target_rules/DEVICE_merged.csv", label="DEVICE")
rules = []
rules.extend(finding_rules)
rules.extend(anatomy_rules)
rules.extend(device_rules)