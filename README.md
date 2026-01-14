# AI-Powered IT Ticket Intelligence System

### *Automated Ticket Categorization using BERT-SVM Ensemble & Streamlit*

## Project Overview

This project automates the manual process of IT helpdesk ticket routing. By utilizing a **State-of-the-Art (SOTA)** Ensemble approach, the system analyzes user-submitted issue descriptions and automatically assigns them to one of eight technical categories (Hardware, Access, Administrative Rights, etc.) with high precision.

---

## Key Features

* **Hybrid Ensemble Engine**: Combines **DistilBERT** (Semantic Context) and **Linear SVM** (Keyword Precision) for a final accuracy of **~89.2%**.
* **JSON-Native Output**: Designed for enterprise integration, providing categories and confidence scores in structured JSON.
* **Aesthetic UI**: A user-friendly Streamlit interface with a soft pastel theme for modern IT operations.
* **Production-Ready**: Implemented with Git LFS for large model weight management and modular Python architecture.

---

## Model Performance Journey

During the research phase, we compared multiple architectures to find the optimal balance between speed and accuracy:

| Model Stage | Architecture | Accuracy | Status |
| --- | --- | --- | --- |
| **Baseline** | Logistic Regression | 72.0% | ❌ Replaced |
| **Specialist** | Linear SVM | 84.5% | ✅ Included |
| **SOTA** | DistilBERT | 86.4% | ✅ Included |
| **Final System** | **BERT-SVM Ensemble** | **88.7% - 89.2%** | 🏆 **Champion** |

---

## Project Structure

```text
IT-Ticket-Automation/
├── 📂 Kaggle Dataset/
│   └── 📂 models/             # Local weights (Managed via Git LFS)
│       ├── 📁 final_bert_model/
│       ├── 📄 svm_model.pkl
│       └── 📄 tfidf_vectorizer.pkl
├── 📄 M1.ipynb                # Preprocessing & Class Balancing
├── 📄 M2.ipynb                # Training & Evaluation
├── 📄 M3.ipynb                # JSON Engine Development
├── 📄 app.py                  # Final Streamlit Interface
├── 📄 .gitattributes          # Git LFS Configurations
└── 📄 requirements.txt        # Dependency Management

```

---

## Installation & Usage

### 1. Clone the Repository

```bash
git clone https://github.com/Anamika74/AI-Powered-Ticket-Creation-and-Categorization-from-User-Input.git
cd IT-Ticket-Automation

```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm

```

### 3. Run the Application

```bash
streamlit run app.py

```

---

## Technical Choices (Milestone Highlights)

* **Omitted Traditional NLP**: We skipped stemming and stop-word removal. **Reason**: BERT relies on sentence context; removing these elements destroys the "Attention" patterns the model uses to understand intent.
* **Class Weighting**: Since the dataset was imbalanced, we calculated manual weights for the loss function rather than oversampling (SMOTE) to prevent overfitting on synthetic data.
* **Hybrid Logic**: The engine uses a **60/40 weighted vote** between BERT and SVM, ensuring the system remains robust even when technical jargon is misspelled.

---

## License

Distributed under the MIT License. See `LICENSE` for more information.

---

### **Next Step for You**

You can now create a file named `README.md` in your main VS Code folder, paste this content inside, and then:

1. `git add README.md`
2. `git commit -m "Docs: Finalized aesthetic README"`
3. `git push`
