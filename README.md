
#AI-Powered Ticket Creation and Categorization from User Input
## Project Overview- This project is an end-to-end AI solution designed to automate the lifecycle of IT support tickets. By leveraging Natural Language Processing (NLP) and Machine Learning, the system transforms raw, unstructured user complaints into structured, actionable data.

The system automatically predicts the **Department/Topic**, determines the **Urgency (Priority)**, and extracts critical technical **Entities** (like User IDs and Device names) to eliminate manual triage.

---

## Project Roadmap & Status| Milestone | Objective | Status |
| --- | --- | --- |
| **Milestone 1** | Data Acquisition, Cleaning & Feature Engineering | **✅ Completed** |
| **Milestone 2** | Model Selection, Training, and NER Development | **✅ Completed** |
| **Milestone 3** | Ticket Generation Engine & Interface Integration | **🚀 In Progress** |

---

## Detailed Technical Workflow
### Milestone 1: Data FoundationsIn this phase, we processed a large-scale dataset (47k+ rows) to create a clean "Gold Standard" for training.

* **Text Preprocessing:** Implemented a robust cleaning pipeline:
* Conversion to lowercase.
* Removal of URLs, HTML tags, and special characters.
* Stop-word removal and Lemmatization to preserve technical context.


* **Label Engineering:** Created a rule-based logic to generate initial **Priority** labels based on keywords and sentiment patterns.
* **Vectorization:** Implemented **TF-IDF (Term Frequency-Inverse Document Frequency)** to convert text into numerical feature matrices, capturing the importance of technical terms (e.g., "server," "crash," "VPN").

### Milestone 2: The AI BrainThis phase involved building three distinct models to handle different parts of the ticket.

####1. Topic & Priority ClassificationWe conducted a "Model Tournament" to find the most accurate architecture:

* **Models Tested:** Logistic Regression, Naive Bayes, Linear SVM, Random Forest, and XGBoost.
* **Winning Model:** **Linear SVM** emerged as the top performer due to its high efficiency with sparse TF-IDF data.
* **Performance:**
* **Topic Classification:** Weighted F1-Score of **~0.7677**
* **Urgency Classification:** Weighted F1-Score of **~0.7931**



####2. Named Entity Recognition (NER)To extract structured data from sentences (e.g., "Laptop-44 is broken for user ryan_hr"), we trained a custom NLP model.

* **Architecture:** Developed using **spaCy’s blank English model** with a custom NER pipe.
* **Data Iteration:** Initially trained on 1,000 rows, then **doubled to 2,000 rows** to improve the model's ability to distinguish between a `DEVICE` and a `USER_ID`.
* **Refinement:** Optimized over 30 training epochs with dropout to prevent overfitting.

---

## Repository Structure| File/Folder | Description |
| --- | --- |
| **`/Kaggle Dataset`** | The primary directory containing all trained AI assets. |
| `tfidf_vectorizer.pkl` | The trained "translator" that converts user text to numbers. |
| `best_topic_classifier.pkl` | Finalized SVM model for predicting the ticket category. |
| `best_priority_classifier.pkl` | Finalized SVM model for predicting urgency. |
| **`/custom_it_ner_model`** | The folder containing the saved spaCy NER model (v1.0). |
| `confusion_matrix.png` | Visual proof of model accuracy and classification performance. |
| `milestone_01_prep.ipynb` | Jupyter notebook for Data Cleaning & Feature Engineering. |
| `milestone_02_train.ipynb` | Jupyter notebook for Model Training and NER optimization. |

---

## How the System Works1. **Input:** User types: *"The SAP software is crashing on my Laptop-X12 for user smith_j."*
2. **Processing:**
* **Step 1:** The **TF-IDF Vectorizer** converts the text for the classifiers.
* **Step 2:** The **Topic Model** identifies this as a "Software" ticket.
* **Step 3:** The **Priority Model** identifies this as "Medium/High" urgency.
* **Step 4:** The **NER Model** extracts `SAP` (Software), `Laptop-X12` (Device), and `smith_j` (User).


3. **Output:** A structured JSON object ready for the IT database.

---

##🛠 Installation & EnvironmentTo run this project locally, ensure you have Python 3.8+ installed:

```bash
# Install core dependencies
pip install pandas scikit-learn joblib spacy matplotlib seaborn

# Download spaCy base model
python -m spacy download en_core_web_sm

```

---

###💡 Key Technical Decisions* **Why SVM?** We chose Linear SVM over Random Forest because it performed significantly better with high-dimensional text data.
* **Data Recovery:** During the Git push process, we utilized `git reflog` and `git reset --hard` to recover work lost during a merge conflict, ensuring zero data loss during the handoff.
* **NER Balancing:** We manually adjusted the training sample to ensure the model didn't confuse hardware names with user IDs.

---
