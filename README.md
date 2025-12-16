# AI-Powered Ticket Creation and Categorization from User Input

## Project Overview
This project is an end-to-end AI solution designed to automate the lifecycle of IT support tickets. By leveraging Natural Language Processing (NLP) and Machine Learning, the system transforms raw, unstructured user complaints into structured, actionable data.

The system automatically predicts the **Department/Topic**, determines the **Urgency (Priority)**, and extracts critical technical **Entities** (like User IDs and Device names) to eliminate manual triage.

---

## Project Roadmap & Status

| Milestone | Objective | Status |
| :--- | :--- | :--- |
| **Milestone 1** | Data Acquisition, Cleaning & Feature Engineering | ✅ Completed |
| **Milestone 2** | Model Selection, Training, and NER Development | ✅ Completed |
| **Milestone 3** | Ticket Generation Engine & Interface Integration | 🚀 In Progress |
| **Milestone 4** | Deployment & Reporting | Planned |

---

## Detailed Technical Workflow

### Milestone 1: Data Foundations
In this phase, we processed a large-scale dataset (**47k+ rows**) to create a clean "Gold Standard" for training.

### Milestone 2: Core Model Development
We developed the "Brain" of the system using three distinct components:

* **Topic Classification:** SVM (Linear Kernel) chosen for high accuracy (~0.7677 F1).
* **Urgency Prediction:** SVM/Logistic Regression for priority labeling (~0.7931 F1).
* **NER Extraction:** Custom spaCy model for identifying technical entities.
