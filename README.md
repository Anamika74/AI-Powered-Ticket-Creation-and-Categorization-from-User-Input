#  AI-Powered Ticket Creation and Categorization from User Input

##  Project Overview

This repository hosts an end-to-end Natural Language Processing (NLP) system designed to automate the initial triage process for customer support complaints.
By analyzing raw text input, the system automatically classifies the complaint's **Category** (e.g., Refund, Shipping) and assigns a **Priority Level (Urgency)**.

This solution is being developed using a structured, iterative approach, starting with foundational machine learning models (TF-IDF + Scikit-learn classifiers).

---

##  Status: Ongoing Development

### Phase Completion

Development is currently focused on **Milestone 3: Integrating the full Ticket Generation Engine.**

| Milestone | Objective | Status |
| :--- | :--- | :--- |
| **Milestone 1** | Data Prep and Feature Engineering | **Completed** |
| **Milestone 2** | Core Model Development & Selection | **Completed** |
| **Milestone 3** | Ticket Generation Engine Integration | **In Progress** |
| **Milestone 4** | Optimization (Hyperparameter Tuning, Deep Learning) | *Planned* |

---

##  Milestone 2: Core Model Development Results

The initial baseline models were trained, validated, and selected to finalize the core classification mechanism.

### Best Model Selection (Weighted F1-Score)

| Task | Best Model Selected | Weighted F1-Score |
| :--- | :--- | :--- |
| **Category Classification** | **SVM (Linear Kernel)** | **0.7677** |
| **Urgency Classification** | **SVM / Logistic Regression** | **~0.7931** |

The **SVM (Linear Kernel)** was chosen as the consistent best performer to anchor both classification tasks in the final pipeline.



---

##  Project Architecture

The final system architecture combines multiple components into a seamless processing pipeline:

1.  **Preprocessing & Cleaning:** Text is cleaned (lower-cased, tokenized, lemmatized, stopwords removed) to reduce noise.
2.  **Feature Extraction:** **TF-IDF Vectorization** converts clean text into a sparse numerical matrix .
3.  **Classification:** The numerical features are fed to the trained **SVM** classifiers for Category and Urgency prediction.
4.  **Entity Recognition (NER):** A spaCy model extracts key named entities (e.g., Order IDs, Dates) to auto-populate the structured ticket.

---

##  Repository Contents

| File/Folder | Description | Milestone |
| :--- | :--- | :--- |
| `milestone_01.ipynb` | Code for Data Loading, Feature Engineering (Cleaning, TF-IDF preparation), and target variable encoding. | M1 |
| `milestone_02.ipynb` | Code for Model Comparison, training LR/SVM/RF/XGBoost, and full evaluation using F1-Score and Confusion Matrices. | M2 |
| `Customer_Complaints_Updated.csv` | The raw input dataset used for training and testing. | M1 |
| `model_f1_comparison.png` | Visualization of all model F1-Score results. | M2 |
| `ticket_generation_engine.py` | *(Current Focus)* The final Python module containing the `generate_ticket` function for end-to-end execution. | M3 |

---

##  Getting Started (Local Setup)

To run the project locally, follow these steps:

### 1. Prerequisites

1.  Python 3.8+
2.  Git

### 2. Installation

Clone the repository and install the required libraries:

```bash
# Clone the repository
git clone [https://github.com/your-username/AI-Powered-Ticket-Creation-and-Categorization-from-User-Input.git](https://github.com/your-username/AI-Powered-Ticket-Creation-and-Categorization-from-User-Input.git)
cd AI-Powered-Ticket-Creation-and-Categorization-from-User-Input

# Install core dependencies (use the full list including NLTK and SpaCy)
pip install pandas scikit-learn nltk seaborn matplotlib xgboost ipykernel

# Download necessary NLTK and SpaCy resources
python -c "import nltk; nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('punkt')"
python -m spacy download en_core_web_sm
