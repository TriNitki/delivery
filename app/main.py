from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from .routers import autocomplete, review, product, user, warehouse, favorite, order, cart
from .db import sync_all

app = FastAPI()

app.include_router(user.router)
app.include_router(autocomplete.router)
app.include_router(order.router)
app.include_router(cart.router)
app.include_router(favorite.router)
app.include_router(product.router)
app.include_router(review.router)
app.include_router(warehouse.router)

@app.get('/', include_in_schema=False)
async def docs_redirect():
    return RedirectResponse('/docs')

sync_all.sync_models()