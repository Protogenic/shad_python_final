from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy.future import select

from src.configurations import get_async_session
from src.models.sellers import Seller
from src.schemas.seller import IncomingSeller, ReturnedSeller, ReturnedSellerWithBooks
from src.schemas.books import ReturnedBook

sellers_router = APIRouter(tags=["sellers"], prefix="/sellers")

DBSession = Depends(get_async_session)


@sellers_router.post("/", response_model=ReturnedSeller, status_code=status.HTTP_201_CREATED)
async def create_seller(seller: IncomingSeller, session: AsyncSession = DBSession):
    new_seller = Seller(**seller.dict())
    session.add(new_seller)
    await session.flush()
    return new_seller


@sellers_router.get("/", response_model=list[ReturnedSeller])
async def get_all_sellers(session: AsyncSession = DBSession):
    query = select(Seller)
    result = await session.execute(query)
    sellers = result.scalars().all()
    return sellers


@sellers_router.get("/{seller_id}", response_model=ReturnedSellerWithBooks)
async def get_seller(seller_id: int, session: AsyncSession = Depends(get_async_session)):
    print(f"🔍 Looking for seller with ID {seller_id}...")

    query = select(Seller).options(joinedload(Seller.books)).where(Seller.id == seller_id)
    result = await session.execute(query)
    seller = result.scalars().first()

    if not seller:
        print("Seller not found")
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    
    return ReturnedSellerWithBooks(
        id=seller.id,
        first_name=seller.first_name,
        last_name=seller.last_name,
        e_mail=seller.e_mail,
        books=[ReturnedBook(id=b.id, title=b.title, author=b.author, year=b.year, pages=b.pages, seller_id=b.seller_id) for b in seller.books]  # ✅ Преобразование в Pydantic
    )


@sellers_router.put("/{seller_id}", response_model=ReturnedSeller)
async def update_seller(seller_id: int, seller_data: IncomingSeller, session: AsyncSession = DBSession):
    seller = await session.get(Seller, seller_id)
    if seller:
        seller.first_name = seller_data.first_name
        seller.last_name = seller_data.last_name
        seller.e_mail = seller_data.e_mail
        await session.flush()
        return seller

    return Response(status_code=status.HTTP_404_NOT_FOUND)


@sellers_router.delete("/{seller_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_seller(seller_id: int, session: AsyncSession = DBSession):
    seller = await session.get(Seller, seller_id)
    if seller:
        await session.delete(seller)
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    return Response(status_code=status.HTTP_404_NOT_FOUND)
