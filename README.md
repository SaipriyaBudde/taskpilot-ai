# TaskPilot AI

> **From mental chaos to clear execution — instantly.**

TaskPilot AI is an intelligent execution assistant that transforms unstructured thoughts into a clear, prioritized, and actionable plan — helping users move from *overwhelm → action* in seconds.

---

## 🚩 The Problem

Modern productivity tools fail at the most critical step: **decision-making**.

People don’t struggle to *list tasks* — they struggle to:
- decide what actually matters
- figure out where to start
- avoid overload and context switching
- structure their day realistically

This creates:
- decision fatigue  
- procrastination  
- low-quality execution  

---

## 💡 Solution

TaskPilot AI bridges the gap between **intention and execution**.

It takes messy, natural-language input and converts it into a **structured execution system**.

### Example Input

> “I have a project deadline tomorrow, office work pending, groceries to buy, and I need to prepare for an interview.”

### Output

TaskPilot instantly generates:

- 🎯 A clear execution strategy  
- 🚀 A defined starting point  
- ✅ Today’s non-negotiable tasks  
- 📊 Priority-based task breakdown  
- 🔄 A structured execution flow  

---

## ⚙️ Core Features

### 🧠 Today's Execution Strategy
A high-level plan that defines *how* the day should be approached.

### 🎯 Start Here
Eliminates hesitation by identifying the most critical first step.

### ✅ Today’s Non-Negotiables
Defines the minimum set of tasks required for a successful day.

### 📊 Execution Priorities
Each task is analyzed across:
- Priority  
- Urgency  
- Effort  
- Impact  

### 🔄 Suggested Execution Plan
A frictionless sequence of tasks designed for momentum and focus.

---

## 🚀 Why TaskPilot AI Stands Out

Most tools optimize for **task storage**.  
TaskPilot optimizes for **task execution**.

It doesn’t just organize your tasks —  
it **tells you exactly what to do next**.

---

## 🏗️ Architecture

### Frontend
- React (Vite)
- Custom CSS
- Lucide Icons

### Backend
- FastAPI (Python)

### System Flow

```text
User Input (Unstructured Thoughts)
        ↓
AI Processing Layer (Task Structuring + Prioritization)
        ↓
Execution Engine (Strategy + Flow Generation)
        ↓
Frontend Dashboard (Clear Action Plan)

```

## 📁 Project Structure


taskpilot-ai/
├── backend/
│   └── app/
│       └── main.py
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── main.jsx
│   └── package.json
└── README.md

## Running Locally

### Backend

```bash
cd backend
uvicorn app.main:app --reload
Runs on:  
[http://127.0.0.1:8000](http://127.0.0.1:8000)
```

### Frontend

```bash
cd frontend
npm install
npm run dev
Runs on:  
[http://localhost:5173](http://localhost:5173)
```
