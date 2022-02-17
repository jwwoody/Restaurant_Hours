# Restaurant_Hours
Created By Jeffrey Woodbury
February 2022

This script is written to find compatible hours for a person to eat at a given list of restaurants
User will input day/time info via stdin input

Required: json file (currently grabbing data from rest_hours.json)

This program assumes that the beginning of the week for restaurant hours is marked as Monday, and the end of the week is marked by Sunday.
For example, if a restaurant is open every day of the week, then that is indicated by writing "Mon-Sun HH:MM - HH:MM". 

Lastly, this assumes that nobody wants to be looking for a restaraunt that is open after 6am. At that point, it's the next day. 
For example, if you're looking for a place open Saturday night at 12:30am (technically Sunday), both the restaurant and you will consider that as Saturday still. 
