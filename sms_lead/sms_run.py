import csv
import json
import os
import io
import re
import pandas
import PureCloudPlatformClientV2
import requests
import time
from .models import SMS_Lead_Data
import math


SMS_CHAR_LIMIT = 512

def connect_to_purecloud():
    # Set Purecloud region
    region = PureCloudPlatformClientV2.PureCloudRegionHosts.us_west_2

    # Get API Host for Purecloud region
    PureCloudPlatformClientV2.configuration.host = region.get_api_host()

    # Create API Client and get client credentials with client ID and key
    apiclient = PureCloudPlatformClientV2.api_client.ApiClient().get_client_credentials_token(os.environ.get('Tricon_SMS_Client_ID'), os.environ.get('Tricon_SMS_Client_Secret'))

    return apiclient


def grab_lead_data(apiclient):
   
    zillow_list_id = os.environ.get('Tricon_Zillow_Contact_ID')
    zillow_contact_list_url = os.environ.get('Tricon_Contact_List_URI')

    api_instance = PureCloudPlatformClientV2.OutboundApi(apiclient)
    # Grab Zillow_Master download URI
    exporturi = api_instance.get_outbound_contactlist_export(zillow_list_id).to_dict()

    # Grab CSV content by providing the download uri with authorization header
    req = requests.get(exporturi['uri'], headers={'authorization': f'Bearer {apiclient.access_token}'}).text

    return req


def download_data(req):
      zillow_json = pandas.read_csv(io.StringIO(req))
    #   with open('.\contact_pull.json', 'a+') as f:
    #       json.dump(zillow_json, f)
      return zillow_json


def save_data(row):
    sms_model = SMS_Lead_Data()

    sms_model.Number = row['Number']
    sms_model.Type = row['Type']
    sms_model.Timezone = row['Timezone']
    sms_model.First = row['First']
    sms_model.Last = row['Last']
    sms_model.Address = row['Address']
    sms_model.City = row['City']
    sms_model.State = row['State']
    sms_model.Zip = row['Zip']
    # sms_model.PropertyID = row['PropertyID']
    # sms_model.UploadDate = row['UploadDate']
    # sms_model.SMSMessage1 = row['SMSMessage1']
    # sms_model.SMSMessage2 = row['SMSMessage2'].fillna(0)
    # sms_model.SMSMessage3 = row['SMSMessage3'].fillna(0)
    # sms_model.SMSMessage4 = row['SMSMessage4'].fillna(0)
    # sms_model.SMSStatus = row['SMSStatus']
    # sms_model.SMSTimeStamp = row['SMSTimeStamp']
    sms_model.save()

def parse_data(zillow):
    complete_list = []
    for count, (index, row) in enumerate(zillow.iterrows()):
        sms = {}
        message = {}
        save_data(row)
        for r, l in row.items():
            if re.findall(r'^smsmessage', r.lower()):
                message[r] = l
                sms['sms'] = message
            else:
                sms[r] = l
    complete_list.append(sms)
    return complete_list


def agentless_sms(apiclient, data):
    # # Create Outbound Api Client
    api_instance = PureCloudPlatformClientV2.ConversationsApi(apiclient)
    body = PureCloudPlatformClientV2.SendAgentlessOutboundMessageRequest()
    try:
        api_response = api_instance.post_conversations_messages_agentless(data)
        json_api_response = json.loads(api_response.to_json())
        with open('.\SMS_Response.json', 'a+') as f:
            json.dump(json_api_response, f)
    except Exception as e:
        failed_record = {str(400):data}
        with open('.\SMS_Response.json', 'a+') as f:
            json.dump(failed_record, f)


def char_count(message):
    message_segments = []
    a_string = message
    n = SMS_CHAR_LIMIT
    message_segments = [a_string[index : index + n] for index in range(0, len(a_string), n)]
    return message_segments


def compose_sms(contact):
    sms_messages = []
    sms_message = []
    if contact['Type'] == 'Cell':
        contact['Type'] = 'sms'
    for x, z in contact['sms'].items():
        if not z.lower() == 'nan':
                sms_message.append(z)

    message = f"Hi {contact['First']}, {str(' '.join(sms_message))}"
    message_segments = char_count(message)
    for count, x in enumerate(message_segments):
        data = {
        "fromAddress": str(os.environ.get('Tricon_fromAddress')),
        "toAddress": "...", #''.join(["+1", str(contact['Number'])]),
        "toAddressMessengerType": str(contact['Type']),
        "textBody": x,
        }
        sms_messages.append(data)
    return sms_messages


def send_failed_to_agentless_campaign():
      pass


def main():
    connection = connect_to_purecloud()
    uri = grab_lead_data(connection)
    data = download_data(uri)
    parsed_data = parse_data(data)
    for d in parsed_data:
        composed_message = compose_sms(d)
        for message in composed_message:
            pass
            agentless_sms(connection, message)


if __name__ == "__main__":
    main()