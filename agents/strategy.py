from pydantic_ai import Agent, RunContext
from agents.finance import finance_agent
from data.database import ExpenseDatabase
from prompts.persona import STRATEGY_PERSONA
from core.settings import settings
from core.models import StrategyResponse

# Initialize the High-Level Wealth Strategy Agent
strategy_agent = Agent(
    model=settings.get_model(),
    deps_type=ExpenseDatabase,
    system_prompt=STRATEGY_PERSONA,
    output_type=StrategyResponse
)

@strategy_agent.tool
async def query_finance_assistant(ctx: RunContext[ExpenseDatabase], query: str) -> str:
    """
    Delegates a query to the Finance Assistant for data retrieval or expense recording.
    Use this for:
    - Recording new expenses
    - Viewing history
    - Getting basic spending analysis
    - Generating budget plans
    """
    # We pass the same database dependency to the sub-agent
    result = await finance_agent.run(query, deps=ctx.deps)
    return result.output

@strategy_agent.tool
def evaluate_goal_feasibility(ctx: RunContext[ExpenseDatabase], goal_name: str, amount: float) -> str:
    """
    Analyze if a specific financial goal is feasible based on current data.
    """
    # This is a placeholder for more complex logic
    # In a real scenario, it might fetch historical savings rate
    return f"Goal '{goal_name}' for ${amount} is under review. Please ask the Finance Assistant for my savings history first."
