#Retrieve genres

import http.client

conn = http.client.HTTPSConnection("api.themoviedb.org")

payload = "{}"

conn.request("GET", "/3/genre/movie/list?language=en-US&api_key=05df6955e82bd36ed52418517ea60b7b", payload)

res = conn.getresponse()
data = res.read()

print(data)