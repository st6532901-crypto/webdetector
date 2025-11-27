import pytz
from datetime import datetime
indian_timezone = pytz.timezone('Asia/Kolkata')
current_time = datetime.now(indian_timezone)
formatted_time = current_time.strftime("%H:%M:%S")
print("Current Indian Time:", formatted_time)
hour = current_time.hour
minute = current_time.minute
seconds = current_time.second
print("hour", hour)
print("minute", minute)
print("seconds", seconds)
if hour >= 0 and hour < 12:
    print("Good Morning sir!")
elif hour >= 12 and hour < 17:
    print("Good afternoon sir!")
elif hour >= 17 and hour < 21:
    print("Good evening sir!")
elif hour >= 21 and hour <= 24:
    print("Good night sir!")
    