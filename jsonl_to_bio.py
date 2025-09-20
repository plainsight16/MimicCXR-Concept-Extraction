import spacy
import medspacy
from cxr_target_rules import rules

nlp = medspacy.load()

context = nlp.get_pipe("medspacy_context")

target_matcher = nlp.get_pipe("medspacy_target_matcher")

target_rules = rules

target_matcher.add(target_rules) #type: ignore


def jsonl_to_bio(data, output_path):
    with open(output_path, "w") as out:
        for record in data:
            text = record["text"]
            anns = record["annotations"]

            doc = nlp(text)

            for token in doc:
                ner_label = "O"
                context_label = ""

                for ann in anns:
                    if ann["start_offset"] <= token.idx < ann["end_offset"]:
                        prefix = "B" if token.idx == ann["start_offset"] else "I"
                        ner_label = f"{prefix}-{ann['label']}"

                        for ent in doc.ents:
                            if ent.start_char == ann["start_offset"] and ent.end_char == ann["end_offset"]:
                                if ent._.is_negated:
                                    context_label = "NEGATED"
                                elif ent._.is_uncertain:
                                    context_label = "UNCERTAIN"
                                else:
                                    context_label = "PRESENT"
                                break
                        break

                out.write(f"{token.text} {ner_label} {context_label}\n")
            out.write("\n")