from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model

from ...db.database import get_ac_db

    
class DbReview(Model):
    __table_name__: str = 'reviews'
    __keyspace__: str = 'delivery'
    session = get_ac_db()
    session.default_fetch_size = 1000
    
    product_id = columns.Text(primary_key=True)
    user_id = columns.UUID(primary_key=True, clustering_order='desc')
    description = columns.Text()
    publication_datetime = columns.DateTime()
    rating = columns.SmallInt()

class DbCart(Model):
    __table_name__: str = 'carts'
    __keyspace__: str = 'delivery'
    session = get_ac_db()
    session.default_fetch_size = 1000
    
    user_id = columns.UUID(primary_key=True)
    product_id = columns.Text(primary_key=True, clustering_order='asc')
    quantity = columns.Integer()
    addition_datetime = columns.DateTime()

class DbOrder(Model):
    __table_name__: str = 'orders'
    __keyspace__: str = 'delivery'
    session = get_ac_db()
    session.default_fetch_size = 1000
    
    user_id = columns.UUID(primary_key=True)
    creation_datetime = columns.DateTime(primary_key=True, clustering_order='desc')
    delivery_datetime = columns.DateTime()
    estimated_delivery_time = columns.Integer() # in days
    delivery_address = columns.Text()
    quantity = columns.Integer()
    is_cancelled = columns.Boolean(default=False)
    
    product_id = columns.Text(primary_key=True, clustering_order='asc')
    product_name = columns.Text()
    product_price = columns.Decimal()
    product_weight = columns.Integer()
    product_manufacturer_country = columns.Text()
    product_category_name = columns.Text()
    product_brand = columns.Text()
    product_discount = columns.SmallInt()
    product_description = columns.Text()
    product_image = columns.Text()
    product_is_active = columns.Boolean()
    product_seller_id = columns.UUID()
    
    
    