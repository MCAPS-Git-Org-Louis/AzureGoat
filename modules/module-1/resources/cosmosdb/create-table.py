
import json
from optparse import Values
import time
from urllib.parse import urljoin
import uuid
from azure.cosmos import  CosmosClient, PartitionKey




import os

# Initialize the Cosmos client
host = os.environ.get('COSMOS_ENDPOINT', '')
key = os.environ.get('COSMOS_KEY', '')

# <create_cosmos_client>
url = str(host)
primarykey = str(key)
print(url)
print(primarykey)
client = CosmosClient(url, primarykey)
# </create_cosmos_client>

# Create a database
# <create_database_if_not_exists>
database_name = 'ine-cosmos-sql-db'
database = client.create_database_if_not_exists(id=database_name)
# </create_database_if_not_exists>

# Create a container
# Using a good partition key improves the performance of database operations.
# <create_container_if_not_exists>
container_name = 'blog-users'
container = database.create_container_if_not_exists(
    id=container_name, 
    partition_key=PartitionKey(path="/id")
)


db_file_json_1 = open('./modules/module-1/resources/cosmosdb/blog-users.json')
db_file_1 = json.loads(db_file_json_1.read())
for db_item_1 in db_file_1:
   container.upsert_item(body=db_item_1)

container_name = 'blog-posts'
container = database.create_container_if_not_exists(
    id=container_name, 
    partition_key=PartitionKey(path="/id")
)

db_file_json_2 = open('./modules/module-1/resources/cosmosdb/blog-posts.json')
db_file_2 = json.loads(db_file_json_2.read())
for db_item_2 in db_file_2:
   container.upsert_item(body=db_item_2)

print("Items Updated")
