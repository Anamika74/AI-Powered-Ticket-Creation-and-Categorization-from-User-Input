# AI-Powered IT Ticket Intelligence System

### *Strategic Automation via BERT-SVM Ensemble & Streamlit*

## Project Overview

This project is an **end-to-end AI solution** designed to automate the lifecycle of IT support tickets. By leveraging Natural Language Processing (NLP) and Deep Learning, the system transforms raw, unstructured user complaints into **structured, actionable data**.

The system automatically predicts the **Department/Topic**, determines **Urgency**, and extracts critical **Technical Entities** (User IDs, Device Names) to eliminate manual triage.

---

## Project Roadmap & Status

| Milestone | Objective | Status |
| --- | --- | --- |
| **Milestone 1** | Data Acquisition, Cleaning & Feature Engineering | ✅ **Completed** |
| **Milestone 2** | Model Selection, Training, and NER Development | ✅ **Completed** |
| **Milestone 3** | Ticket Generation Engine & JSON Integration | ✅ **Completed** |
| **Milestone 4** | Deployment (Streamlit App) & Reporting | 🚀 **In Progress** |

---

## Technical Workflow (The "Brain")

We developed a sophisticated multi-component architecture to handle the complexity of IT communication:

### **1. Hybrid Topic Classification**

* **Approach**: **BERT-SVM Ensemble**.
* **Performance**: While standalone SVM achieved ~76%, our hybrid approach reached **~89.2% accuracy**.
* **Benefit**: Combines **Deep Semantic Context** (BERT) with **Keyword Precision** (SVM) to handle both technical jargon and conversational language.

### **2. Intelligence Engine**

* **Urgency Prediction**: Implemented via probability-based labeling to ensure critical outages are prioritized immediately.
* **NER Extraction**: A custom **spaCy model** specifically trained to identify and extract entities like **User IDs** and **Device Names** directly from the ticket text.

---

##  Project Structure

```text
IT-Ticket-Automation/
├── 📂 Kaggle Dataset/
│   └── 📂 models/             # AI Weights (Managed via Git LFS)
│       ├── 📁 final_bert_model/
│       ├── 📄 svm_model.pkl
│       └── 📄 tfidf_vectorizer.pkl
├── 📄 M1.ipynb                # Data Cleaning & Preprocessing
├── 📄 M2.ipynb                # Model Benchmarking & NER Training
├── 📄 M3.ipynb                # JSON Logic & Ensemble Engine
├── 📄 app.py                  # Streamlit UI (Finalizing)
├── 📄 .gitattributes          # LFS Configuration
└── 📄 requirements.txt        # Dependency Management

```

---

## Installation & Usage

### **1. Environment Setup**

```bash
# Clone the repository
git clone https://github.com/Anamika74/AI-Powered-Ticket-Creation-and-Categorization-from-User-Input.git

# Enter the project directory
cd AI-Powered-Ticket-Creation-and-Categorization-from-User-Input

# Install dependencies
pip install -r requirements.txt
python -m spacy download en_core_web_sm

```

### **2. Launching the App**

```bash
streamlit run app.py

```

---

## Engineering Excellence

* **Git LFS Implementation**: Professionally managed the **255MB BERT model** using Git Large File Storage, ensuring a clean and functional GitHub repository.
* **Aesthetic UI Design**: Milestone 4 utilizes a **modern pastel theme** (Lavender & Soft Pink) to improve the user experience for IT support agents.
* **Modular Architecture**: The AI engine is decoupled from the UI, making it ready for integration into enterprise APIs or Chatbots.

---

## Technical Choices (Milestone Highlights)

* **Omitted Traditional NLP**: We skipped stemming and stop-word removal. **Reason**: BERT relies on sentence context; removing these elements destroys the "Attention" patterns the model uses to understand intent.
* **Class Weighting**: Since the dataset was imbalanced, we calculated manual weights for the loss function rather than oversampling (SMOTE) to prevent overfitting on synthetic data.
* **Hybrid Logic**: The engine uses a **60/40 weighted vote** between BERT and SVM, ensuring the system remains robust even when technical jargon is misspelled.

---

## License

Distributed under the MIT License. See `LICENSE` for more information.

---
