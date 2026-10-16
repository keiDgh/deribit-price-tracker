from fastapi import APIRouter, Query, HTTPException, status

from datetime import datetime

from app.infra.api.schemas import PriceSchema
from app.infra.api.dependencies import PriceServiceDep, CurrencyServiceDep

from app.domain.exceptions import CurrencyNotFoundError

router = APIRouter()

@router.get(
        "", 
        response_model=list[PriceSchema], 
        summary="Get ticker's prices"
)
async def get_prices(
    price_service: PriceServiceDep, 
    currency_service: CurrencyServiceDep, 
    ticker: str = Query(default="btc_usd"), 
    skip: int = Query(default=0, ge=0), 
    limit: int = Query(default=10, ge=20, le=200)
):
    try:
        currency = await currency_service.get_by_ticker(ticker)
    except CurrencyNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=str(e)
        )
    
    prices = await price_service.get_by_ticker(ticker=ticker, skip=skip, limit=limit)

    return [
        PriceSchema(
            id=price.id, 
            ticker=currency.ticker, 
            name=currency.name, 
            price=price.price, 
            timestamp=price.timestamp
        )
        for price in prices
    ]

@router.get(
        "/latest", 
        response_model=PriceSchema
)
async def get_prices(
    price_service: PriceServiceDep, 
    currency_service: CurrencyServiceDep, 
    ticker: str = Query(default="btc_usd"), 
):
    try:
        currency = await currency_service.get_by_ticker(ticker)
    except CurrencyNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=str(e)
        )
    
    price = await price_service.get_last(ticker)

    if price is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Prices info is not found or not set yet"
        )

    return PriceSchema(
        id=price.id, 
        ticker=currency.ticker, 
        name=currency.name, 
        price=price.price, 
        timestamp=price.timestamp
    )
    

@router.get(
        "/history", 
        response_model=list[PriceSchema]
)
async def get_prices(
    price_service: PriceServiceDep, 
    currency_service: CurrencyServiceDep, 
    ticker: str = Query(default="btc_usd"), 
    skip: int = Query(default=0, ge=0), 
    limit: int = Query(default=10, ge=20, le=200), 
    start: datetime = Query(), 
    end: datetime = Query()
):
    try:
        currency = await currency_service.get_by_ticker(ticker)
    except CurrencyNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=str(e)
        )
    prices = await price_service.get_by_ticker_and_period(
        ticker=ticker, 
        start=start,
        end=end, 
        skip=skip, 
        limit=limit
    )

    return [
        PriceSchema(
            id=price.id, 
            ticker=currency.ticker, 
            name=currency.name, 
            price=price.price, 
            timestamp=price.timestamp
        )
        for price in prices
    ]