import json
from restaurant import Restaurant
import re
 
def time_to_value(_day, _time, _ampm):
    # days_to_value = {'mon': 0, 'tue': 24, 'wed': 48, 'thu': 72, 'fri': 96, 'sat': 120, 'sun': 144}
    # val = days_to_value[_day]
    val = 0
    hour, min = _time.split(':')
    val += int(hour)
    val += int(min)/60

    if _ampm == 'pm':
        if int(hour) != 12:
            val += 12
    return val

def get_days(start, end):
    days_of_week = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
    start_index = days_of_week.index(start)
    end_index = days_of_week.index(end)+1
    output_list =  days_of_week[start_index:end_index]
    output_string = ",".join(output_list)
    return output_string

def split_day_and_hours(block):
    block = block.replace(" ", "").lower()
    first_digit = re.search(r"\d", block).start()
    return block[:first_digit], block[first_digit:]

def get_time_value(hour_in, meridian_in):
    time_value = 0
    hour_time = 0
    minutes_time = 0
    if ':' in hour_in:
        colon_index = hour_in.find(':')
        hour_time = hour_in[:colon_index]
        minutes_time = hour_in[colon_index+1:]

        time_value += int(hour_time)
        time_value += int(minutes_time)/60
    else:
        hour_time = int(hour_in)
        time_value += int(hour_in)
    
    if meridian_in == "pm":
        if hour_time != 12:
            time_value +=12
    else:
        if hour_time == "12":
            time_value -=12

    return time_value

# Opening JSON file
f = open('rest_hours.json')
# f = open('test_file.json')
 
# returns JSON object as
# a dictionary
data = json.load(f)
 
# Iterating through the json
# list
# desired_day = input('What day do you want to eat? (Mon, Tue, Wed, Thu, Fri, Sat, Sun)--->').strip()
desired_day = "Sat"
desired_day = desired_day.lower()

# desired_time = input('When do you want to eat? (HH:MM)')
desired_time = '3'

# am_or_pm = input('AM or PM?')
am_or_pm = 'AM'
am_or_pm = am_or_pm.lower()

detailed_pick = desired_day + ' at '+ desired_time+ ' '+ am_or_pm
print('you picked: ', detailed_pick)

# converted_pick = time_to_value(desired_day, desired_time, am_or_pm)
converted_pick = get_time_value(desired_time, am_or_pm)
print(converted_pick)


places = []
answers = []
for listing in data:
    rest = Restaurant()
    rest.name = listing["name"]
    rest.times = listing['times']
    conver_times = []
    for block in rest.times:
        
        # Split the block by day info and hour info
        day_info, hour_info = split_day_and_hours(block)

        while '-' in day_info:
            dash_index = day_info.find('-')
            start_day = day_info[dash_index-3:dash_index]
            end_day = day_info[dash_index+1:dash_index+4]
            day_info = day_info.replace(day_info[dash_index-3:dash_index+4], get_days(start_day, end_day))
        
        if desired_day not in day_info:
            pass #Go to next TimeBlock
        
        if '-' in hour_info:
            dash_index = hour_info.find('-')
            start_hour = hour_info[0:dash_index-2]
            start_meridian = hour_info[dash_index-2:dash_index]
            end_hour = hour_info[dash_index+1:-2]
            end_meridian = hour_info[-2:]

            

            start_hour_value = get_time_value(start_hour, start_meridian)
            end_hour_value = get_time_value(end_hour, end_meridian)

            if converted_pick >= start_hour_value and converted_pick < end_hour_value:
                answers.append((rest.name, block))
                print(rest.name, block)
                print('TOP')
                break
            elif end_hour_value < start_hour_value: #Restaurant open after Midnight
                if converted_pick < end_hour_value:
                    answers.append((rest.name, block))
                    print(rest.name, block)
                    print('BOTTOM')    
                    break
        else:
            print('Invalid time for: ', rest.name, ' at ', block)
        
        
            
            




            

    places.append(rest)
    # print(rest)

if not answers : #Empty Answers
    print('Oh No!, there are no restaurants open at:', detailed_pick.upper())
else:
    print(answers)
# Closing file
f.close()


    
    
