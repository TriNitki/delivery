from fastapi import APIRouter, Depends, Path, Query, Body
from ..db.elastic import product_autocomplete as product_ac
from ..db.elastic import country_autocomplete as country_ac

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