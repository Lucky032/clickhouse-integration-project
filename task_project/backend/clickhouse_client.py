# backend/clickhouse_client.py
from clickhouse_driver import Client

def get_client(host, port, database, user, jwt_token):
    """
    Establishes a connection to the ClickHouse database.
    """
    client = Client(host=host, port=port, database=database, user=user, password=jwt_token)
    return client
