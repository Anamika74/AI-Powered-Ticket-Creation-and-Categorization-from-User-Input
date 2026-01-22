# 🤖 AI-Powered IT Ticket Intelligence System

### *Strategic Automation using BERT–SVM Ensemble & Streamlit*

---

## 📌 Project Overview

The **AI-Powered IT Ticket Intelligence System** is an end-to-end NLP solution that automates the lifecycle of IT support tickets.
It converts **unstructured user complaints** into **structured, actionable tickets** using advanced Natural Language Processing and Machine Learning.

The system is built with a **stateful architecture using SQLite**, ensuring that all tickets are persistently stored, tracked via **SLA timers**, and managed through a **professional role-based workflow**.

---

## 🗺️ Project Roadmap & Status

This project followed a **rigorous 4-phase development cycle**, evolving from a raw ML model into a **production-ready enterprise dashboard**.

| Phase   | Milestone             | Key Deliverables                                                   | Status     |
| ------- | --------------------- | ------------------------------------------------------------------ | ---------- |
| Phase 1 | Data & Foundation     | Data acquisition, cleaning, and feature engineering for IT tickets | ✅ Complete |
| Phase 2 | AI Engine Development | BERT + SVM Ensemble training (89.2% accuracy) and NER development  | ✅ Complete |
| Phase 3 | Core Ticket Logic     | Automated prioritization and JSON-based ticket generation          | ✅ Complete |
| Phase 4 | Enterprise Deployment | Role-based UI, SQLite persistence, and real-time SLA tracking      | ✅ Complete |

---

## 📅 Agile Project Management

Detailed planning and execution artifacts are included:

* **AGILE_SPRINT_REPORT.md**

  * Sprint velocity metrics
  * 19 delivered features
  * Sprint retrospectives

* **Feature Overview**

  * Technical breakdown of the AI engine
  * Database schema and ticket workflow design

---

## 🧠 Technical Workflow — *The “Brain”*

### 1️⃣ Hybrid Topic Classification (Ensemble)

* **Approach:** BERT + SVM Ensemble
* **Performance:** 89.2% classification accuracy

**Why it works:**

* BERT captures deep semantic context
* SVM enhances keyword-level precision

✅ Robust handling of both technical jargon and conversational user language

---

### 2️⃣ SLA Intelligence & Workflow Management

**Real-Time SLA Monitoring**

* 🟢 On Track: < 2 hours
* 🟡 Warning: 2–6 hours
* 🔴 Breached: > 6 hours

**Ticket Lifecycle**

```
Open → In Progress → Resolved → Closed
```

---

## 📂 Project Structure

```plaintext
AI-Powered-Ticket-Automation/
├── 📄 AGILE_SPRINT_REPORT.md      # Sprint breakdown & velocity metrics
├── 📄 app.py                      # Streamlit UI with role-based access
├── 📄 database.py                 # SQLite persistence & SLA logic
├── 📄 engine_wrapper.py           # AI inference wrapper
├── 📄 service_desk.db             # Persistent SQLite database
├── 📂 Kaggle Dataset/             # ML training notebooks & models
└── 📄 requirements.txt            # Dependency management
```

---

## 🛠️ Engineering Highlights

* **Persistent State:** SQLite ensures tickets persist across sessions
* **Role-Based Dashboards:**

  * General Users → Ticket submission
  * Support Staff → Queue management & analytics
* **Live Analytics:** Real-time metrics for:

  * Total tickets
  * Open tickets
  * High-priority tickets
* **Git LFS:** Managed a 255MB BERT model using Git Large File Storage

---

## 🔮 Future Enhancements

Planned upgrades to evolve this into a **full ITSM platform**:

* 🤝 Smart Agent Assignment (expertise-based routing)
* 📧 Email & Slack integration for real-time notifications
* 🔁 Automated retraining pipeline with user feedback

---

## 🚀 Installation & Usage

### Clone the Repository

```bash
git clone https://github.com/Anamika74/AI-Powered-Ticket-Creation-and-Categorization.git
cd AI-Powered-Ticket-Creation-and-Categorization
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Application

```bash
streamlit run app.py
```

---

## 👩‍💻 Author

**Developed by Anamika Sharma**
