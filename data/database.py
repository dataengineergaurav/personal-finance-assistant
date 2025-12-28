import os
from typing import List, Optional
from datetime import datetime
from dotenv import load_dotenv
from supabase import create_client, Client
from core.models import Expense, ExpenseCategory, TransactionType
from postgrest.exceptions import APIError

load_dotenv()

class ExpenseDatabase:
    def __init__(self):
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
        if not self.url or not self.key:
            # We don't raise an error here to allow the agent to start even if DB is not configured,
            # but we'll check it when performing operations.
            self.supabase = None
        else:
            self.supabase: Client = create_client(self.url, self.key)
    
    def _check_client(self):
        if not self.supabase:
            raise ValueError("Supabase is not configured. Please set SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY in .env")

    def add_expense(self, expense: Expense) -> Expense:
        self._check_client()
        data = {
            "amount": expense.amount,
            "category": expense.category.value,
            "description": expense.description,
            "date": expense.date.isoformat(),
            "type": expense.type.value # Persist the type
        }
        try:
            # We try to insert. If 'type' column is missing in DB, this might fail with PGRST204
            response = self.supabase.table("expenses").insert(data).execute()
        except APIError as e:
            # Check if this is a "column not found" error (PGRST204 is generic "Columns not found", 
            # or sometimes 400 Bad Request if strict).
            # The error message from reproduction was: code='PGRST204', message="Could not find the 'type' column..."
            if e.code == 'PGRST204' or "Could not find the 'type' column" in str(e):
                # Fallback: remove 'type' and try again
                del data["type"]
                response = self.supabase.table("expenses").insert(data).execute()
            else:
                raise e

        if response.data:
            new_data = response.data[0]
            expense.id = new_data["id"]
        return expense
    
    def _infer_type(self, item: dict) -> TransactionType:
        # If 'type' exists, use it.
        # Otherwise, infer from category: 'income' -> INCOME, else EXPENSE.
        if "type" in item and item["type"]:
            return TransactionType(item["type"])
        
        # Fallback inference
        if item["category"] == ExpenseCategory.INCOME.value:
            return TransactionType.INCOME
        return TransactionType.EXPENSE

    def get_all_expenses(self) -> List[Expense]:
        self._check_client()
        response = self.supabase.table("expenses").select("*").order("date", desc=True).execute()
        return [
            Expense(
                id=item["id"],
                amount=item["amount"],
                type=self._infer_type(item),
                category=ExpenseCategory(item["category"]),
                description=item["description"],
                date=datetime.fromisoformat(item["date"].replace("Z", "+00:00"))
            )
            for item in response.data
        ]
    
    def get_expenses_by_category(self, category: ExpenseCategory) -> List[Expense]:
        self._check_client()
        response = self.supabase.table("expenses").select("*").eq("category", category.value).order("date", desc=True).execute()
        return [
            Expense(
                id=item["id"],
                amount=item["amount"],
                type=self._infer_type(item),
                category=ExpenseCategory(item["category"]),
                description=item["description"],
                date=datetime.fromisoformat(item["date"].replace("Z", "+00:00"))
            )
            for item in response.data
        ]
    
    def get_expenses_by_date_range(
        self, 
        start_date: Optional[datetime] = None, 
        end_date: Optional[datetime] = None
    ) -> List[Expense]:
        self._check_client()
        query = self.supabase.table("expenses").select("*")
        if start_date:
            query = query.gte("date", start_date.isoformat())
        if end_date:
            query = query.lte("date", end_date.isoformat())
        
        response = query.order("date", desc=True).execute()
        return [
            Expense(
                id=item["id"],
                amount=item["amount"],
                type=self._infer_type(item),
                category=ExpenseCategory(item["category"]),
                description=item["description"],
                date=datetime.fromisoformat(item["date"].replace("Z", "+00:00"))
            )
            for item in response.data
        ]
    
    def get_total_spending(self) -> float:
        self._check_client()
        response = self.supabase.table("expenses").select("amount").execute()
        return sum(item["amount"] for item in response.data)
    
    def clear_all(self):
        self._check_client()
        # In a real app, this might be dangerous, but keeping it for compatibility with original code
        self.supabase.table("expenses").delete().neq("id", 0).execute()