Online Movie Ticket Booking

An online Movie Ticket Booking System, where a User can select a city, then a movie of their choice, and be able to find theaters playing the movie
and book one or more seats in that theater using this system. Price of all the seats are same.

Assumptions made - 

1. All the theatres have only a single screen, multiple screens per theatre is not considered.
2. While booking seats, though an entry for user is made in the booking table, but the user is hardcoded.


APIs - 

1. /showAllCities - Gives a list of all the cities in the DB
2. /showAllTheatres - Gives a list of all the cities in the DB
3. /showAllMovies - Gives a list of all the movies in the city
4. /showTheatres - Takes movie and city as input parameters and outputs theatres in the particular city showing the movie
5. /showMovies - Takes city as input parameter and outputs movies showing in the particular city
6. /bookSeats - Takes city, movie, theatre and no of seats as input, creates a booking for the user and returns booking id


Simplified System Architecture - 

![MovieBooking_architecture](https://user-images.githubusercontent.com/10531214/120625380-41dfaa80-c47f-11eb-9b07-c330108158b3.png)
