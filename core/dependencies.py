from dataclasses import dataclass
from typing import Any
from core.interfaces import ExpenseRepository, IncomeRepository

@dataclass
class FinanceDependencies:
    """
    Aggregates all dependencies required by the Finance Domain logic.
    Using this explicitly makes it clear what the agent needs.
    """
    expense_repo: ExpenseRepository
    income_repo: IncomeRepository

@dataclass
class DataEngineDependencies:
    """
    Dependencies for the Data Warehousing Agent.
    """
    pool: Any # asyncpg.Pool

