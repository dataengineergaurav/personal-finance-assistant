import os
import gspread
from typing import List, Optional
from datetime import datetime
from google.oauth2.service_account import Credentials
from core.models import Expense, ExpenseCategory
from data.base import BaseExpenseDatabase

class GoogleSheetDatabase(BaseExpenseDatabase):
    def __init__(self):
        self.credentials_path = os.getenv("GSHEET_CREDENTIALS_FILE")
        self.spreadsheet_id = os.getenv("GSHEET_ID")
        self.sheet_name = os.getenv("GSHEET_NAME", "Expenses")
        
        if not self.credentials_path or not self.spreadsheet_id:
            self.client = None
            self.sheet = None
        else:
            try:
                scopes = ["https://www.googleapis.com/auth/spreadsheets"]
                creds = Credentials.from_service_account_file(self.credentials_path, scopes=scopes)
                self.client = gspread.authorize(creds)
                spreadsheet = self.client.open_by_key(self.spreadsheet_id)
                
                try:
                    self.sheet = spreadsheet.worksheet(self.sheet_name)
                except gspread.exceptions.WorksheetNotFound:
                    # Create sheet if not exists with headers
                    self.sheet = spreadsheet.add_worksheet(title=self.sheet_name, rows="100", cols="5")
                    self.sheet.append_row(["ID", "Date", "Category", "Amount", "Description"])
            except Exception as e:
                print(f"⚠️ Google Sheets Connection Error: {str(e)}")
                self.client = None
                self.sheet = None

    def _check_client(self):
        if not self.sheet:
            raise ValueError("Google Sheets is not configured or accessible. Check GSHEET_CREDENTIALS_FILE and GSHEET_ID.")

    def add_expense(self, expense: Expense) -> Expense:
        self._check_client()
        # For GSheets, we'll use timestamp as an ID for now
        expense_id = int(datetime.now().timestamp())
        row = [
            expense_id,
            expense.date.isoformat(),
            expense.category.value,
            expense.amount,
            expense.description
        ]
        self.sheet.append_row(row)
        expense.id = expense_id
        return expense

    def get_all_expenses(self) -> List[Expense]:
        self._check_client()
        rows = self.sheet.get_all_records()
        expenses = []
        for row in rows:
            expenses.append(Expense(
                id=int(row["ID"]),
                date=datetime.fromisoformat(row["Date"]),
                category=ExpenseCategory(row["Category"]),
                amount=float(row["Amount"]),
                description=row["Description"]
            ))
        # Return sorted by date descending for compatibility
        return sorted(expenses, key=lambda x: x.date, reverse=True)

    def get_expenses_by_category(self, category: ExpenseCategory) -> List[Expense]:
        all_expenses = self.get_all_expenses()
        return [e for e in all_expenses if e.category == category]

    def get_total_spending(self) -> float:
        all_expenses = self.get_all_expenses()
        return sum(e.amount for e in all_expenses)

    def clear_all(self):
        self._check_client()
        # Keep headers
        self.sheet.clear()
        self.sheet.append_row(["ID", "Date", "Category", "Amount", "Description"])
