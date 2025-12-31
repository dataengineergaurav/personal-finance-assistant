# 💰 Personal Finance Assistant (Domain-Driven Edition)

A professional AI-powered expense tracking and financial insights agent built with **Pydantic AI** and **Supabase**. This agent leverages modern LLMs (**Ollama (Recommended)**, **Google Gemini**, **OpenAI**) to provide precise financial management through a natural language interface.

## 📁 Project Architecture

The project follows a Domain-Driven Design (DDD) approach to ensure maintainability and scalability.

```txt
personal-finance-assistant/
├── agents/             # Agent definitions (Finance, Strategy, Data Engineer)
├── core/               # Core configurations and observability (Settings, MLflow)
├── data/               # Data layer (Supabase Repositories, Migrations)
├── finance/            # Central Finance Package
│   ├── models/         # Domain Models (Transaction, Reports)
│   ├── services/       # Domain Services (Ledger, Advisor, Categories)
│   └── repositories/   # Repository Protocols
├── prompts/            # Professional financial personas & templates
├── tests/              # Test suite (E2E, Evaluation, Structural)
├── app.py              # Main Pydantic AI Web Application
├── run_clerk.py        # CLI Entry point for Finance Clerk
├── run_director.py     # CLI Entry point for Wealth Director
└── start_ui.sh         # Script to launch the Web UI
```

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.12+
- A Supabase account and project
- API Keys for cloud LLM providers (Optional, Ollama recommended for local-first)

### 2. Environment Setup
```bash
# Create and activate virtual environment
python3.12 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Database Configuration
1. Create a new project in [Supabase](https://supabase.com/).
2. Run the SQL provided in `data/setup.sql` in the Supabase SQL Editor to create the `expenses` and `income` tables.
3. Obtain your `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY` from the project settings.

### 4. Configuration
Copy `.env.example` to `.env` and fill in your credentials:
```bash
cp .env.example .env
```
Key variables:
- `MODEL_PROVIDER`: Default provider (`ollama` recommended, `gemini`, or `openai`).
- `GEMINI_API_KEY`: Required for Google Gemini (Get from [Google AI Studio](https://aistudio.google.com/))

---

## 🏃 Usage

Launch the agents using their respective CLI managers:

### 1. Web Interface (Recommended)
The new Pydantic AI built-in accessible web interface.
```bash
./start_ui.sh
```
- **API/Swagger UI**: `http://localhost:8000/docs`
- **Chat Endpoint**: `POST /api/chat`

### 2. Finance Clerk (CLI)
```bash
# Use default provider (from .env)
python run_clerk.py

# Override with a specific provider
python run_clerk.py --model gemini
```

### 3. Wealth Director (CLI)
```bash
python run_director.py
```

### 4. Interactive Streamlit Dashboard (New)
A modern web interface with chat and spending visualizations.
```bash
streamlit run streamlit_app.py
```

---

## 🔬 Observability & Evaluation (MLflow)

This project integrates **MLflow** for end-to-end tracing and agent evaluation.

### Running Evaluations
Run the "golden set" of queries to regression test the agents:
```bash
python tests/evaluate_agents.py
```

### Viewing Traces
Launch the MLflow UI to inspect agent reasoning, tool calls, and latency:
```bash
mlflow ui
# Open http://127.0.0.1:5000
```

### 🗣️ Example Queries

- **Record Expenses**: 
    - *"I spent $15 on a burger today"*
    - *"Paid $1200 for rent"*
    - *"Bought some groceries for $45.50"*
- **Record Income**:
    - *"My salary of $5000 arrived today"*
    - *"Received a bonus of $500"*
- **View History**:
    - *"Show my recent expenses"*
    - *"How much did I spend on food?"*
    - *"List all my transport costs"*
- **Financial Analysis**:
    - *"Analyze my spending habits"* (Provides top categories and recommendations)
- **Budgeting**:
    - *"Create a budget for a $6000 monthly income"* (Generates a 50/30/20 plan)

---

## 🛠️ Agent Capabilities

|Feature|Description|
|---|---|
|**Smart Ledger**|Automatically maps natural language to categories (food, transport, shopping, etc.).|
|**Income Tracking**|Record salary, bonuses, and deposits with precise source attribution.|
|**History Views**|Filter and view transaction records directly from Supabase.|
|**Spending Insights**|Identifies top spending categories and provides actionable advice.|
|**Budget Planning**|Generates professional allocation plans based on personalized income.|
|**Multi-Model Support**|Seamlessly switch between local (Ollama) and cloud (Gemini, OpenAI) models.|
|**Observability**|Full MLflow integration for tracing agent thoughts and evaluating performance.|

---

## 📊 Categories

The assistant automatically maps your spending to these standard financial categories:
`food`, `transport`, `entertainment`, `utilities`, `healthcare`, `shopping`, `education`, `other`.

---

## 🧪 Testing

Run the end-to-end agent test suite to verify the integration:
```bash
python tests/e2e_test.py
```
