from fastapi import APIRouter, Query, HTTPException, status

from datetime import datetime

from app.infra.api.schemas import CurrencySchema
from app.infra.api.dependencies import CurrencyServiceDep

from app.domain.exceptions import CurrencyNotFoundError

router = APIRouter()

@router.get(
        "", 
        response_model=list[CurrencySchema]
)
async def get_currencies(
    currency_service: CurrencyServiceDep
):
    currencies = await currency_service.get_all()
    return currencies