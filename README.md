# 🤖 CrediFlow: The Autonomous Loan Processing Agent

**Live Demo:** https://credflow-frontend-132825211942.us-central1.run.app  
**Blog Post:** [Link to your Medium/Blog post]  
**Demo Video:** [Link to your YouTube/Loom video]
**Demo FE:** lovable.dev/projects/dd1e7b9b-a49f-4e56-8f5c-ed92087aa31f?view=codeEditor


---

## 🚀 What is CrediFlow?

CrediFlow is an advanced, autonomous AI agent system built for the **Google Cloud Build and Blog Marathon 2025**. It demonstrates how a Bank or Financial Institution (BFSI) can fully automate its personal loan lifecycle—from initial customer verification to final sanction letter generation.

The system uses a **Master/Worker Agent architecture**, where a **Master Agent (Gemini 2.5 Flash)** orchestrates a suite of specialized **Worker Agents** (Python tools) to execute business logic.

The project includes a **Streamlit "Agent Command Center"** that shows real-time agent traces and decision-making transparency.

---

## 🏛️ Architecture

CrediFlow runs as **two microservices** deployed on **Google Cloud Run**, ensuring seamless scaling and isolation of concerns.

> Add the image `crediflow_architecture.png` to the root of your GitHub repo.

### **Core Components**

#### **Frontend (`credflow-frontend`)**
- Built with **Streamlit**
- Acts as the **Agent Command Center**
- Displays real-time **Live Agent Trace**
- Serves the customer chat interface

#### **Backend (`credflow-backend`)**
- **FastAPI** server orchestrating the agentic workflow

#### **Master Agent**
- **Gemini 1.5 Flash**
- Understands intent, applies business rules, decides next tool calls

#### **Worker Agents (Tools)**
- **Verification Agent**
  - Connects to Firestore
  - Validates customer data and KYC status
- **Underwriting Agent**
  - Runs credit logic (bureau score checks, FOIR evaluation)
- **Sanction Letter Agent**
  - Generates PDF sanction letters
  - Uploads them to Cloud Storage and returns public URL

#### **Database**
- **Cloud Firestore (NoSQL)**  
  Stores CRM and credit profiles

#### **Storage**
- **Google Cloud Storage**  
  Holds generated sanction letters

#### **Monitoring**
- **Cloud Logging**  
  Tracks all agent actions and API calls

---

## 🏃 How to Use the Live Demo

Interact with the system like a real customer. Use the following pre-seeded profiles:

---

### **Scenario 1: “Happy Path” — Loan Approved**

**User:** hello  
**Agent:** Asks for phone number  
**User:** `9876543210` → *Aarav Sharma*  
**User:** I need 50000 for 12 months  
**Agent:** Approves + Generates PDF sanction letter (Cloud Storage link)

---

### **Scenario 2: Loan Rejected — Low Credit Score**

**User:** hello  
**User:** `9876543214` → *Vikram Kumar (Score: 680)*  
**User:** I want 200000 for 24 months  
**Agent:** Rejects due to score < 700

---

### **Scenario 3: KYC Failed**

**User:** hello  
**User:** `9876543212` → *Rohan Singh (KYC not done)*  
**Agent:** Informs user and stops the process

---

## 💻 How to Run Locally

### 1. Clone the Repository

```bash
git clone [Your GitHub Repo URL]
cd crediflow-agent
