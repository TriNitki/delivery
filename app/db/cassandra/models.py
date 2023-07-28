from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model

from ...db.database import get_ac_db

class DbReview(Model):
    __table_name__: str = 'reviews'
    __keyspace__: str = 'delivery'
    session = get_ac_db()
    session.default_fetch_size = 1000
    
    product_number = columns.Integer(primary_key=True)
    user_id = columns.UUID()
    description = columns.Text()
    publication_datetime = columns.DateTime()
    rating = columns.SmallInt()
    
    