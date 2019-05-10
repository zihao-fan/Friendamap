A location based web application using Yelp API and MapQuest API. It encompasses the following features:

- Users can search for a nearby place (eg. restaurant) that is similar to a specific place of
their choosing. For example, if users are visiting a new city, they can provide the name
of their favorite restaurant in their hometown and the app will suggest a similar
restaurant in the city they are currently visiting. To implement this feature, we
connect to MapQuest API to collect the longitude and latitude of the place provided by users and their current location,
search for nearby places using Yelp API, and return 5 places that is most similar to the place provided by user (sorted from most similar to least similar). 

- Users can find out who else using this app favors a place. To
implement this feature, we stored the favorite places provided by each user in a MySQL database. We implemented a POST request to store new favorite place for a user id, and a GET request to retrieve user ids that liked a place using the place name and address. 

- Users can get a list of users who have visited a place. To implement
this feature, each user account is able to indicate whether the user has visited the place through a POST request. We store this information in MySQL database. A GET request with place name and address can retrieve the users who have visited a place with place name and address. 

