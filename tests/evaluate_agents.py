
import asyncio
import mlflow
import pandas as pd
import sys
import os

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.finance import finance_agent
from data.database import ExpenseDatabase
from core.settings import settings

# Test Dataset
EVAL_QUESTIONS = [
    {
        "input": "I specifically spent exactly $50.00 on gas today.",
        "expected_category": "transport",
        "type": "transaction"
    },
    {
        "input": "How much have I spent on food?",
        "type": "query"
    },
    {
        "input": "My salary arrived: $3000",
        "expected_category": "salary",
        "type": "income"
    }
]

async def run_evaluation():
    print(f"Starting evaluation run: {settings.MLFLOW_EXPERIMENT_NAME}")
    
    # Initialize DB (Mock or Real - using Real for now as per env)
    try:
        db = ExpenseDatabase()
    except:
        print("Warning: DB Init failed, some tests may error.")
        db = None

    mlflow.set_tracking_uri(settings.MLFLOW_TRACKING_URI)
    mlflow.set_experiment(settings.MLFLOW_EXPERIMENT_NAME)

    with mlflow.start_run(run_name="manual_evaluation_script") as run:
        results = []
        
        for i, item in enumerate(EVAL_QUESTIONS):
            question = item["input"]
            print(f"[{i+1}/{len(EVAL_QUESTIONS)}] Testing: {question}")
            
            try:
                # Direct agent call for eval simplicity, bypassing router for now
                # In a real e2e, we might test the router too.
                result = await finance_agent.run(question, deps=db)
                # Finance agent is untyped, so result is in .output
                output = result.output
                
                results.append({
                    "input": question,
                    "output": output,
                    "error": None
                })
            except Exception as e:
                results.append({
                    "input": question,
                    "output": None,
                    "error": str(e)
                })

        # Log results as a table
        df = pd.DataFrame(results)
        mlflow.log_table(df, "evaluation_results.json")
        print("Evaluation complete. Results logged to MLflow.")

if __name__ == "__main__":
    asyncio.run(run_evaluation())
