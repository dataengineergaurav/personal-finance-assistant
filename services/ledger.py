from typing import List, Optional
from datetime import datetime
from core.models import Expense, ExpenseCategory, TransactionType
from data.database import ExpenseDatabase

class LedgerService:
    def __init__(self, db: ExpenseDatabase):
        self.db = db

    def record_transaction(self, amount: float, category: ExpenseCategory, description: str) -> Expense:
        """
        Record a new EXPENSE transaction.
        """
        expense = Expense(
            amount=amount,
            category=category,
            description=description,
            type=TransactionType.EXPENSE,
            date=datetime.now()
        )
        return self.db.add_expense(expense)

    def record_income(self, amount: float, source: str, description: str) -> Expense:
        """
        Record a new INCOME transaction.
        """
        income = Expense(
            amount=amount,
            category=ExpenseCategory.INCOME, # Use the generic INCOME category
            description=f"{source}: {description}",
            type=TransactionType.INCOME,
            date=datetime.now()
        )
        return self.db.add_expense(income)

    def get_transaction_history(self, category: Optional[ExpenseCategory] = None) -> List[Expense]:
        if category:
            return self.db.get_expenses_by_category(category)
        return self.db.get_all_expenses()

    def calculate_total_spending(self, expenses: List[Expense]) -> float:
        """Sum of EXPENSES only."""
        return sum(e.amount for e in expenses if e.type == TransactionType.EXPENSE)

    def calculate_total_income(self, expenses: List[Expense]) -> float:
        """Sum of INCOME only."""
        return sum(e.amount for e in expenses if e.type == TransactionType.INCOME)

    def format_history_report(self, category: Optional[ExpenseCategory], expenses: List[Expense]) -> str:
        if not expenses:
            return f"No records found for {category.value if category else 'all categories'}."

        title = f"LEDGER REPORT: {category.value.upper() if category else 'ALL TRANSACTIONS'}"
        report = f"{'='*40}\n{title}\n{'='*40}\n"
        
        for e in expenses:
            date_str = e.date.strftime('%Y-%m-%d')
            # Visual indicator for income/expense
            prefix = "+" if e.type == TransactionType.INCOME else "-"
            report += f"[{date_str}] {prefix} ${e.amount:>8.2f} | {e.category.value:12} | {e.description}\n"
            
        total_spent = self.calculate_total_spending(expenses)
        total_income = self.calculate_total_income(expenses)
        
        report += f"{'-'*40}\n"
        report += f"TOTAL INCOME:   ${total_income:>10.2f}\n"
        report += f"TOTAL SPENDING: ${total_spent:>10.2f}\n"
        report += f"NET FLOW:       ${(total_income - total_spent):>10.2f}\n"
        report += f"{'='*40}"
        return report
