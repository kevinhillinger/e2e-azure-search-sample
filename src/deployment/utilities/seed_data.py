import os
from gremlin_python.driver import client, serializer
import sys, traceback

# base from https://raw.githubusercontent.com/Azure-Samples/azure-cosmos-db-graph-python-getting-started/master/connect.py

class SeedData(object):
  
  def __init__(self, account_name, account_key, database_name, graph_name):
    self._gremlin_cleanup_graph = "g.V().drop()"

    self._gremlin_insert_vertices = [
        # partition 1
        "g.addV('person').property('id', 'thomas').property('firstName', 'Thomas').property('age', 44).property('partitionKey', 1)",
        "g.addV('person').property('id', 'mary').property('firstName', 'Mary').property('lastName', 'Andersen').property('age', 39).property('partitionKey', 1)",
        "g.addV('person').property('id', 'peter').property('firstName', 'Peter').property('lastName', 'Smith').property('age', 25).property('partitionKey', 1)",
        "g.addV('person').property('id', 'jenny').property('firstName', 'Jenny').property('lastName', 'Curran').property('age', 25).property('partitionKey', 1)",

        #   address
        "g.addV('address').property('id', '8916_marvin_gardens').property('streetName', 'Marvin Gardens Rd').property('streetNumber', 8916).property('city', 'Atlanta').property('partitionKey', 1)",
        "g.addV('address').property('id', '8917_marvin_gardens').property('streetName', 'Marvin Gardens Rd').property('streetNumber', 8917).property('city', 'Atlanta').property('partitionKey', 1)",
        "g.addV('address').property('id', '1611_boardwalk').property('streetName', 'Boardwalk Blvd').property('streetNumber', 1611).property('city', 'New York').property('partitionKey', 1)",

        # partition 2
        "g.addV('person').property('id', 'ben').property('firstName', 'Ben').property('lastName', 'Miller').property('partitionKey', 2)",
        "g.addV('person').property('id', 'robin').property('firstName', 'Robin').property('lastName', 'Wakefield').property('partitionKey', 2)",
        "g.addV('person').property('id', 'forrest').property('firstName', 'Forrest').property('lastName', 'Gump').property('partitionKey', 2)",
        "g.addV('person').property('id', 'john').property('firstName', 'John').property('lastName', 'McClane').property('age', 34).property('partitionKey', 2)",

         #   address
        "g.addV('address').property('id', '926_parkplace').property('streetName', 'Park Place Ave').property('streetNumber', 926).property('city', 'New York').property('partitionKey', 2)",
        "g.addV('address').property('id', '8917_illinois').property('streetName', 'Illinois Ave').property('streetNumber', 8917).property('city', 'Atlanta').property('partitionKey', 2)",
        "g.addV('address').property('id', '4933_baltic').property('streetName', 'Baltic Ave').property('streetNumber', 4933).property('city', 'Vermont').property('partitionKey', 2)",
    ]

    self._gremlin_insert_edges = [
          "g.V('thomas').addE('knows').to(g.V('mary'))",
          "g.V('thomas').addE('knows').to(g.V('ben'))",
          "g.V('jenny').addE('knows').to(g.V('forrest'))",
          "g.V('ben').addE('knows').to(g.V('robin'))",

          "g.V('peter').addE('lives_on').to(g.V('1611_boardwalk'))",
          "g.V('ben').addE('lives_on').to(g.V('926_parkplace'))",
          "g.V('forrest').addE('lives_on').to(g.V('4933_baltic'))"
      ]
    
    self.client = client.Client('wss://' + account_name + '.gremlin.cosmosdb.azure.com:443/','g', 
          username="/dbs/" + database_name + "/colls/" + graph_name, 
          password=account_key,
          message_serializer=serializer.GraphSONSerializersV2d0()
      )

  def cleanup_graph(self):
      print("\tRunning this Gremlin query:\n\t{0}".format(self._gremlin_cleanup_graph))
      callback = self.client.submitAsync(self._gremlin_cleanup_graph)
      if callback.result() is not None:
          print("\tCleaned up the graph!")
      print("\n")

  def insert_vertices(self):
      for query in self._gremlin_insert_vertices:
          print("\tRunning this Gremlin query:\n\t{0}\n".format(query))
          callback = self.client.submitAsync(query)
          if callback.result() is not None:
              print("\tInserted this vertex:\n\t{0}\n".format(callback.result().one()))
          else:
              print("Something went wrong with this query: {0}".format(query))
      print("\n")

  def insert_edges(self):
      for query in self._gremlin_insert_edges:
          print("\tRunning this Gremlin query:\n\t{0}\n".format(query))
          callback = self.client.submitAsync(query)
          if callback.result() is not None:
              print("\tInserted this edge:\n\t{0}\n".format(callback.result().one()))
          else:
              print("Something went wrong with this query:\n\t{0}".format(query))
      print("\n")

  def execute(self):
    try:
        self.cleanup_graph()
        self.insert_vertices()
        self.insert_edges()
    except Exception as e:
        print('There was an exception: {0}'.format(e))
        traceback.print_exc(file=sys.stdout)
        sys.exit(1)