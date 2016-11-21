#Retrieve genres

import http.client
import tmdbsimple as tmdb
from pprint import pprint

horror_id=27
romance_id=10749
action_id=28

tmdb.API_KEY = '05df6955e82bd36ed52418517ea60b7b'

genre_id=10749 #Romance
genre= tmdb.Genres(genre_id)

movies_in_genre=genre.movies()

print("-------These are list attributes---------")
for i in movies_in_genre:
	print(i)
print("-------End Attributes---------")	


counter=1
for i in movies_in_genre["results"]:
	print(counter,".","Title: {}".format(i["original_title"]))
	print("Release date: {}".format(i["release_date"]))
	print("Description: {}\n".format(i["overview"]))
	counter+=1
