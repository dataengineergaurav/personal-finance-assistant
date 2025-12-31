import asyncio
import os
import sys
import argparse
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Project imports
from core.container import Container, create_finance_agent
from core.settings import settings
from core.observability import track_agent_run, log_agent_result

async def main():
    parser = argparse.ArgumentParser(description='Personal Finance Assistant')
    parser.add_argument('--model', type=str, choices=['ollama', 'openai', 'gemini', 'google'],
                      help='Model provider to use (overrides MODEL_PROVIDER env var)')
    args = parser.parse_args()

    # Domain models and services
    try:
        deps = Container.get_finance_dependencies()
    except Exception as e:
        print(f"❌ Database Error: {str(e)}")
        sys.exit(1)

    # Resolve Model
    provider = args.model or settings.MODEL_PROVIDER
    model = settings.get_model(provider)

    print("=" * 60)
    print("💰 Personal Finance Assistant (Domain-Driven Edition)")
    print("=" * 60)
    print(f"\n🤖 Provider: {provider.capitalize()}")
    print("\nI can help you:\n"
          "  • Track expenses           (e.g., 'I spent $15 on lunch')\n"
          "  • Record income            (e.g., 'Salary $5000 received')\n"
          "  • View spending            (e.g., 'Show my food expenses')\n"
          "  • Get expert advice        (e.g., 'Analyze my spending')\n"
          "  • Budgeting plans          (e.g., 'Budget for $5000 income')\n")
    print("Type 'quit' or 'exit' to end the session.\n")

    history = []

    while True:
        try:
            user_input = input("🗣️  You: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("\n👋 Stay financially healthy. Goodbye!")
                break

            # Execute Request
            # We pass the pre-resolved model object to ensure correctness
            async with track_agent_run("Finance Clerk CLI", str(provider), {"query": user_input}):
                finance_agent = create_finance_agent()
                result = await finance_agent.run(
                    user_input,
                    model=model,
                    deps=deps,
                    message_history=history,
                    model_settings={'temperature': 0.0}
                )
                log_agent_result(result.output)

            # Update conversation history
            history = result.all_messages()
            print(f"\n🤖 Assistant: {result.output}")

        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            print("Please try again or type 'quit' to exit.")

if __name__ == "__main__":
    asyncio.run(main())
