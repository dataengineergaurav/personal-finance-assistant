from typing import List, Protocol, Optional
from datetime import datetime
from core.models import Transaction, ExpenseCategory

# Note: We are using the 'Expense' model for both Income and Expense for now, 
# as they share the same structure (amount, description, date).

class ExpenseRepository(Protocol):
    """
    Interface for managing Expense transactions.
    """
    
    def add_expense(self, expense: Transaction) -> Transaction:
        """Persist a new expense record."""
        ...

    def get_all_expenses(self) -> List[Transaction]:
        """Retrieve all expense records."""
        ...

    def get_expenses_by_category(self, category: ExpenseCategory) -> List[Transaction]:
        """Retrieve expenses filtered by category."""
        ...

    def get_expenses_by_date_range(
        self, 
        start_date: Optional[datetime] = None, 
        end_date: Optional[datetime] = None
    ) -> List[Transaction]:
        """Retrieve expenses within a date range."""
        ...

    def get_total_spending(self) -> float:
        """Calculate total spending amount."""
        ...
    
    def clear_all_expenses(self) -> None:
        """Clear all expense records."""
        ...

class IncomeRepository(Protocol):
    """
    Interface for managing Income transactions.
    """

    def add_income(self, income: Transaction) -> Transaction:
        """Persist a new income record."""
        ...
    
    def get_all_income(self) -> List[Transaction]:
        """Retrieve all income records."""
        ...

    def get_total_income(self) -> float:
        """Calculate total income amount."""
        ...
