# import pandas lib as pd
import pandas as pd


def date_time(inp):
    # splitting by space gives 2 values, the date, time
    timings = inp.split(' ')

    # if length is not 2, then invalid data, move to the next row
    if len(timings) != 2:
        return -1,-1
    
    # splitting the date by '-'
    # gives 3 values, month, day, year
    date = timings[0].split('-')

    # if length is not 3, then invalid data, move to the next row
    if len(date) != 3:
        return -1,-1

    # since all dates are in same month, only the day is of the matter
    day = int(date[2])

    # check for valid date
    if day > 31 or day < 1:
        return -1,-1
    
    # timings[1] is of the format ##:##:##
    if len(timings[1].split(':')) != 3:
        return -1,-1
    
    hour = int(timings[1].split(':')[0])
    min = int(timings[1].split(':')[1])

    # invalid time data
    if hour<0 or hour>23 or min<0 or min>60:
        return -1,-1
    
    # calculating time in total minutes
    time = hour*60 + min

    return day,time

def diff_in_min(day1,time1,day2,time2):
    if day1 == day2:
        # if time1 < time2, invalid entry
        if time1 < time2:
            return -1
        else:
            return time2-time1
    else:
        diff = 24*60-time1 + time2 + (day2-day1-1)*60
        return diff

# read by default 1st sheet of an excel file
df = pd.read_excel('Assignment_Timecard.xlsx')

# employee_timings = {
#     'name1': [
#                {
#                     'checkin_day':'##',
#                     'checkin_time':'##',
#                     'checkout_day':'##',
#                     'checkout_time':'##'
#                }
#             ]
# }

employee_timings = {}

#storing employee postion ID
employee_position_id = {}

# iterating through the rows of the excel file

# checkin_day,checkin_time = date_time(str(df['Time'][1]))

for ind in df.index:
    # get the names of the employees in the row
    names = str(df['Employee Name'][ind]).split(',')

    # get the values of checkin day and time
    checkin_day,checkin_time = date_time(str(df['Time'][ind]))
    # get the values of checkout day and time
    checkout_day,checkout_time = date_time(str(df['Time Out'][ind]))

    if checkin_day == -1 or checkout_day == -1:
        continue
    id = str(df['Position ID'][ind])

    slot_timings = {'checkin_day':checkin_day,
                    'checkin_time':checkin_time,
                    'checkout_day':checkout_day,
                    'checkout_time':checkout_time}
    
    for name in names:
        name.strip()
        if name in employee_position_id:
            employee_position_id[name] = id
        else:
            employee_position_id.update({name:id})
        
        if name in employee_timings:
            employee_timings[name].append(slot_timings)
        else:
            employee_timings.update({name:[slot_timings]})

cons_7_days = set()
break_10_hours = set()
work_14_hours = set()

# calculating for each employee
for employee in employee_timings:
    prev_day = 0
    prev_time = 0
    days = [0]*32
    # going shift wise for a employee
    for ind in range(0,len(employee_timings[employee])):        
        if ind == 0:
            checkin_day = employee_timings[employee][ind]['checkin_day']
            checkin_time = employee_timings[employee][ind]['checkin_time']
            checkout_day = employee_timings[employee][ind]['checkout_day']
            checkout_time = employee_timings[employee][ind]['checkout_time']
            shift_duration = diff_in_min(checkin_day,checkin_time,checkout_day,checkout_time)
            if shift_duration >= 14*60:
                work_14_hours.add(employee)

            if shift_duration != -1:
                prev_day = checkout_day
                prev_time = checkout_time
            
            days[checkin_day] = 1

        else:
            checkin_day = employee_timings[employee][ind]['checkin_day']
            checkin_time = employee_timings[employee][ind]['checkin_time']
            checkout_day = employee_timings[employee][ind]['checkout_day']
            checkout_time = employee_timings[employee][ind]['checkout_time']
            
            # finding the break length
            break_duration = diff_in_min(prev_day,prev_time,checkin_day,checkin_time)
            if break_duration > 60 and break_duration < 10*60:
                break_10_hours.add(employee)

            # finding the shift length
            shift_duration = diff_in_min(checkin_day,checkin_time,checkout_day,checkout_time)
            if shift_duration >= 14*60:
                work_14_hours.add(employee)

            if shift_duration != -1:
                prev_day = checkout_day
                prev_time = checkout_time

            days[checkin_day] = 1
    cons = 1
    # checking max number of consecutive days
    for ind in range(1,32):
        if days[ind] == 1:
            cons = cons + 1
        else:
            if cons >= 7:
                cons_7_days.add(employee)
            cons = 0

# writing the output to output.txt
file = open('output.txt','w')
file.writelines("People who have worked more than 14 hours in single shift\n")
for ele in work_14_hours:
    file.writelines(ele)
    file.writelines('\n')
file.writelines("\nPeople who have worked for more than 7 consecutive days\n")
for ele in cons_7_days:
    file.writelines(ele)
    file.writelines('\n')
file.writelines("\nPeople whose shift break duration is less than 10 hours but greater than 1 hour\n")
for ele in break_10_hours:
    file.writelines(ele)
    file.writelines('\n') 
file.close()


            
            


        


    
    




