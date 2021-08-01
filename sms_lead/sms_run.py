import datetime
import json
import os
import io
import re
import pandas
import PureCloudPlatformClientV2
import requests
import pytz
import time
from requests.models import Response
from urllib3.connection import _CONTAINS_CONTROL_CHAR_RE
from .models import SMS_Lead_Data
from .serializers import SMSLeadSerializer


START_TIME = '06:00:00'
END_TIME = '20:00:00'
SMS_CHAR_LIMIT = 520

def log_data(action):
    # log_data will print action to screen and log in DATE log file
    
    print(action)
    with open(".\\logs\\" + datetime.date.today().isoformat().replace('-', '') + "_insertSet.log", 'a+') as f:
        f.write(str(datetime.datetime.now()) + f": {action}..." + '\n')
        return 1


def connect_to_purecloud():
    # Set Purecloud region
    region = PureCloudPlatformClientV2.PureCloudRegionHosts.us_west_2

    # Get API Host for Purecloud region
    PureCloudPlatformClientV2.configuration.host = region.get_api_host()

    # Create API Client and get client credentials with client ID and key
    apiclient = PureCloudPlatformClientV2.api_client.ApiClient().get_client_credentials_token(os.environ.get('Tricon_SMS_Client_ID'), os.environ.get('Tricon_SMS_Client_Secret'))

    return apiclient


def grab_lead_data(apiclient):
    # Temp
    zillow_list_id = os.environ.get('Tricon_Zillow_Contact_ID')
    zillow_contact_list_url = os.environ.get('Tricon_Contact_List_URI')
    try:
        api_instance = PureCloudPlatformClientV2.OutboundApi(apiclient)
        # Grab Zillow_Master download URI
        exporturi = api_instance.get_outbound_contactlist_export(zillow_list_id).to_dict()

        # Grab CSV content by providing the download uri with authorization header
        req = requests.get(exporturi['uri'], headers={'authorization': f'Bearer {apiclient.access_token}'}).text
    except:
        try:
            api_instance.post_outbound_contactlist_export('215b5365-0fcd-4ce4-8ac9-7f2f18eb5a1d')
            time.wait(1)
            api_instance = PureCloudPlatformClientV2.OutboundApi(apiclient)
            # Grab Zillow_Master download URI
            exporturi = api_instance.get_outbound_contactlist_export(zillow_list_id).to_dict()
            # Grab CSV content by providing the download uri with authorization header
            req = requests.get(exporturi['uri'], headers={'authorization': f'Bearer {apiclient.access_token}'}).text
        except:
            log_data("Unable to download contactlist export.. please check Purecloud. Updating the ContactList UUID may be required")
    return req


def download_data(req):
      zillow_json = pandas.read_csv(io.StringIO(req))
    #   with open('.\contact_pull.json', 'a+') as f:
    #       json.dump(zillow_json, f)
      return zillow_json


def checking_timezonez_in_range(startTime, endTime, timezone):
    startTime = datetime.datetime.strptime(startTime, "%H:%M:%S").time()
    endTime = datetime.datetime.strptime(endTime, "%H:%M:%S").time()
    print(startTime, endTime, timezone)
    # get the standard UTC time 
    UTC = pytz.utc
    
    # it will get the time zone 
    # of the specified location
    IST = datetime.datetime.now(pytz.timezone(timezone))
    time_in_zone = datetime.datetime.strptime(IST.strftime('%T'), "%H:%M:%S").time()
    print(time_in_zone)
    if startTime < endTime: 
        print(time_in_zone >= startTime and time_in_zone <= endTime )
        return time_in_zone >= startTime and time_in_zone <= endTime 
    else: 
        #Over midnight: 
        return time_in_zone >= startTime or time_in_zone <= endTime 

    
def parse_data(row):
    sms = {}
    message = {}
    # row = handle_nan(row_na)
    for r, l in row.items():
        if re.findall(r'^smsmessage', r.lower()):
            message[r] = l
            sms['sms'] = message
        else:
            sms[r] = l
    return sms


