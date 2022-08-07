from src import Session
from src.schemas.main import CreateOrder, CreateTransaction
from src.models.main import Order, Transaction, Book


def get_all(db: Session):  # get all order
    orders = db.query(Order).all()
    return orders


def get_transaction_by_id(db: Session, id: int):  # get transaction by id and the items
    transaction = db.query(Transaction).filter(Transaction.id == id).first()
    order = db.query(Order).filter(Order.transaction_id == id).all()
    data: list = []
    for i in order:
        data.append(
            {
                "id": i.id,
                "book_id": i.book_id,
            }
        )
    return {
        "transaction_id": transaction.id,
        "member_id": transaction.member_id,
        "tota;": transaction.total,
        "qty_total": transaction.qty_items,
        "order_at": str(transaction.create_at),
        "order": data,
    }


async def create_new_order(db: Session, order: CreateOrder):  # create new order
    book = db.query(Book).filter(Book.id == order.book_id).first()
    new_order = Order(
        book_id=order.book_id,
        transaction_id=order.transaction_id,
        qty=order.qty,
        total=order.qty * book.price,
        order_at=order.order_at,
    )
    db.add(new_order)
    db.commit()
    return new_order


async def create_new_transaction(db: Session, transaction: CreateTransaction):  # create new transaction
    transaction = Transaction(
        member_id=transaction.member_id,
    )
    db.add(transaction)
    db.commit()
    return transaction


async def update_trasanction(db: Session, id: int):  # update transaction
    transaction = db.query(Transaction).filter(Transaction.id == id).first()
    order = db.query(Order).filter(Order.transaction_id == id).all()
    total: int = 0
    qty: int = 0
    for i in order:
        total += i.total
        qty += i.qty
    transaction.total = total
    transaction.qty_items = qty
    db.merge(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction


async def delete_order_all(db: Session, transaction_id: int):
    trans = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    order = db.query(Order).filter(Order.transaction_id == transaction_id).all()
    db.delete(trans)
    db.delete(order)
    db.commit()
    return {"order": order, "transaction": trans}
