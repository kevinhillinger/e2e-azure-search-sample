
-- Query for data source for person indexer

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

-- Query for data source for address indexer

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
