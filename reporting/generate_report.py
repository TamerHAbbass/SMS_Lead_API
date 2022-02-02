from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
import smtplib, ssl
from email.mime.text import MIMEText
from sms_lead.models import Campaign, SMS_Successful, Sent_Call_List, SMS_Queued
import datetime
import pandas
import csv

CSV = ''

class GenerateReport:
    
    def __init__(self, campaign_name, columns, days):
        self.columns = columns
        self.campaign_name = campaign_name
        self.campaign_id = None
        self.queryset = None
        self.count = 0
        self.data_success = None
        self.data_fail = None
        self.file = None
        self.numberDays = days


    def getCampaignId(self):
        qs = Campaign.objects.get(name=self.campaign_name)
        self.campaign_id = qs.uuid.__str__().replace('-','')
        return self.campaign_id

    
    def getSMSList(self):
        self.data_fail = Sent_Call_List.objects.all().filter(campaign=self.campaign_id).values(*self.columns)
        self.data_success = SMS_Successful.objects.all().filter(campaign=self.campaign_id).values(*self.columns)
        return 1

    def setReportFileName(self):
        self.file = f"{self.campaign_name.replace(' ','_')}_{str(datetime.datetime.now()).replace(':', '_').replace('.', '_')}.csv"
        return 0

    def writeSMSByFilteredDate(self):
        count_fail, count_success = 0, 0
        with open(self.file, 'w+', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.columns)
            writer.writeheader()
            writer.writerow(self.columns)

            # Process Failed
            for data in self.data_fail.order_by('updated'):
                if (datetime.datetime.now() - datetime.timedelta(days=self.numberDays)) < data['updated'].replace(tzinfo=None) and (datetime.datetime.now()) > data['updated'].replace(tzinfo=None):
                        count_fail += 1
                        writer.writerow(data)
            print(f"{self.campaign_name} Failed:",count_fail)

            # Process Success
            for data in self.data_success.order_by('updated'):
                if (datetime.datetime.now() - datetime.timedelta(days=self.numberDays)) < data['updated'].replace(tzinfo=None) and (datetime.datetime.now()) > data['updated'].replace(tzinfo=None):
                        count_success += 1
                        writer.writerow(data)
            print(f"{self.campaign_name} Success:",count_success)
        return self.file, count_fail, count_success


    def sendEmail(self, receivers, file, count_fail, count_success):

        sender = 'sos-api@team-sos.com'
        receivers = receivers

        port = 	'587'
        user = 'sos-api@team-sos.com'
        password = 'YQyBjZCA)ye8kBdA'

        msg = MIMEMultipart()
        msg['Subject'] = 'Tricon SMS Campaign Reporting'
        msg['From'] = sender

        part = MIMEBase('application', "octet-stream")
        part.set_payload(open(self.file, "rb").read())

        part.add_header('Content-Disposition', f"attachment; filename={self.file}")
        msg.attach(part)

        body = f"Good Morning, \n\n\tThe following data represents the number of records processed between {(datetime.datetime.now() - datetime.timedelta(days=self.numberDays)).strftime('%m-%d-%y %I:%M')} - {datetime.datetime.now().strftime('%m-%d-%y %I:%M')}. Please see the attached reports for additional record information:\n\n\n{self.campaign_name.title()}\n\n\tSuccess: {count_success}\n\n\tFailed: {count_fail}\n\n\tTotal: {count_fail+count_success}\n\nThank you!"
        body = MIMEText(body) # convert the body to a MIME compatible string
        msg.attach(body) # attach it to your main message


        server = smtplib.SMTP('webmail.team-sos.com',timeout=6000)
        # server.login(user=user, password=password)
        server.starttls()
        server.login(user=user, password=password)
        for i in receivers:
            print(f"Sending to contact: {i}")
            server.sendmail(msg['From'], to_addrs=i, msg=msg.as_string())

def cleanUpReportFile(file):
    import os
    os.remove(file)


def processReport(campaign_name, columns, receivers, days):
    report = GenerateReport(campaign_name, columns, days)
    report.getCampaignId()
    report.setReportFileName()
    report.getSMSList()
    file, successc, failc = report.writeSMSByFilteredDate()
    report.sendEmail(receivers, file, successc, failc)
    cleanUpReportFile(file)


def main():
    receivers = ['tabbass@team-sos.com', 'rthornton@team-sos.com', 'gknutson@triconresidential.com']

    # Rental Forgiveness & Zillow Contacts Reports
    columns = {'Number': '', 'First': '', 'Last': '', 'Address': '', 'City': '', 'State': '', 'Zip': '', 'PropertyID': '','SMSMessage1': '',  'updated': ''}
    processReport('Rental Forgiveness', columns, receivers, days=7)
    processReport('Zillow Contacts', columns, receivers, days=7)

    # MF_Communications
    columns = {'Number': '', 'First': '', 'PropertyID': '', 'SMSMessage1': '', 'updated': ''}
    processReport('MF_Communications', columns, receivers, days=7)



if __name__ == '__main__':
    main()