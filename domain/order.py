from enum import Enum
from domain.money import Money


class OrderStatus(Enum):
    CREATED = "CREATED"
    PAID = "PAID"


class OrderLine:
    def __init__(self, product_name: str, price: Money, qty: int):
        if qty <= 0:
            raise ValueError("Quantity must be positive")
        self.product_name = product_name
        self.price = price
        self.qty = qty

    def total_price(self):
        return Money(self.price.amount * self.qty)


class Order:
    def __init__(self, order_id: str):
        self.order_id = order_id
        self.lines = []
        self.status = OrderStatus.CREATED

    def add_line(self, line: OrderLine):
        if self.status == OrderStatus.PAID:
            raise ValueError("Cannot modify paid order")
        self.lines.append(line)

    def total_amount(self):
        total = Money(0)
        for line in self.lines:
            total = total.add(line.total_price())
        return total

    def pay(self):
        if len(self.lines) == 0:
            raise ValueError("Cannot pay empty order")
        if self.status == OrderStatus.PAID:
            raise ValueError("Order already paid")
        self.status = OrderStatus.PAID
