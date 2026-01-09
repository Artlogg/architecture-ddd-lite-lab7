class FakePaymentGateway:
    def __init__(self):
        self.charges = []

    def charge(self, order_id, money):
        self.charges.append((order_id, money.amount))
