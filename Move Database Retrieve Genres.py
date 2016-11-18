#------------------------API Key

https://api.themoviedb.org/3/movie/550?api_key= #Example of api request

#--------- retrieve Movie Genres----
#This will return an array of all movie genres with specific ID assigned to each genre.
#Horror ID:27, Romance ID: 10749, Action: 28

import http.client

conn = http.client.HTTPSConnection("api.themoviedb.org")

payload = "{}"

headers = { 'content-type': "application/json" }

conn.request("GET", "/3/genre/movie/list?language=en-US&api_key=", payload, headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))

#End


#-----------retrieve Popular Horror Movies
#Returns a list in a form of an array of Popular horror movies in descending order.
import http.client

conn = http.client.HTTPSConnection("api.themoviedb.org")

payload = "{}"

conn.request("GET", "/3/discover/movie?with_genres=27&page=1&include_video=true&include_adult=false&certification_country=US&sort_by=popularity.desc&language=en-US&api_key=05df6955e82bd36ed52418517ea60b7b", payload)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))

#End

#---------------Retrieve Popular Romance Movies
#Returns a list in a form of an array of Popular romance movies in descending order.
import http.client

conn = http.client.HTTPSConnection("api.themoviedb.org")

payload = "{}"

conn.request("GET", "/3/discover/movie?with_genres=10749&page=1&include_video=true&include_adult=false&certification_country=US&sort_by=popularity.desc&language=en-US&api_key=05df6955e82bd36ed52418517ea60b7b", payload)

res = conn.getresponse()
data = res.read()


print(data.decode("utf-8"))
#END


#--------------Retrieve Popular Action Movies
#Returns a list in a form of an array of Popular action movies in descending order.
import http.client

conn = http.client.HTTPSConnection("api.themoviedb.org")

payload = "{}"

conn.request("GET", "/3/discover/movie?with_genres=28&page=1&include_video=true&include_adult=false&certification_country=US&sort_by=popularity.desc&language=en-US&api_key=05df6955e82bd36ed52418517ea60b7b", payload)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))

#END
