from src import APIRouter, Depends, JSONResponse, HTTPException, status, get_db, List
from src.schemas.main import CreateOrder, CreateTransaction
from src.handler.order import *

route = APIRouter(prefix="/order", tags=["order"])  # define order router


@route.get("/")  # get all orders
def get_all_orders(db: Session = Depends(get_db)):
    order = get_all(db)
    data: list = []
    for i in order:
        data.append(
            {
                "id": i.id,
                "transaction_id": i.transaction_id,
                "book_id": i.book_id,
                "qty": i.qty,
                "total": i.total,
            }
        )
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "get all orders", "data": data})


@route.get("/{id}")
def get_transaction(id: int, db: Session = Depends(get_db)):  # get transaction by id
    transaction = get_transaction_by_id(db, id)
    if transaction is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="transaction not found")
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "get transaction", "data": transaction})


@route.post("/")  # create new order
async def create_transaction(order: List[CreateOrder], trans: CreateTransaction, db: Session = Depends(get_db)):
    try:
        transaction = await create_new_transaction(db, trans)
        for x in order:
            x.transaction_id = transaction.id
            await create_new_order(db, x)

        await update_trasanction(db, transaction.id)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "create new order"})
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="create new order failed")
