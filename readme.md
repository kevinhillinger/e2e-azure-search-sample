# End to End Azure Search Sample / Demo

This is an e2e demonstration of Azure Search. In a production scenario, you would never expose the Search REST API directly. Instead, you will want to ensure that Azure Search API keys are kept secure on the backend, while using an authorization protocol like OAuth2 for either active or non-interactive HTTP calls to Search.

Additionally, the codebase demonstrates Cosmos DB Graph database as the Data Source for Azure Search. The Graph API is not supported directly, but because Cosmos DB is multi-API, we can easily get around this and use the Document /SQL API.

## Prerequisites

* Python 3.5+
* [Azure CLI 2.0](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest)
* Azure Subscription
* [Azure Service Principal](https://docs.microsoft.com/en-us/cli/azure/create-an-azure-service-principal-azure-cli?view=azure-cli-latest)

## Getting Started

### 1. clone the repository 

```
git clone https://github.com/kevinhillinger/e2e-azure-search-sample.git
```

### 2. Setup Python environment

Next, open a terminal (or powershell) and execute the setup script:

```bash
sudo chmod 775 setup.sh
./setup.sh
```

Powershell: 

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned
./setup.ps1
```
This script will create the Python virtual environment and install the python requirements necessary to kick off the process that will deploy the Azure resources and perform configuration.

### 3. Update settings.yaml
You will need to update the ```settings.yaml``` with your settings. Update it with the target subscription information and the service principal info.

    NOTE: If you don't know or haven't create a service principal yet for Azure, you will find [the instructions here](https://docs.microsoft.com/en-us/cli/azure/create-an-azure-service-principal-azure-cli?view=azure-cli-latest)


# Explanation

## Azure Search


### Data Source Setup


#### Cosmos DB Graph Connection String
Since Azure Search does NOT support the Graph API, you will not be able to use the portal options directly when setting up a data source. Instead, you will need to input the connection string. When getting the connection string from Cosmos DB, you must be sure to remove the ```ApiKind=Gremlin``` parameter from the string. Otherwise, it will not be accepted by Azure Search.


### Example Query

For the queries below, not that since the Graph data structure is written and read slightly different than a usual document in Cosmos DB, it's necessary to JOIN on each property (which in the Graph API has a value and an id), and then select the value as a named field.

```
SELECT 
    c.id,
    c.partitionKey AS accountId,
    c._ts,
    l._value AS lastName,
    f._value AS firstName,
    a._value AS age
FROM c 
JOIN f in c.firstName
JOIN l in c.lastName
JOIN a in c.age
WHERE c.label = 'person' AND c._ts >= @HighWaterMark 
ORDER BY c._ts
```


```
SELECT 
    c.id,
    c.partitionKey AS accountId,
    c._ts,
    n1._value AS streetName,
    n2._value AS streetAddress,
    c2._value AS city
FROM c 
JOIN n1 in c.streetName
JOIN n2 in c.streetNumber
JOIN c2 in c.city
WHERE c.label = 'address' AND c._ts >= @HighWaterMark 
ORDER BY c._ts
```

## Updating Search Document (index updates)

### Azure Functions example

For this sample, Azure Functions is being used to take advantage of the Cosmos DB trigger. Right now, the example is using v1 of Azure Functions.

#### Dependencies

The dependencies you'll need are located in the ```project.json``` file. Be sure to note the extra dependencies as those may be required.

### Resources

* [Updating documents](https://docs.microsoft.com/en-us/rest/api/searchservice/AddUpdate-or-Delete-Documents)
* [Search getting started code samples](https://github.com/Azure-Samples/search-dotnet-getting-started/blob/master/DotNetHowTo/DotNetHowTo/Program.cs)
* [search import data using c#](https://docs.microsoft.com/en-us/azure/search/search-import-data-dotnet)