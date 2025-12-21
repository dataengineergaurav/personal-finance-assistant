from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from enum import Enum


class ExpenseCategory(str, Enum):
    FOOD = "food"
    TRANSPORT = "transport"
    ENTERTAINMENT = "entertainment"
    UTILITIES = "utilities"
    HEALTHCARE = "healthcare"
    SHOPPING = "shopping"
    EDUCATION = "education"
    OTHER = "other"


class Expense(BaseModel):
    id: Optional[int] = None
    amount: float = Field(gt=0, description="Expense amount (must be positive)")
    category: ExpenseCategory
    description: str
    date: datetime = Field(default_factory=datetime.now)


class SpendingSummary(BaseModel):
    category: ExpenseCategory
    total_amount: float
    expense_count: int
    percentage: float


class FinancialReport(BaseModel):
    total_spent: float
    categories: dict[str, float]
    top_category: str
    recommendations: List[str]


class BudgetRecommendation(BaseModel):
    category: ExpenseCategory
    current_spending: float
    recommended_budget: float
    status: str
    advice: str


class BudgetReport(BaseModel):
    monthly_income: float
    needs: float
    wants: float
    savings: float
    advice: List[str]


class StrategyResponse(BaseModel):
    analysis: str
    steps: List[str]
    confidence_score: float


class FinancialGoal(BaseModel):
    name: str
    target_amount: float
    deadline: Optional[datetime] = None
    priority: int = 1  # 1-5, 1 being highest