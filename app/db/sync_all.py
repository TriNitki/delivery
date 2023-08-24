from cassandra.cqlengine.management import sync_table
from ..config import settings

from .postgres import models as pg_models
from .database import engine
from .cassandra import models as ac_models

def sync_models():
    sync_table(ac_models.DbReview, [settings.CASSANDRA_KEYSPACE])
    sync_table(ac_models.DbCart, [settings.CASSANDRA_KEYSPACE])
    sync_table(ac_models.DbOrder, [settings.CASSANDRA_KEYSPACE])
    pg_models.Base.metadata.create_all(engine)