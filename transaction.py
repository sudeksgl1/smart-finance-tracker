from datetime import datetime

class Transaction:
    def __init__(self, amount, category, transaction_type, description=""):
        self.amount = amount
        self.category = category
        self.transaction_type = transaction_type
        self.description = description
        self.date = datetime.now().strftime("%Y-%m-%d")

    def to_dict(self):
        return {
            "amount": self.amount,
            "category": self.category,
            "transaction_type": self.transaction_type,
            "description": self.description,
            "date": self.date
        }