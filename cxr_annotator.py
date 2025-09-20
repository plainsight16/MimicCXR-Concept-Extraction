# cxr_annotator.py
import json
import streamlit as st
from pathlib import Path

# ----------- Load Data ----------- #
DATA_PATH = Path("doccano_input.jsonl")
OUT_PATH = Path("corrected_doccano_output.jsonl")


if "examples" not in st.session_state:
    if DATA_PATH.exists():
        with DATA_PATH.open() as f:
            st.session_state["examples"] = [json.loads(line) for line in f]
    else:
        st.session_state["examples"] = []  # empty list fallback

examples = st.session_state["examples"]
total = len(examples)

# ----------- Page Navigation ----------- #
if "index" not in st.session_state:
    st.session_state.index = 0

def go_next():
    if st.session_state.index < total - 1:
        st.session_state.index += 1

def go_prev():
    if st.session_state.index > 0:
        st.session_state.index -= 1

# ----------- Active Example ----------- #
doc = examples[st.session_state.index]

text = doc["text"]
annotations = doc.get("annotations", [])

# ----------- PAGE HEADING ----------- #
st.title("🩺 CXR Annotation Review Tool")
st.write(f"📄 Document {st.session_state.index + 1} of {total}")

# ----------- Display Text with Annotations ----------- #
def highlight_text(text, annotations):
    """Wrap annotated spans in brackets with labels."""
    sorted_anns = sorted(annotations, key=lambda x: x["start_offset"])
    out = ""
    last = 0
    for ann in sorted_anns:
        start, end, label = ann["start_offset"], ann["end_offset"], ann["label"]
        out += text[last:start]
        out += f"[{text[start:end]}|{label}]"
        last = end
    out += text[last:]
    return out

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("### ✏️ Annotated Text")
    
with col2:
    st.button("⬅️ Previous", on_click=go_prev)

with col3:
    st.button("Next ➡️", on_click=go_next)

st.code(highlight_text(text, annotations), language="markdown")
# ----------- Annotation Tools ----------- #
st.markdown("### ➕ Add Annotation")
col1, col2 = st.columns(2)
with col1:
    phrase = st.text_input("Entity Phrase")
with col2:
    label = st.selectbox("Label", ["FINDING", "ANATOMY", "DEVICE"])

if st.button("Add"):
    lower_text = text.lower()
    lower_phrase = phrase.lower()
    start = lower_text.find(lower_phrase)
    
    if start == -1:
        st.error("❌ Phrase not found in text.")
    else:
        end = start + len(phrase)
        new_ann = {"start_offset": start, "end_offset": end, "label": label}
        if new_ann not in annotations:
            annotations.append(new_ann)
            st.success(f"✅ Added [{phrase}] as {label}")
            st.rerun()
        else:
            st.warning("⚠️ Annotation already exists.")

# ----------- View/Delete Annotations ----------- #
st.markdown("### ❌ Delete Annotation")
    
if annotations:
    delete_idx = st.selectbox("Choose annotation to delete", list(range(len(annotations))))
    if st.button("Delete Selected"):
        
        deleted = annotations.pop(delete_idx)
        st.success(f"🗑️ Deleted: {deleted}")
        st.rerun()
else:
    st.info("No annotations yet.")

# ----------- Save Button ----------- #
if st.button("💾 Save to File"):
    with DATA_PATH.open("w") as f:
        for ex in examples:
            f.write(json.dumps(ex) + "\n")
    st.success("✅ Saved changes back to doccano_input.jsonl")

# ----------- Navigation Buttons ----------- #
st.markdown("### 📜 Navigation")
goto_idx = st.number_input(
    "Go to document index",
    min_value=0,
    max_value=total - 1,
    value=st.session_state.index,
    step=1
)
if goto_idx != st.session_state.index:
    st.session_state.index = goto_idx
    st.rerun()
