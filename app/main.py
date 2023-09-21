from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from cassandra.cqlengine.management import sync_table

from .product import router as product
from .review import router as review
from .warehouse import router as warehouse
from .user import router as user
from .favorite import router as favorite
from .cart import router as cart
from .search import router as search
from .order import router as order

from .config import settings
from .database import engine
from . import models as pg_models
from . import models_cas as ac_models

app = FastAPI()

app.include_router(product.router)
app.include_router(review.router)
app.include_router(warehouse.router)
app.include_router(user.router)
app.include_router(favorite.router)
app.include_router(cart.router)
app.include_router(search.router)
app.include_router(order.router)

@app.get('/', include_in_schema=False)
async def docs_redirect():
    return RedirectResponse('/docs')

sync_table(ac_models.DbOrder, [settings.CASSANDRA_KEYSPACE])
pg_models.Base.metadata.create_all(engine)