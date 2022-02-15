import json
from restaurant import Restaurant
 
def time_to_value(_day, _time, _ampm):
    days_to_value = {'mon': 0, 'tue': 24, 'wed': 48, 'thu': 72, 'fri': 96, 'sat': 120, 'sun': 144}
    val = days_to_value[_day]
    hour, min = _time.split(':')
    val += int(hour)
    val += int(min)/60

    if _ampm == 'pm':
        val += 12
    return val

def get_days(start, end):
    days_of_week = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
    start_index = days_of_week.index(start)
    end_index = days_of_week.index(end)+1
    return days_of_week[start_index:end_index]

# Opening JSON file
f = open('rest_hours.json')
 
# returns JSON object as
# a dictionary
data = json.load(f)
 
# Iterating through the json
# list
day = input('What day do you want to eat? (Mon, Tue, Wed, Thu, Fri, Sat, Sun)--->').strip()
day = day.lower()

desired_time = input('When do you want to eat? (HH:MM)')

am_or_pm = input('AM or PM?')
am_or_pm = am_or_pm.lower()

print('you picked: ', day, ' at ', desired_time, ' ', am_or_pm)

converted_pick = time_to_value(day, desired_time, am_or_pm)
print(converted_pick)


places = []
answers = []
for listing in data:
    rest = Restaurant()
    rest.name = listing["name"]
    rest.times = listing['times']
    conver_times = []
    for block in rest.times:
        for index in range(0, len(block)):
            if block[index] == ',':
                index +=1
                
            what_day = block[index:index+3].lower()
            if block[index + 3] == "-":
                start_day = what_day
                end_day = block[index + 4:index + 7].lower()
                options = get_days(start_day, end_day)
                # if day in options:
                #     pass
                index+=7
            

    places.append(rest)
    # print(rest)
 
# Closing file
f.close()


    
    
