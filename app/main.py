from fastapi import FastAPI
from cassandra.cqlengine.management import sync_table

from .routers import user, review, product
from .db.postgres import models as pg_models
from .db.cassandra import models as ac_models
from .db.database import engine


app = FastAPI()
app.include_router(user.router)
app.include_router(product.router)
app.include_router(review.router)

sync_table(ac_models.DbReview, ['delivery'])
pg_models.Base.metadata.create_all(engine)