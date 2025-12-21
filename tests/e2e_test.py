import asyncio
import os
from data.database import ExpenseDatabase
from agents.finance import finance_agent
from core.models import ExpenseCategory
from datetime import datetime
from core.settings import settings

async def test_end_to_end():
    print("🚀 Starting End-to-End Agent Test (Domain-Driven)...")
    
    # 1. Setup Model
    env_provider = os.getenv('MODEL_PROVIDER')
    if env_provider:
        provider = env_provider
    elif os.getenv('GEMINI_API_KEY'):
        provider = 'gemini'
    elif os.getenv('OPENAI_API_KEY'):
        provider = 'openai'
    else:
        provider = 'ollama'
    
    model = settings.get_model(provider)
    print(f"🤖 Testing with provider: {provider}")

    db = ExpenseDatabase()
    
    # 2. Test Add Expense
    test_desc = f"Agent Test {datetime.now().strftime('%H:%M:%S')}"
    user_input = f"I spent $12.34 on {test_desc} in shopping category"
    
    print(f"🗣️ User: {user_input}")
    
    result = await finance_agent.run(
        user_input, 
        model=model,
        deps=db,
        model_settings={'temperature': 0.0}
    )
    
    print(f"🤖 Assistant: {result.output}")
    
    # Verify in DB
    expenses = db.get_expenses_by_category(ExpenseCategory.SHOPPING)
    found = any(e.description == test_desc and e.amount == 12.34 for e in expenses)
    
    if found:
        print("✅ Success: Expense recorded in Supabase by Agent!")
    else:
        print("❌ Failure: Expense not found in Supabase.")

    # 3. Test View History
    print("\n🗣️ User: Show my shopping expenses")
    result = await finance_agent.run(
        "Show my shopping expenses", 
        model=model,
        deps=db,
        model_settings={'temperature': 0.0}
    )
    print(f"🤖 Assistant: {result.output}")
    
    if str(12.34) in result.output and test_desc in result.output:
        print("✅ Success: Assistant correctly retrieved history from Supabase!")
    else:
        print("❌ Failure: Assistant failed to show the recorded expense.")

if __name__ == "__main__":
    asyncio.run(test_end_to_end())
