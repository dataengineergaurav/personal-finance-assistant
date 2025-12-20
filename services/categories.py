from typing import Optional
from models import ExpenseCategory

class CategoryService:
    @staticmethod
    def map_to_category(text: str) -> ExpenseCategory:
        """
        Professional mapping of natural language to financial categories.
        """
        text = text.lower()
        
        # Mapping clusters
        mappings = {
            'food': ['lunch', 'dinner', 'breakfast', 'restaurant', 'cafe', 'grocery', 'food', 'starbucks', 'mcdonalds'],
            'transport': ['uber', 'taxi', 'fuel', 'gas', 'metro', 'bus', 'train', 'parking', 'flight'],
            'entertainment': ['movie', 'cinema', 'game', 'netflix', 'spotify', 'concert', 'bar', 'club'],
            'utilities': ['rent', 'electricity', 'water', 'gas', 'internet', 'phone', 'bill'],
            'healthcare': ['doctor', 'medicine', 'pharmacy', 'hospital', 'dentist', 'clinic'],
            'shopping': ['shopping', 'amazon', 'clothes', 'shoes', 'electronics', 'gift'],
            'education': ['course', 'book', 'tuition', 'school', 'workshop'],
        }

        for category, keywords in mappings.items():
            if any(kw in text for kw in keywords):
                return ExpenseCategory(category)
        
        return ExpenseCategory.OTHER
