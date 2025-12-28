from pydantic_ai import Agent, RunContext
from core.interfaces import ExpenseRepository, IncomeRepository
from core.dependencies import FinanceDependencies
from services.ledger import LedgerService
from services.advisor import AdvisorService
from services.categories import CategoryService
from core.observability import log_and_handle_error
from prompts.persona import FINANCIAL_PERSONA, SUMMARY_TEMPLATE
from core.settings import settings

# Initialize the Professional Financial Assistant
# We don't define the model here anymore to allow injection
finance_agent = Agent(
    'openai:gpt-4o', # Default, will be overridden by container
    deps_type=FinanceDependencies,
    system_prompt=FINANCIAL_PERSONA
)

@finance_agent.tool
@log_and_handle_error
def add_expense(ctx: RunContext[FinanceDependencies], amount: float, category: str, description: str) -> str:
    """
    Record a new expense transaction.
    Args:
        amount: The dollar amount spent (positive number).
        category: Category of expense (food, transport, entertainment, etc.)
        description: Brief details of the purchase.
    """
    ledger = LedgerService(ctx.deps.expense_repo, ctx.deps.income_repo)
    # Use CategoryService for robust mapping
    expense_cat = CategoryService.map_to_category(category)
    expense = ledger.record_expense(amount, expense_cat, description)
    return SUMMARY_TEMPLATE.format(
        category=expense.category.value,
        amount=expense.amount,
        description=expense.description
    )

@finance_agent.tool
@log_and_handle_error
def add_income(ctx: RunContext[FinanceDependencies], amount: float, source: str, description: str = "") -> str:
    """
    Record a new income (deposit, salary, etc.).
    Args:
        amount: The dollar amount earned (positive number).
        source: Source of income (Salary, Freelance, Gift, etc.)
        description: Optional details.
    """
    ledger = LedgerService(ctx.deps.expense_repo, ctx.deps.income_repo)
    income = ledger.record_income(amount, source, description)
    return f"💰 Income Recorded: +${income.amount:.2f} from {source}"

@finance_agent.tool
@log_and_handle_error
def view_history(ctx: RunContext[FinanceDependencies], category_name: str = "all") -> str:
    """
    Retrieve and format the transaction history (Income and Expenses).
    Args:
        category_name: Optional category to filter by (or 'all').
    """
    ledger = LedgerService(ctx.deps.expense_repo, ctx.deps.income_repo)
    category = None
    if category_name and category_name.lower() != 'all':
        category = CategoryService.map_to_category(category_name)
    
    expenses = ledger.get_transaction_history(category)
    return ledger.format_history_report(category, expenses)

@finance_agent.tool
@log_and_handle_error
def get_financial_advice(ctx: RunContext[FinanceDependencies]) -> str:
    """
    Analyze spending patterns and provide actionable financial advice.
    """
    advisor = AdvisorService()
    ledger = LedgerService(ctx.deps.expense_repo, ctx.deps.income_repo)
    expenses = ledger.get_transaction_history()
    analysis = advisor.analyze_spending(expenses)
    
    res = f"FINANCIAL ANALYSIS\n{'='*20}\n"
    res += f"Total Spending: ${analysis.total_spent:.2f}\n"
    res += f"Top Category: {analysis.top_category}\n\n"
    res += "Recommendations:\n"
    for rec in analysis.recommendations:
        res += f"- {rec}\n"
    return res

@finance_agent.tool
@log_and_handle_error
def get_budget_plan(ctx: RunContext[FinanceDependencies], monthly_income: float) -> str:
    """
    Generate a professional budget plan based on monthly income.
    Args:
        monthly_income: Your total monthly earnings.
    """
    advisor = AdvisorService()
    plan = advisor.get_budget_advice(monthly_income)
    
    res = f"BUDGET PLAN FOR INCOME: ${monthly_income:.2f}\n{'='*40}\n"
    res += f"- Needs (50%):    ${plan.needs:>10.2f}\n"
    res += f"- Wants (30%):    ${plan.wants:>10.2f}\n"
    res += f"- Savings (20%):  ${plan.savings:>10.2f}\n"
    res += f"{'-'*40}\nExpert Suggestions:\n"
    for s in plan.advice:
        res += f"• {s}\n"
    return res