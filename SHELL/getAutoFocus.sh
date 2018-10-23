#!/bin/bash
# Get JSON
curl -X POST https://autofocus.paloaltonetworks.com/api/v1.0/samples/search/ \
-H "Content-Type: application/json" \
-d '{
  "apiKey": "7957eec6-0485-4176-8046-f54b9eb3c8ae",
  "query": {
    "operator": "all",
    "children": [
      {
        "field": "sample.malware",
        "operator": "is",
        "value": 1
      }
    ]
  },
  "size": 50,
  "from": 0,
  "sort": {
    "create_date": {
      "order": "desc"
    }
  },
  "scope": "public"
}' > XML/test.json
cookie=$(cat XML/test.json | grep -Po '"[^"]{40}"' | sed -e 's/"//g')
# Get results
curl -X POST "https://autofocus.paloaltonetworks.com/api/v1.0/samples/results/$cookie" \
-H "Content-Type: application/json" \
-d '{
   "apiKey": "7957eec6-0485-4176-8046-f54b9eb3c8ae"
}' > XML/result.json
