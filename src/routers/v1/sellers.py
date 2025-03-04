from fastapi import APIRouter, Depends, Response, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.configurations import get_async_session
from src.models.sellers import Seller
from src.schemas.seller import IncomingSeller, ReturnedSeller, ReturnedSellerWithBooks

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
async def get_seller(seller_id: int, session: AsyncSession = DBSession):
    seller = await session.get(Seller, seller_id)
    if seller:
        return seller

    return Response(status_code=status.HTTP_404_NOT_FOUND)


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
