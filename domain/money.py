class Money:
    def __init__(self, amount: int):
        if amount < 0:
            raise ValueError("Amount cannot be negative")
        self.amount = amount

    def add(self, other):
        return Money(self.amount + other.amount)

    def __eq__(self, other):
        return isinstance(other, Money) and self.amount == other.amount
