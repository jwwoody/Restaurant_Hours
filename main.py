"""
Created By Jeffrey Woodbury
February 2022

This script is written to find compatible hours for a person to eat at a given list of restaurants
User will input day/time info via stdin input

Required: json file (currently grabbing data from rest_hours.json)
"""

import json
from restaurant import Restaurant
import re

DAYS_OF_WEEK = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
EARLIEST_MORNING_HOUR = 6 #For example, no restaraunt can have an opening hour before 6am

def get_day_pick():
    """Returns the day pick (first 3 letters, lowercase)

    :return: string for day selection
    :rtype: string
    """

    desired_day = ""
    while desired_day == "": #Check valid input for day input
        desired_day = input('What day do you want to eat? (Mon, Tue, Wed, Thu, Fri, Sat, Sun)--->').strip().lower()
        if desired_day in DAYS_OF_WEEK:
            break
        
        else:
            if desired_day[:3] in DAYS_OF_WEEK:
                correct = input(f'Did you mean {desired_day[:3]}? (y or n)').strip().lower()
                if correct == "y":
                    desired_day = desired_day[:3]
                else:
                    desired_day = ""
                    print('Try again')
                    continue
            else:
                print('Invalid Input: Must enter a day of the week')
                desired_day = "" #Need to try again
    return desired_day

def get_time_pick():
    """Returns the time pick (HH:MM)

    :return: string for time pick
    :rtype: string
    """

    desired_time = ""
    while desired_time == "": #Check valid input for time input
        desired_time = input('When do you want to eat? (HH:MM)').strip().lower()
    
        if ':' in desired_time: #We have minutes info
            colon_index = desired_time.find(':')
            hour_time = desired_time[:colon_index]
            minutes_time = desired_time[colon_index+1:]
            if len(minutes_time) > 2 or len(hour_time) > 2:
                print('Invalid Input: Must enter time between 1 an 12:59')
                desired_time = ""
                continue
            try:
                hour_test = int(hour_time)
                min_test = int(minutes_time)
            except ValueError:
                print('Invalid Input: Must enter time between 1 an 12:59')
                desired_time = ""
                continue
            if  1<= hour_test <= 12: #Good!
                pass
            else:
                print('Invalid Input: Must enter time between 1 an 12:59')
                desired_time = ""
                continue
            if  0<= min_test <= 59: #Good!
                pass
            else:
                print('Invalid Input: Must enter time between 1 an 12:59')
                desired_time = ""
                continue

            break
        else: #On the whole hour
            try:
                value = int(desired_time)
            except ValueError:
                print('Invalid Input: Must enter hour between 1 an 12:59')
                desired_time = ""
                continue
            if 1 <= value <= 12:
                break
            else:
                print('Invalid Input: Must enter hour between 1 an 12:59')
                desired_time = ""
                continue
    return desired_time

def get_meridian_pick():
    """Returns the meridian pick (am or pm)

    :return: string with am or pm 
    :rtype: string
    """

    am_or_pm = ""
    while am_or_pm == "": #Check valid input for am or pm input
        am_or_pm = input('AM or PM?').strip().lower()
        if am_or_pm == "am" or am_or_pm == "pm":
            break
        
        else:
            print('Invalid Input: Must enter AM or PM')
            am_or_pm = ""
    return am_or_pm
    
def get_days(start, end):
    """Returns the days between start and end days, inclusive.

    :param start: a string
    :type string: string for start day of interval

    :param end: another numeric value
    :type string: string for end day of interval

    :return: comma separated string with days between start and end, inclusive 
    :rtype: string
    """

    
    start_index = DAYS_OF_WEEK.index(start)
    end_index = DAYS_OF_WEEK.index(end)+1
    output_list =  DAYS_OF_WEEK[start_index:end_index]
    output_string = ",".join(output_list)
    return output_string

def split_day_and_hours(block):
    """Returns the day information and hour information in a given string
    Assume that the hourly info starts with the first digit in the block

    :param block: a string with both day and hour info ex: "Mon-Sun 11 am - 10 pm"
    :type string

    :return: the day information and the hour information, separated
    :rtype: string, string
    """

    block = block.replace(" ", "").lower()
    first_digit = re.search(r"\d", block).start() #find first digit index
    return block[:first_digit], block[first_digit:]

