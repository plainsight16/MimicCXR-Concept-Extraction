# Clinical Concept Extraction from MIMIC-CXR Radiology Reports

This repository contains the implementation of a **Clinical ModernBERT-based framework** for extracting clinical concepts and their assertion status (Present, Negated, Uncertain) from chest radiology reports in the **MIMIC-CXR dataset**.

The project combines **semi-automatic labeling** with **multi-task transformer-based learning**, enabling scalable and accurate structuring of unstructured radiology narratives.

---

## ✨ Features

* **Semi-Automatic Labeling Pipeline**

  * Candidate vocabulary construction using **n-grams + Log-Likelihood Ratio (LLR)**
  * Vocabulary verification against **RadLex** ontology
  * Rule-based entity detection with **spaCy/medspaCy**
  * Assertion labeling for context classification (Present, Negated, Uncertain)

* **Transformer Model (Clinical ModernBERT)**

  * Multi-task architecture with two classification heads:

    * **Concept Type Classification (NER)**: Findings, Anatomy, Device
    * **Assertion Status Classification**: Present, Negated, Uncertain
  * Long-context support (up to 8192 tokens)
  * Joint optimization with **Sparse Categorical Cross-Entropy Loss (SCCE)**

* **Evaluation & Visualization**

  * Metrics: Precision, Recall, F1-score, Accuracy
  * Classification reports using **scikit-learn**
  * Inline visualization of extracted entities with **spaCy displaCy**, color-coded by assertion status

---

## 📊 Results

* **Concept Classification (NER):** Weighted F1 = **0.939**
* **Assertion Classification:** Weighted F1 = **0.777**

  * Present and Uncertain detected effectively
  * Negated class remains challenging due to data sparsity

These results highlight the effectiveness of Clinical ModernBERT for semantic concept extraction, while also showing the need for improved negation detection strategies.

---

## ⚙️ Installation

Clone this repository and install dependencies:

```bash
git clone https://github.com/plainsight16/clinical-concept-extraction.git
cd clinical-concept-extraction
pip install -r requirements.txt
```

### Requirements

* Python 3.10+
* PyTorch
* Hugging Face Transformers
* spaCy + medspaCy
* scikit-learn
* streamlit (for demos/visualizations)

`requirements.txt` already includes:

```txt
numpy<2.0
spacy
streamlit==1.27.2
medspacy
torch
transformers
scikit-learn
```

---

## 🚀 Usage

### 1. Data Access

Due to ethical restrictions, **MIMIC-CXR reports cannot be shared directly**.

* Apply for access via [PhysioNet](https://physionet.org/).
* Complete the **CITI Human Subjects Research – Data or Specimens Only Research** course.
* Download and preprocess the reports as described in the paper.

### 2. Training the Model

```python
python train.py
```

This will fine-tune **Clinical ModernBERT** on your labeled subset and save the model checkpoint.

### 3. Evaluation

```python
python evaluate.py
```

Generates classification reports for both tasks (NER & assertion classification).

### 4. Visualization

Use `streamlit` or Jupyter notebooks to visualize entity extraction inline with colored highlights for assertion status.

```bash
streamlit run visualize_app.py
```

---

## 📂 Project Structure

```
├── data/                 # Preprocessed reports (not shared)
├── notebooks/            # Jupyter notebooks for experiments
├── src/                  # Core source code
│   ├── dataset.py        # MultiTaskDataset class
│   ├── model.py          # MultiTaskTokenClassifier
│   ├── train.py          # Training loop
│   ├── evaluate.py       # Evaluation scripts
│   └── visualize_app.py  # Streamlit visualization
├── requirements.txt
└── README.md
```

---

## 📑 Citation

If you use this code or approach in your research, please cite:

```
Edagbami SE, Abdullahi B.  
Clinical Concept Extraction from MIMIC-CXR Radiology Reports using Semi-Automatic Labeling and BERT Fine-Tuning.  
University of Lagos, 2025.
```

---

## ⚖️ License

This project is released under the **MIT License**.

---

## 🔮 Future Work

* Improved handling of negation and uncertainty via **data augmentation** and **specialized modules**
* Integration with external ontologies (UMLS, RadGraph)
* Extension to multimodal learning by aligning **image + report representations**
* Deployment in clinical decision support systems
