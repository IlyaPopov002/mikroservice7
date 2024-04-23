# 1. Поменять int на UUID в функциях

from uuid import UUID, uuid4
from fastapi import Depends
from datetime import datetime
import asyncio

from app.models.order import Order, OrderStatus
from app.rabbitmq import send_to_receipt_queue
from app.repositories.db_order_repo import OrderRepo


# from app.repositories.local_order_repo import OrderRepo

# from app.services.receipt_service import ReceiptService


class OrderService():
    order_repo: OrderRepo

    # receipt_service: ReceiptService

    # deliveryman_repo: DeliverymenRepo

    # def __init__(self, order_repo: OrderRepo = Depends(OrderRepo),
    #              receipt_service: ReceiptService = Depends(ReceiptService)) -> None:
    def __init__(self, order_repo: OrderRepo = Depends(OrderRepo), ) -> None:
        self.order_repo = order_repo
        # self.receipt_service = receipt_service
        # self.deliveryman_repo = DeliverymenRepo()

    def get_order(self) -> list[Order]:
        return self.order_repo.get_order()

    def create_order(self, address_info: str, customer_info: str, order_info: str) -> Order:
        order = Order(ord_id=uuid4(), status=OrderStatus.CREATE, address_info=address_info, customer_info=customer_info,
                      create_date=datetime.now(), completion_date=None, order_info=order_info)
        return self.order_repo.create_order(order)

    def accepted_order(self, id: UUID) -> Order:
        order = self.order_repo.get_order_by_id(id)
        if order.status != OrderStatus.CREATE:
            raise ValueError

        order.status = OrderStatus.ACCEPTED

        receipt_data = {
            "rec_id": uuid4(),
            "ord_id": id,
            "type": "Test Type",
            "create_date": datetime.now(),
            "rec": "Test Receipt",
            "customer_info": order.customer_info
        }

        asyncio.run(send_to_receipt_queue(receipt_data))

        return self.order_repo.set_status(order)

    def pick_up_order(self, id: UUID) -> Order:
        order = self.order_repo.get_order_by_id(id)
        if order.status != OrderStatus.ACCEPTED:
            raise ValueError

        order.status = OrderStatus.PICK_UP
        return self.order_repo.set_status(order)

    def delivering_order(self, id: UUID) -> Order:
        order = self.order_repo.get_order_by_id(id)
        if order.status != OrderStatus.PICK_UP:
            raise ValueError

        order.status = OrderStatus.DELIVERING
        return self.order_repo.set_status(order)

    def delivered_order(self, id: UUID) -> Order:
        order = self.order_repo.get_order_by_id(id)
        if order.status != OrderStatus.DELIVERING:
            raise ValueError

        order.status = OrderStatus.DELIVERED
        return self.order_repo.set_status(order)

    def paid_order(self, id: UUID) -> Order:
        order = self.order_repo.get_order_by_id(id)
        if order.status != (OrderStatus.DELIVERED or OrderStatus.DELIVERING):
            raise ValueError

        order.status = OrderStatus.PAID
        return self.order_repo.set_status(order)

    def done_order(self, id: UUID) -> Order:
        order = self.order_repo.get_order_by_id(id)
        if order.status != OrderStatus.PAID:
            raise ValueError

        order.status = OrderStatus.DONE
        order.completion_date = datetime.now()
        return self.order_repo.set_status(order)

    def cancel_order(self, id: UUID) -> Order:
        order = self.order_repo.get_order_by_id(id)
        if order.status != (OrderStatus.CREATE or OrderStatus.ACCEPTED):
            raise ValueError

        order.status = OrderStatus.CANCELLED
        return self.order_repo.set_status(order)

    def delete_order(self, id: UUID) -> None:
        order = self.order_repo.get_order_by_id(id)
        if not order:
            raise ValueError(f'Order with id={id} not found')

        return self.order_repo.delete_order_by_id(id)
