import pytest
from domain.order import Order, OrderLine
from domain.money import Money
from application.pay_order_use_case import PayOrderUseCase
from infrastructure.in_memory_order_repository import InMemoryOrderRepository
from infrastructure.fake_payment_gateway import FakePaymentGateway


def create_order_with_items():
    order = Order("order-1")
    order.add_line(OrderLine("Item A", Money(100), 2))
    return order


def test_successful_payment():
    repo = InMemoryOrderRepository()
    gateway = FakePaymentGateway()
    order = create_order_with_items()
    repo.save(order)

    use_case = PayOrderUseCase(repo, gateway)
    result = use_case.execute("order-1")

    assert result["status"] == "PAID"
    assert result["amount"] == 200
    assert len(gateway.charges) == 1


def test_cannot_pay_empty_order():
    repo = InMemoryOrderRepository()
    gateway = FakePaymentGateway()
    order = Order("order-2")
    repo.save(order)

    use_case = PayOrderUseCase(repo, gateway)

    with pytest.raises(ValueError):
        use_case.execute("order-2")


def test_cannot_pay_twice():
    repo = InMemoryOrderRepository()
    gateway = FakePaymentGateway()
    order = create_order_with_items()
    repo.save(order)

    use_case = PayOrderUseCase(repo, gateway)
    use_case.execute("order-1")

    with pytest.raises(ValueError):
        use_case.execute("order-1")


def test_cannot_modify_paid_order():
    order = create_order_with_items()
    order.pay()

    with pytest.raises(ValueError):
        order.add_line(OrderLine("Item B", Money(50), 1))


def test_total_amount_calculation():
    order = Order("order-3")
    order.add_line(OrderLine("Item A", Money(100), 1))
    order.add_line(OrderLine("Item B", Money(50), 2))

    assert order.total_amount().amount == 200
