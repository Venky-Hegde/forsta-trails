# from ics import Calendar, Event
# from django.core.mail import EmailMessage
# from smartrec.settings import EMAIL_HOST_USER,EMAIL_HOST_PASSWORD
# from jobs.models import Job
#/home/aveto/Desktop/gitnew4/forsta/smartrec/settings/base.py

from dateutil import tz


# #
# def send_email(excel_file):
#     # print(user_email,"^^^^^^^^^^^^^^^")
#     # from_string = '{0} <{1}>'.format("aaaaaaaaaaaaaaaaaaa", user_email)
#     # print(from_string,"###########3333333")
#     subject="ical"
#     email_message="my events"
#     user_email=EMAIL_HOST_USER
#     to_email_list=["sinchana.k@avetoconsulting.com"]
#     email = EmailMessage(subject,email_message,user_email,to_email_list)
#
#     email.attach_file(excel_file)
#
#     email.send()
#
#
#
# c = Calendar()
# e = Event()
# e.name = "My cool event"
# e.begin = '20140101 00:00:00'
# c.events.add(e)
# print(c.events)
# with open('my.ics', 'w') as my_file:
#     my_file.writelines(c)
#     res = my_file
#     filename = str(res) + ".ics"
#     file_path = base.MEDIA_ROOT + '/' + filename
#     send_email(my_file)
# print(str(file_path))



from icalendar import Calendar, Event
from datetime import datetime
from pytz import UTC # timezone

cal = Calendar()
cal.add('prodid', '-//My calendar product//mxm.dk//')
cal.add('version', '2.0')
from_zone = tz.tzutc()
to_zone = tz.tzlocal()
utc = datetime.strptime('2019-02-21 02:37:21', '%Y-%m-%d %H:%M:%S')
utc = utc.replace(tzinfo=from_zone)
central = utc.astimezone(to_zone)

event = Event()
event.add('summary', 'Python meeting about calendaring')
event.add('dtstart', datetime(2019,2,21,8,0,0,tzinfo=UTC))
event.add('dtend', datetime(2019,2,21,10,0,0,tzinfo=UTC))
event.add('dtstamp', datetime(2019,2,21,0,10,0,tzinfo=UTC))
event['uid'] = '20050115T101010/27346262376@mxm.dk'
event.add('priority', 5)

cal.add_component(event)

f = open('example.ics', 'wb')
f.write(cal.to_ical())
f.close()

g = open('example.ics','rb')
gcal = Calendar.from_ical(g.read())
for component in gcal.walk():
    print(component.name)
g.close()


g = open('example.ics','rb')
gcal = Calendar.from_ical(g.read())
for component in gcal.walk():
    if component.name == "VEVENT":
        print(component.get('summary'))
        print(component.get('dtstart'))
        print(component.get('dtend'))
        print(component.get('dtstamp'))
g.close()