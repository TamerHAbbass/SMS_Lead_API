from datetime import datetime
import pytz
  

IST = pytz.timezone('CST6CDT')
print("IST in Default Format : ", datetime.now(IST))


import datetime as dt
from scheduler import Scheduler
import scheduler.trigger as trigger

# Create a payload callback function
def useful():
    print("Very useful function.")

# Instead of setting the timezones yourself you can use the `pytz` library
tz_new_york = dt.timezone(dt.timedelta(hours=-5))
tz_wuppertal = dt.timezone(dt.timedelta(hours=2))
tz_sydney = dt.timezone(dt.timedelta(hours=10))




UTC-12: Anywhere on Earth (AoE)
UTC-11: Samoa Standard Time (ST)
UTC-10: Hawaii-Aleutian Standard Time (HAT)
UTC-9: Alaska Standard Time (AKT)
UTC−8: Pacific Standard Time (PT)
UTC−7: Mountain Standard Time (MT)
UTC−6: Central Standard Time (CT)
UTC−5: Eastern Standard Time (ET)
UTC−4: Atlantic Standard Time (AST)
UTC+10: Chamorro Standard Time (ChT)
UTC+12: Wake Island Time Zone (WIT)


# can be any valid timezone
schedule = Scheduler(tzinfo=dt.timezone.utc)

# schedule jobs
schedule.daily(dt.time(hour=12, tzinfo=tz_new_york), useful)
schedule.daily(dt.time(hour=12, tzinfo=tz_wuppertal), useful)
schedule.daily(dt.time(hour=12, tzinfo=tz_sydney), useful)

# Show a table overview of your jobs
print(schedule)


