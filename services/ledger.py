from typing import List, Optional
from datetime import datetime
from core.models import Transaction, ExpenseCategory, TransactionType
from core.interfaces import ExpenseRepository
from data.database import SupabaseExpenseRepository # for type aliasing if needed, but better to just use interface


from core.interfaces import ExpenseRepository, IncomeRepository

class LedgerService:
    def __init__(self, expense_repo: ExpenseRepository, income_repo: IncomeRepository):
        self.expense_repo = expense_repo
        self.income_repo = income_repo

    def record_expense(self, amount: float, category: ExpenseCategory, description: str) -> Transaction:
        """
        Record a new EXPENSE transaction.
        """
        expense = Transaction(
            amount=amount,
            category=category,
            description=description,
            type=TransactionType.EXPENSE,
            date=datetime.now()
        )
        return self.expense_repo.add_expense(expense)

    def record_income(self, amount: float, source: str, description: str) -> Transaction:
        """
        Record a new INCOME transaction.
        """
        income = Transaction(
            amount=amount,
            category=ExpenseCategory.INCOME, # Use the generic INCOME category
            description=f"{source}: {description}",
            type=TransactionType.INCOME,
            date=datetime.now()
        )
        return self.income_repo.add_income(income)

    def get_transaction_history(self, category: Optional[ExpenseCategory] = None) -> List[Transaction]:
        # If specific category (and not Income), get from expense repo
        if category:
            if category == ExpenseCategory.INCOME:
                return self.income_repo.get_all_income()
            return self.expense_repo.get_expenses_by_category(category)
        
        # If all, get both and merge
        expenses = self.expense_repo.get_all_expenses()
        income = self.income_repo.get_all_income()
        
        # Merge and sort by date desc
        all_tx = expenses + income
        all_tx.sort(key=lambda x: x.date, reverse=True)
        return all_tx

    def calculate_total_spending(self, expenses: List[Transaction]) -> float:
        """Sum of EXPENSES only."""
        return sum(e.amount for e in expenses if e.type == TransactionType.EXPENSE)

    def calculate_total_income(self, expenses: List[Transaction]) -> float:
        """Sum of INCOME only."""
        return sum(e.amount for e in expenses if e.type == TransactionType.INCOME)

    def format_history_report(self, category: Optional[ExpenseCategory], expenses: List[Transaction]) -> str:
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
