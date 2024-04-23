from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException

from app.services.receipt_service import ReceiptService

from app.models.receipt import Receipt, CreateReceiptRequest

receipt_router = APIRouter(prefix='/receipt', tags=['Receipt'])


@receipt_router.get('/')
def get_receipt(receipt_service: ReceiptService = Depends(ReceiptService)) -> list[Receipt]:
    return receipt_service.get_receipt()


@receipt_router.post('/')
def add_order(
        receipt_info: CreateReceiptRequest,
        order_service: ReceiptService = Depends(ReceiptService)
) -> Receipt:
    try:
        receipt = order_service.create_receipt(receipt_info.ord_id, receipt_info.type, receipt_info.rec,
                                                 receipt_info.customer_info)
        return receipt.dict()
    except KeyError:
        raise HTTPException(400, f'Order with id={receipt_info.rec_id} already exists')


@receipt_router.post('/{id}/delete')
def delete_order(id: UUID, receipt_service: ReceiptService = Depends(ReceiptService)) -> Receipt:
    try:
        receipt = receipt_service.delete_receipt(id)
        return receipt.dict()
    except KeyError:
        raise HTTPException(404, f'Receipt with id={id} not found')
