from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime
from core.models import Expense, ExpenseCategory

class BaseExpenseDatabase(ABC):
    @abstractmethod
    def add_expense(self, expense: Expense) -> Expense:
        """Record a new financial transaction."""
        pass
    
    @abstractmethod
    def get_all_expenses(self) -> List[Expense]:
        """Retrieve all transaction history."""
        pass
    
    @abstractmethod
    def get_expenses_by_category(self, category: ExpenseCategory) -> List[Expense]:
        """Retrieve transactions filtered by category."""
        pass
    
    @abstractmethod
    def get_total_spending(self) -> float:
        """Calculate total spending across all categories."""
        pass

    @abstractmethod
    def clear_all(self):
        """Wipe all data from the database."""
        pass
