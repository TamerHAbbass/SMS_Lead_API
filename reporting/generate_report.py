from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
import smtplib, ssl
from email.mime.text import MIMEText
from sms_lead.models import Campaign, SMS_Successful, Sent_Call_List, SMS_Queued
import datetime
import pandas
import csv

CSV = ''

def generate():
    column_name = {'Number': '', 'First': '', 'Last': '', 'Address': '', 'City': '', 'State': '', 'Zip': '', 'PropertyID': '','SMSMessage1': '',  'updated': ''}
    campaign_list = []
    queryset = Campaign.objects.all()
    
    count = 0
    data_set = SMS_Successful.objects.all().filter(campaign=str('67544c3482904aa28cca1545ae9965d0')).values('Number', 'First', 'Last', 'Address', 'City', 'State', 'Zip', 'PropertyID','SMSMessage1',  'updated')
    
    file = f"Rental_Forgiveness_Success_{str(datetime.datetime.now()).replace(':', '_').replace('.', '_')}.csv"
    with open(file, 'w+', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=column_name)
        writer.writeheader()
        
        writer.writerow(column_name)
        for data in data_set:
            if (datetime.datetime.now() - datetime.timedelta(hours=24)) < data['updated'].replace(tzinfo=None): # and datetime.datetime.now() > data['updated'].replace(tzinfo=None):
                print((datetime.datetime.now() - datetime.timedelta(hours=24)) < data['updated'].replace(tzinfo=None))
                count += 1
                writer.writerow(data)
    print("Rental Forgiveness Success:",count)
    return file, count


def generate_2():
    column_name = {'Number': '', 'First': '', 'Last': '', 'Address': '', 'City': '', 'State': '', 'Zip': '', 'PropertyID': '','SMSMessage1': '',  'updated': ''}
    campaign_list = []
    queryset = Campaign.objects.all()
    count = 0
    data_set = SMS_Successful.objects.all().filter(campaign=str('2bc8a390424f4ce68222e4bab536264b')).values('Number', 'First', 'Last', 'Address', 'City', 'State', 'Zip', 'PropertyID','SMSMessage1',  'updated')
   
    file = f"Zillow_Contacts_Success_{str(datetime.datetime.now()).replace(':', '_').replace('.', '_')}.csv"
    with open(file, 'w+', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=column_name)
        writer.writeheader()
        
        writer.writerow(column_name)
        for data in data_set:
            
            if (datetime.datetime.now() - datetime.timedelta(hours=24)) < data['updated'].replace(tzinfo=None): # and datetime.datetime.now() > data['updated'].replace(tzinfo=None):
                count += 1
                writer.writerow(data)
    print("Zillow Contacts Success:",count)
    return file, count

def generate_3():
    column_name = {'Number': '', 'First': '', 'Last': '', 'Address': '', 'City': '', 'State': '', 'Zip': '', 'PropertyID': '','SMSMessage1': '',  'updated': ''}
    queryset = Campaign.objects.all()
    
    count = 0
    data_set = Sent_Call_List.objects.all().filter(campaign=str('67544c3482904aa28cca1545ae9965d0')).values('Number', 'First', 'Last', 'Address', 'City', 'State', 'Zip', 'PropertyID','SMSMessage1',  'updated')
    file = f"Rental_Forgiveness_Failed_{str(datetime.datetime.now()).replace(':', '_').replace('.', '_')}.csv"
    with open(file, 'w+', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=column_name)
        writer.writeheader()
        
        writer.writerow(column_name)
        for data in data_set:
            if (datetime.datetime.now() - datetime.timedelta(hours=24)) < data['updated'].replace(tzinfo=None): # and datetime.datetime.now() > data['updated'].replace(tzinfo=None):
                count += 1
                writer.writerow(data)
    print("Rental Forgiveness Failed:",count)
    return file, count

def generate_4():
    column_name = {'Number': '', 'First': '', 'Last': '', 'Address': '', 'City': '', 'State': '', 'Zip': '', 'PropertyID': '','SMSMessage1': '',  'updated': ''}
    queryset = Campaign.objects.all()
    
    count = 0
    data_set = Sent_Call_List.objects.all().filter(campaign=str('2bc8a390424f4ce68222e4bab536264b')).values('Number', 'First', 'Last', 'Address', 'City', 'State', 'Zip', 'PropertyID','SMSMessage1',  'updated')
    file = f"Zillow_Contacts_Failed_{str(datetime.datetime.now()).replace(':', '_').replace('.', '_')}.csv"
    with open(file, 'w+', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=column_name)
        writer.writeheader()
        
        writer.writerow(column_name)
        for data in data_set:
            if (datetime.datetime.now() - datetime.timedelta(hours=24)) < data['updated'].replace(tzinfo=None): # and datetime.datetime.now() > data['updated'].replace(tzinfo=None):
                count += 1
                writer.writerow(data)
    print("Zillow Contacts Failed:",count)
    return file, count




sender = 'sos-api@team-sos.com'
receivers = ['tabbass@team-sos.com', 'rthornton-ad@team-sos.com']

port = 	587
user = 'sos-api@team-sos.com'
password = 'yuXn>jvuR7n*XQFH'


def send_report():
    msg = MIMEMultipart()
    msg['Subject'] = 'Tricon SMS Campaign Reporting'
    msg['From'] = sender
    msg['To'] = receivers[0]

    report1, rfsuccess = generate()
    report2, zcsuccess = generate_2()
    report3, rffail = generate_3()
    report4, zcfail = generate_4()

    part = MIMEBase('application', "octet-stream")
    part.set_payload(open(report1, "rb").read())
    # Encoders.encode_base64(part)

    part2 = MIMEBase('application', "octet-stream")
    part2.set_payload(open(report2, "rb").read())

    part3 = MIMEBase('application', "octet-stream")
    part3.set_payload(open(report3, "rb").read())

    part4 = MIMEBase('application', "octet-stream")
    part4.set_payload(open(report4, "rb").read())

    part.add_header('Content-Disposition', f"attachment; filename={report1}")
    msg.attach(part)
    part2.add_header('Content-Disposition', f"attachment; filename={report2}")
    msg.attach(part2)
    part3.add_header('Content-Disposition', f"attachment; filename={report3}")
    msg.attach(part3)
    part4.add_header('Content-Disposition', f"attachment; filename={report4}")
    msg.attach(part4)

    body = f"Good Morning, \n\n\tThe following data represents the number of records processed in the last 24 hours. Please see the attached reports for additional record information:\n\nRental Forgiveness:\n\n\tTotal: {rfsuccess+rffail}\n\n\t Successful: {rfsuccess}\n\n\t Failed: {rffail}\n\nZillow Contacts:\n\n\tTotal: {zcsuccess+zcfail}\n\n\t Successful: {zcsuccess}\n\n\t Failed: {zcfail}"
    body = MIMEText(body) # convert the body to a MIME compatible string
    msg.attach(body) # attach it to your main message

    server = smtplib.SMTP('webmail.team-sos.com', timeout=6000)
    server.sendmail(msg['From'], msg['To'], msg.as_string())