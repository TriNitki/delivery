from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from cassandra.cqlengine.management import sync_table

from .routers import user, review, product, warehouse, favorite, order, cart, auth
from .db.postgres import models as pg_models
from .db.cassandra import models as ac_models
from .db.database import engine
from .config import settings


app = FastAPI()
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(order.router)
app.include_router(cart.router)
app.include_router(favorite.router)
app.include_router(product.router)
app.include_router(review.router)
app.include_router(warehouse.router)

@app.get('/', include_in_schema=False)
async def docs_redirect():
    return RedirectResponse('/docs')

sync_table(ac_models.DbReview, [settings.CASSANDRA_KEYSPACE])
sync_table(ac_models.DbFavorite, [settings.CASSANDRA_KEYSPACE])
sync_table(ac_models.DbCart, [settings.CASSANDRA_KEYSPACE])
sync_table(ac_models.DbOrder, [settings.CASSANDRA_KEYSPACE])
pg_models.Base.metadata.create_all(engine)