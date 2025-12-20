from typing import List, Optional
from datetime import datetime
from models import Expense, ExpenseCategory
from database import ExpenseDatabase

class LedgerService:
    def __init__(self, db: ExpenseDatabase):
        self.db = db

    def record_transaction(self, amount: float, category: ExpenseCategory, description: str) -> Expense:
        """
        Record a new financial transaction in the ledger.
        """
        expense = Expense(
            amount=amount,
            category=category,
            description=description,
            date=datetime.now()
        )
        return self.db.add_expense(expense)

    def get_transaction_history(self, category: Optional[ExpenseCategory] = None) -> List[Expense]:
        """
        Retrieve transaction history, optionally filtered by category.
        """
        if category:
            return self.db.get_expenses_by_category(category)
        return self.db.get_all_expenses()

    def calculate_total_spending(self, expenses: List[Expense]) -> float:
        """
        Calculate the total sum of a list of expenses.
        """
        return sum(e.amount for e in expenses)

    def format_history_report(self, category: Optional[ExpenseCategory], expenses: List[Expense]) -> str:
        """
        Produce a professional ledger report.
        """
        if not expenses:
            return f"No records found for {category.value if category else 'all categories'}."

        title = f"LEDGER REPORT: {category.value.upper() if category else 'ALL TRANSACTIONS'}"
        report = f"{'='*40}\n{title}\n{'='*40}\n"
        
        for e in expenses:
            date_str = e.date.strftime('%Y-%m-%d')
            report += f"[{date_str}] {e.category.value:12} | ${e.amount:>8.2f} | {e.description}\n"
            
        total = self.calculate_total_spending(expenses)
        report += f"{'-'*40}\nTOTAL SPENDING: ${total:>23.2f}\n{'='*40}"
        return report
