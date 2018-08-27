#r "Microsoft.Azure.Documents.Client"
#r "Newtonsoft.Json"
using System;
using System.Net;
using Microsoft.Azure.Search;
using Microsoft.Azure.Search.Models;
using Microsoft.Azure.Documents;
using Newtonsoft.Json.Linq;
using Document = Microsoft.Azure.Documents.Document;

// https://docs.microsoft.com/en-us/rest/api/searchservice/AddUpdate-or-Delete-Documents
// https://github.com/Azure-Samples/search-dotnet-getting-started/blob/master/DotNetHowTo/DotNetHowTo/Program.cs
// https://docs.microsoft.com/en-us/azure/search/search-import-data-dotnet
 
public class Person {
  public string id { get; set;}
  public int age {get;set;}
}

public class Address {
  public string id { get; set;}
  public int streetAddress {get;set;}
}

public static void Run(IReadOnlyList<Document> documents, TraceWriter log)
{
    if (documents != null && documents.Count > 0)
    {
        log.Verbose("Documents modified " + documents.Count);
        log.Verbose("First document Id " + documents[0].Id);

        var indexClient = CreateSearchIndexClient("person");

        var batch = GetBatch<Person>(documents, (d) => GetIndexDocument<Person>(d), "person");
        CreateSearchIndexClient("person").Documents.Index(batch);

        // var batch = GetBatch<Address>(documents, (d) => GetIndexDocument<Address>(d), "address");
        // CreateSearchIndexClient("address").Documents.Index(batch);
    }
}

public static IndexBatch<T> GetBatch<T>(IReadOnlyList<Document> documents, Func<Document, T> getIndexDocument, string label) where T : class, new()
{
    var actions = new List<IndexAction<T>>();

    foreach (var doc in documents.Where(d => d.GetPropertyValue<string>("label").Equals(label)))
    {
        var indexDocument = getIndexDocument(doc);

        actions.Add(IndexAction.MergeOrUpload(indexDocument as T));
    }
    return IndexBatch.New<T>(actions.ToArray());
}

public static T GetIndexDocument<T>(Document doc) where T : class, new()
{
    if (typeof(T) == typeof(Person)) {
        return new Person() {
            id = doc.Id,
            age = GetVertexPropertyValue<int>(doc, "age")
        } as T;
    }
    else if (typeof(T) == typeof(Address)) {
        return new Address() {
            id = doc.Id,
            streetAddress = GetVertexPropertyValue<int>(doc, "streetAddress")
        } as T;
    }
    return default(T);
}

public static T GetVertexPropertyValue<T>(Document document, string propertyName) 
{
    return document.GetPropertyValue<JArray>(propertyName).First["_value"].Value<T>();
}

public static SearchIndexClient CreateSearchIndexClient(string indexName)
{
    string searchServiceName = GetEnvironmentVariable("AzureSearchServiceName");
    string queryApiKey = GetEnvironmentVariable("AzureSearchApiKey");

    SearchIndexClient indexClient = new SearchIndexClient(searchServiceName, indexName, new SearchCredentials(queryApiKey));
    return indexClient;
}

public static string GetEnvironmentVariable(string name)
{
    return System.Environment.GetEnvironmentVariable(name, EnvironmentVariableTarget.Process);
}