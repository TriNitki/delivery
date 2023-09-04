from fastapi import APIRouter, Depends, Path, Query, Body
from ..db.elastic import product_autocomplete as product_ac

router = APIRouter(
    prefix='/search-for',
    tags=['search']
)

@router.get('/')
async def product_autocomplete(
    text: str = Query(...)
):
    return product_ac.autocomplete(text)