def get_time_value(hour_in, meridian_in, start_or_end):
    """Returns the military time value of an hour and either AM or PM (however, with hours after midnight, we'll consider 5:59am as the end of the night)

    :param hour_in: a string representing the hour and minutes ex: "11" or "11:30"
    :type string

    :param neridian_in: a string representing am or pm
    :type string

    :param start_or_end: either 0 for start or 1 for end (used for after midnight issues)
    :type int

    :return: the military time value ex: number between 0 and 24
    :rtype: double
    """

    time_value = 0
    hour_time = 0
    minutes_time = 0

    if ':' in hour_in: #Are there minutes attached to the hour
        colon_index = hour_in.find(':')
        hour_time = hour_in[:colon_index]
        minutes_time = hour_in[colon_index+1:]

        time_value += int(hour_time)
        time_value += int(minutes_time)/60
    else: #No minutes attached, full hour
        hour_time = int(hour_in)
        time_value += int(hour_in)
    
    if meridian_in == "pm":
        if hour_time != "12": #If the input time is 12:30pm then we don't want to add 12 to the time_value
            time_value +=12
    else:
        if time_value < EARLIEST_MORNING_HOUR and start_or_end == 1: #We're at the end and in the am, after midnight, ie our time_value can be > than 24
            time_value += 24
        elif hour_time == "12": #If it's 12:30 am, then the value we'll use is 24.5
            time_value +=12

    return time_value


"""Start of main code block
 - Read in JSON file
 - Get input from user via stdin
 - Loop through data checking for restaurants that are open during desired time
 - Output restaurants that match!
"""

# Opening JSON file
f = open('rest_hours.json')
 
# returns JSON object as a dictionary
data = json.load(f)
 
done = False 

#Main loop to check hours multiple times
while not done:
    
    #Get our desired day
    desired_day = get_day_pick() 

    #Get our desired time
    desired_time = get_time_pick() 

    #Get our desired am or pm
    am_or_pm = get_meridian_pick() 


    detailed_pick = desired_day + ' at '+ desired_time+ ' '+ am_or_pm
    print('\nYou picked:', detailed_pick.upper())

    converted_pick = get_time_value(desired_time, am_or_pm, 1) #Convert the desired day/time to military value

    answers = []
    for listing in data:
        rest = Restaurant(listing["name"], listing['times']) #Create a Restaurant Object for Data control

        for block in rest.times: #Loop through the restaurant times by block
            
            # Split the block by day info and hour info
            day_info, hour_info = split_day_and_hours(block)

            while '-' in day_info: #Need to split hour from minutes
                dash_index = day_info.find('-')
                start_day = day_info[dash_index-3:dash_index]
                end_day = day_info[dash_index+1:dash_index+4]
                day_info = day_info.replace(day_info[dash_index-3:dash_index+4], get_days(start_day, end_day))
            
            if desired_day not in day_info:
                continue #Go to next TimeBlock, our desired day/time is not found in this block
            
            if '-' in hour_info:
                dash_index = hour_info.find('-')
                start_hour = hour_info[0:dash_index-2]
                start_meridian = hour_info[dash_index-2:dash_index]
                end_hour = hour_info[dash_index+1:-2]
                end_meridian = hour_info[-2:]

            
                start_hour_value = get_time_value(start_hour, start_meridian, 0)
                end_hour_value = get_time_value(end_hour, end_meridian, 1)

                # Check to see if the desired day/time fits with the current restaurant hours
                if converted_pick >= start_hour_value and converted_pick < end_hour_value:
                    answers.append((rest.name, block))
                    break #We found an answer with the restaurant, so no need to keep checking times

            else: #Something wrong with file time info
                print('Invalid time for: ', rest.name, ' at ', block)


    if not answers : #Empty Answers
        print('Oh No!, there are no restaurants open at:', detailed_pick.upper())
    else:
        print(f'There are {len(answers)} restaraunts open for {detailed_pick.upper()}:\n')
        print(*answers, sep='\n') #Print open restaurants on separate lines

    play_again = input('\nDo you want to check another time? (y or n)').strip().lower()
    if play_again != "y": #User doesn't want to play anymore :(
        print('Thanks for checking hours! Enjoy your meal!')
        done = True 
        break
    print()

# Closing file
f.close()