def agentless_sms(apiclient, data):
    # # Create Outbound Api Client
    api_instance = PureCloudPlatformClientV2.ConversationsApi(apiclient)
    body = PureCloudPlatformClientV2.SendAgentlessOutboundMessageRequest()
    try:
        api_response = api_instance.post_conversations_messages_agentless(data)
        json_api_response = json.loads(api_response.to_json())
        with open('.\SMS_Response.json', 'a+') as f:
            json.dump(json_api_response, f)
        return json_api_response['conversation_id'], json_api_response['timestamp'] 
    except Exception as e:
        failed_record = {str(400):data}
        with open('.\SMS_Response.json', 'a+') as f:
            json.dump(failed_record, f)
        return 0, 0


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
    for key, value in contact['sms'].items():
        sms_message.append(value)
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


def check_status_of_sent_sms(apiclient, uuid):
    api_instance = PureCloudPlatformClientV2.ConversationsApi(apiclient)
    body = PureCloudPlatformClientV2.SendAgentlessOutboundMessageRequest()


    try:
        status = json.loads(api_instance.get_conversations_message(uuid).to_json())
        check = status['participants'][0]['messages'][0]['message_status']
    except Exception as e:
        check = 0
    if check == 'sent':
        check = True
    else:
        check = False
    return check

def send_failed_to_agentless_campaign():
      pass


def delete_contact_from_purecloud_list(apiclient, zillow_list_id, contact_uuid):
    api_instance = PureCloudPlatformClientV2.ConversationsApi(apiclient)
    body = PureCloudPlatformClientV2.SendAgentlessOutboundMessageRequest()
    response = api_instance.delete_outbound_contactlist_contacts(zillow_list_id, contact_uuid)


def check_contact_record_in_db(contact):
    queryset = SMS_Lead_Data.objects.all()
    try:
        results = SMS_Lead_Data.objects.get(uuid=contact['inin-outbound-id'])
        return 1
    except:
        return 0


def save_data(row, index, response='', status=''):
    sms_model = SMS_Lead_Data()

    # Handle Na values
    df = pandas.DataFrame(row)
    df = df.fillna(0).to_dict()[index]

    record = check_contact_record_in_db(df)

    try:
        sms_model.uuid = df['inin-outbound-id']
        sms_model.Number = df['Number']
        sms_model.Type = df['Type']
        sms_model.Timezone = df['Timezone']
        sms_model.First = df['First']
        sms_model.Last = df['Last']
        sms_model.Address = df['Address']
        sms_model.City = df['City']
        sms_model.State = df['State']
        sms_model.Zip = df['Zip']
        sms_model.PropertyID = df['PropertyID']
        sms_model.UploadDate = df['UploadDate']
        sms_model.SMSMessage1 = df['SMSMessage1']
        # sms_model.SMSMessage2 = df['SMSMessage2']
        # sms_model.SMSMessage3 = df['SMSMessage3']
        # sms_model.SMSMessage4 = df['SMSMessage4']
        

        sms_model.save()

        return df['inin-outbound-id']
    except:
        return 0


def query(queued=True):
    queryset = SMS_Lead_Data.objects.all()
    queued = SMS_Lead_Data.objects.filter(queued=queued).values('uuid', 'First', 'Number', 'Type', 'Timezone', 'SMSMessage1')
    return queued


def update_data(contact_uuid, status, response, timestamp):

    queryset = SMS_Lead_Data.objects.all()
    results = SMS_Lead_Data.objects.get(uuid=contact_uuid)
    if timestamp:
        results.SMSTimeStamp = timestamp
    results.SMSStatus = status
    results.sentSMSId = response
    results.queued = False
    results.save()


def start_sms():
    connection = connect_to_purecloud()
    uri = grab_lead_data(connection)
    data = download_data(uri)
    for count, (index, row) in enumerate(data.iterrows()):
        contact_uuid = save_data(row, count)
        if contact_uuid:
            pass
            #delete_contact_from_purecloud_list(os.environ.get['Tricon_Zillow_Contact_ID'], contact_uuid)

    queued = query()

    for count, q in enumerate(queued):
        print(q['Timezone'])
        if checking_timezonez_in_range(START_TIME, END_TIME, q['Timezone']):
            q['in_range'] = True

            parsed_Data = parse_data(q)
            composed_message = compose_sms(parsed_Data)

            response = ''
            status = ''

            for message in composed_message:
                response, timestamp = agentless_sms(connection, message)
                status = check_status_of_sent_sms(connection, response)
            contact_uuid = update_data(q['uuid'], status, response, timestamp)


if __name__ == "__main__":
    start_sms()