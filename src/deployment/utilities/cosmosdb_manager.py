import os
import pydocumentdb.document_client as document_client
import sys, traceback
from azure.mgmt.cosmosdb import CosmosDB
from azure.common.credentials import ServicePrincipalCredentials

from .seed_data import SeedData

# documentation for pydocument https://github.com/Azure/azure-documentdb-python/blob/master/samples/DatabaseManagement/Program.py
# more samples: https://docs.microsoft.com/en-us/azure/cosmos-db/sql-api-python-samples

class CosmosDbManager(object):

    def __init__(self, settings):
        self.subscription_id = settings.account.subscriptionId
        self.resource_group = settings.resourceGroup.name
        self.account_name = settings.resources.cosmosdb.name
        self.database_name = settings.resources.cosmosdb.database.name
        self.graph_name = settings.resources.cosmosdb.database.graph.name
        self.graph_partition_key = settings.resources.cosmosdb.database.graph.partitionKey

        self.credentials = ServicePrincipalCredentials(
            client_id = settings.account.client.id,
            secret = settings.account.client.secret,
            tenant = settings.account.tenantId
        )
        self.manager = CosmosDB(self.credentials, self.subscription_id)
        self.client = None
    
    def create_database(self):
        client = self.__get_client()

        databases = list(self.client.ReadDatabases())
        exists = len(list(filter(lambda db: db['id'] == self.database_name, databases))) == 1

        if (not exists):
            client.CreateDatabase({ 'id': self.database_name })
    
    def create_graph(self):
        client = self.__get_client()
        
        host = self.get_host()
        master_key = self.get_master_key()

        database_link = 'dbs/' + self.database_name
        coll = { "id": self.graph_name, "partitionKey": {  "paths": [self.graph_partition_key] } }

        self.client.CreateCollection(database_link, coll)

    def seed_data_into_graph(self):
        seed_data = SeedData(
            account_name = self.account_name,
            account_key = self.__get_master_key(),
            database_name = self.database_name,
            graph_name = self.graph_name
        )
        seed_data.execute()

    def __get_client(self):
        if self.client is None:
            master_key = self.__get_master_key()
            host = self.__get_host()
            self.client = document_client.DocumentClient(host, { 'masterKey': master_key })
        return self.client

    def __get_master_key(self):
        results = self.manager.database_accounts.list_keys(self.resource_group, self.account_name)
        return results.primary_master_key

    def __get_host(self):
        account = self.manager.database_accounts.get(self.resource_group, self.account_name)
        return account.document_endpoint
