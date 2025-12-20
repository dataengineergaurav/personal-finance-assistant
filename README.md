# 💰 Personal Finance Assistant (Domain-Driven Edition)

A professional AI-powered expense tracking and financial insights agent built with **Pydantic AI** and **Supabase**. This agent leverages modern LLMs (**Google Gemini**, **OpenAI**, **Ollama**) to provide precise financial management through a natural language interface.

## 📁 Project Architecture

The project follows a Domain-Driven Design (DDD) approach to ensure maintainability and scalability.

```txt
personal-finance-assistant/
├── services/           # Domain logic (Ledger, Advisor, Categories)
├── prompts/            # Professional financial personas & templates
├── config/             # Model and environment configurations
├── database.py         # Supabase persistence layer
├── agent.py            # AI Agent orchestration (Tools & Logic)
├── run.py              # CLI Interactive session manager
├── models.py           # Pydantic data models
├── requirements.txt    # Project dependencies
└── setup_supabase.sql  # Database schema definition
```

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.12+
- A Supabase account and project
- API Keys for your preferred LLM provider (Gemini recommended)

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
2. Run the SQL provided in `setup_supabase.sql` in the Supabase SQL Editor to create the `expenses` table.
3. Obtain your `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY` from the project settings.

### 4. Configuration
Copy `.env.example` to `.env` and fill in your credentials:
```bash
cp .env.example .env
```
Key variables:
- `GEMINI_API_KEY`: Required for Google Gemini (Get from [Google AI Studio](https://aistudio.google.com/))
- `SUPABASE_URL` & `SUPABASE_SERVICE_ROLE_KEY`: Your Supabase project credentials.
- `MODEL_PROVIDER`: Default provider (`gemini`, `openai`, or `ollama`).

---

## 🏃 Usage

Launch the assistant using the CLI manager:

```bash
# Use default provider (from .env)
python run.py

# Override with a specific provider
python run.py --model google
python run.py --model openai
python run.py --model ollama
```

### 🗣️ Example Queries

- **Record Expenses**: 
    - *"I spent $15 on a burger today"*
    - *"Paid $1200 for rent"*
    - *"Bought some groceries for $45.50"*
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

| Feature | Description |
|---------|-------------|
| **Smart Ledger** | Automatically maps natural language to categories (food, transport, shopping, etc.). |
| **History Views** | Filter and view transaction records directly from Supabase. |
| **Spending Insights** | Identifies top spending categories and provides actionable advice. |
| **Budget Planning** | Generates professional allocation plans based on personalized income. |
| **Multi-Model Support** | Seamlessly switch between local (Ollama) and cloud (Gemini, OpenAI) models. |

---

## 📊 Categories

The assistant automatically maps your spending to these standard financial categories:
`food`, `transport`, `entertainment`, `utilities`, `healthcare`, `shopping`, `education`, `other`.

---

## 🧪 Testing

Run the end-to-end agent test suite to verify the integration:
```bash
python test_agent_e2e.py
```
