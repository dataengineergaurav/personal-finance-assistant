import asyncio
import os
import sys
import argparse
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Project imports
from agents.strategy import strategy_agent
from core.settings import settings

async def main():
    parser = argparse.ArgumentParser(description='Wealth Strategy Advisor')
    parser.add_argument('--model', type=str, choices=['ollama', 'openai', 'gemini', 'google'],
                      help='Model provider to use (overrides MODEL_PROVIDER env var)')
    args = parser.parse_args()

    # Domain models and services
    try:
        db = settings.get_db()
    except Exception as e:
        print(f"❌ Database Error: {str(e)}")
        sys.exit(1)

    # Resolve Model
    provider = args.model or settings.MODEL_PROVIDER
    model = settings.get_model(provider)

    print("=" * 60)
    print("📈 Wealth Strategy Director (Multi-Agent Edition)")
    print("=" * 60)
    print(f"\n🧠 Director Provider: {provider.capitalize()}")
    print("\nI oversee your long-term wealth. I can:\n"
          "  • Plan large purchases     (e.g., 'Can I buy a Tesla? Check my history')\n"
          "  • Debt strategies          (e.g., 'How do I pay off my credit card?')\n"
          "  • Investment advice        (e.g., 'Where should I put my extra $500?')\n"
          "  • Complex Goal Planning    (e.g., 'Save $100k for a house in 5 years')\n")
    print("Type 'quit' or 'exit' to end the session.\n")

    history = []

    while True:
        try:
            user_input = input("🗣️  Strategist Query: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("\n👋 Plan wisely. Goodbye!")
                break

            # Execute Request
            result = await strategy_agent.run(
                user_input,
                model=model,
                deps=db,
                message_history=history,
            )

            # Update conversation history
            history = result.all_messages()
            
            # Since strategy_agent has output_type=StrategyResponse
            output = result.output
            print(f"\n🏆 STRATEGIC ANALYSIS")
            print(f"{'-'*20}")
            print(f"{output.analysis}")
            print(f"\n✅ ACTION STEPS:")
            for i, step in enumerate(output.steps, 1):
                print(f"  {i}. {step}")
            print(f"\n📊 Confidence: {output.confidence_score * 100:.1f}%")
            print(f"{'='*60}\n")

        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Strategic Error: {str(e)}")
            # For debugging, print full trace
            import traceback
            traceback.print_exc()
            print("Please try again or type 'quit' to exit.")

if __name__ == "__main__":
    asyncio.run(main())
