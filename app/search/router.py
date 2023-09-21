from fastapi import APIRouter, Query
from . import product_autocomplete as product_ac
from . import country_autocomplete as country_ac
from . import city_autocomplete as city_ac

router = APIRouter(
    prefix='/autocomplete',
    tags=['autocomplete']
)

@router.get('/product')
async def product_autocomplete(
    text: str = Query(...)
):
    return product_ac.autocomplete(text)

@router.get('/country')
async def country_autocomplete(
    text: str = Query(...)
):
    return country_ac.autocomplete(text)

@router.get('/city')
async def city_autocomplete(
    text: str = Query(...)
):
    return city_ac.autocomplete(text)