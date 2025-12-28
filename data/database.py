import os
from typing import List, Optional
from datetime import datetime
from dotenv import load_dotenv
from supabase import create_client, Client
from core.models import Transaction, ExpenseCategory, TransactionType
from core.interfaces import ExpenseRepository, IncomeRepository
from core.observability import log_and_handle_error
from postgrest.exceptions import APIError

load_dotenv()

class BaseSupabaseRepository:
    def __init__(self):
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
        if not self.url or not self.key:
            self.supabase = None
        else:
            self.supabase: Client = create_client(self.url, self.key)
    
    def _check_client(self):
        if not self.supabase:
            raise ValueError("Supabase is not configured. Please set SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY in .env")

    def _infer_type(self, item: dict) -> TransactionType:
        if "type" in item and item["type"]:
            return TransactionType(item["type"])
        if item["category"] == ExpenseCategory.INCOME.value:
            return TransactionType.INCOME
        return TransactionType.EXPENSE

    def _map_to_domain(self, item: dict) -> Transaction:
        return Transaction(
            id=item["id"],
            amount=item["amount"],
            type=self._infer_type(item),
            category=ExpenseCategory(item["category"]),
            description=item["description"],
            date=datetime.fromisoformat(item["date"].replace("Z", "+00:00"))
        )

class SupabaseExpenseRepository(BaseSupabaseRepository, ExpenseRepository):
    """
    Concrete implementation of ExpenseRepository using Supabase.
    """
    @log_and_handle_error
    def add_expense(self, expense: Transaction) -> Transaction:
        self._check_client()
        data = {
            "amount": expense.amount,
            "category": expense.category.value,
            "description": expense.description,
            "date": expense.date.isoformat(),
            "type": TransactionType.EXPENSE.value
        }
        try:
            response = self.supabase.table("expenses").insert(data).execute()
        except APIError as e:
            if e.code == 'PGRST204' or "Could not find the 'type' column" in str(e):
                del data["type"]
                response = self.supabase.table("expenses").insert(data).execute()
            else:
                raise e

        if response.data:
            new_data = response.data[0]
            expense.id = new_data["id"]
        return expense

    @log_and_handle_error
    def get_all_expenses(self) -> List[Transaction]:
        self._check_client()
        # Implicitly filter for non-income if needed, but for now we follow old logic or just generic
        # Ideally we should filter by type='expense'
        response = self.supabase.table("expenses").select("*").order("date", desc=True).execute()
        return [self._map_to_domain(item) for item in response.data]
    
    @log_and_handle_error
    def get_expenses_by_category(self, category: ExpenseCategory) -> List[Transaction]:
        self._check_client()
        response = self.supabase.table("expenses").select("*").eq("category", category.value).order("date", desc=True).execute()
        return [self._map_to_domain(item) for item in response.data]
    
    @log_and_handle_error
    def get_expenses_by_date_range(
        self, 
        start_date: Optional[datetime] = None, 
        end_date: Optional[datetime] = None
    ) -> List[Transaction]:
        self._check_client()
        query = self.supabase.table("expenses").select("*")
        if start_date:
            query = query.gte("date", start_date.isoformat())
        if end_date:
            query = query.lte("date", end_date.isoformat())
        
        response = query.order("date", desc=True).execute()
        return [self._map_to_domain(item) for item in response.data]
    
    @log_and_handle_error
    def get_total_spending(self) -> float:
        self._check_client()
        # Sum only non-income
        response = self.supabase.table("expenses").select("amount").execute()
        return sum(item["amount"] for item in response.data)
    
    @log_and_handle_error
    def clear_all_expenses(self):
        self._check_client()
        self.supabase.table("expenses").delete().neq("id", 0).execute() # Clear all logic changed slightly to allow clearing logic 

class SupabaseIncomeRepository(BaseSupabaseRepository, IncomeRepository):
    """
    Concrete implementation of IncomeRepository using Supabase.
    """
    @log_and_handle_error
    def add_income(self, income: Transaction) -> Transaction:
        self._check_client()
        data = {
            "amount": income.amount,
            "category": ExpenseCategory.INCOME.value,
            "description": income.description,
            "date": income.date.isoformat(),
            "type": TransactionType.INCOME.value
        }
        try:
            response = self.supabase.table("income").insert(data).execute()
        except APIError as e:
            if e.code == 'PGRST204' or "Could not find the 'type' column" in str(e):
                del data["type"]
                response = self.supabase.table("income").insert(data).execute()
            else:
                raise e

        if response.data:
            new_data = response.data[0]
            income.id = new_data["id"]
        return income

    @log_and_handle_error
    def get_all_income(self) -> List[Transaction]:
        self._check_client()
        response = self.supabase.table("income").select("*").order("date", desc=True).execute()
        return [self._map_to_domain(item) for item in response.data]

    def get_total_income(self) -> float:
        self._check_client()
        response = self.supabase.table("income").select("amount").execute()
        return sum(item["amount"] for item in response.data)