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
from .models import Campaign, SMS_Queued, Sent_Call_List, SMS_Successful
from apscheduler.schedulers.blocking import BlockingScheduler


SMS_CHAR_LIMIT = 512


def log_data(action, logname):

    # log_data will print action to screen and write to log file
    
    print(action)
    with open(f".\\logs\\{logname}_{datetime.date.today().isoformat().replace('-', '')} insertSet.log", 'a+') as f:
        f.write(str(datetime.datetime.now()) + f": {action}..." + '\n')
        return 1


def connect_to_purecloud(client_id, client_secret):
    log_data('Connecting to PureCloud', 'SMS_RUN_APP')
    # Set Purecloud region
    region = PureCloudPlatformClientV2.PureCloudRegionHosts.us_west_2

    # Get API Host for Purecloud region
    PureCloudPlatformClientV2.configuration.host = region.get_api_host()

    # Create API Client and get client credentials with client ID and key
    apiclient = PureCloudPlatformClientV2.api_client.ApiClient().get_client_credentials_token(client_id, client_secret)

    return apiclient


def grab_lead_data(apiclient, contact_list_id):

    log_data('Grabbing Lead Data', 'SMS_RUN_APP')
    zillow_list_id = contact_list_id

    try:
        api_instance = PureCloudPlatformClientV2.OutboundApi(apiclient)
        api_instance.post_outbound_contactlist_export(zillow_list_id)
        time.sleep(60)

        # Grab Zillow_Master download URI
        exporturi = api_instance.get_outbound_contactlist_export(zillow_list_id).to_dict()

        # Grab CSV content by providing the download uri with authorization header
        req = requests.get(exporturi['uri'], headers={'authorization': f'Bearer {apiclient.access_token}'}).text
        log_data('Lead Data Extraction Successful', 'SMS_RUN_APP')
        return req
    except:
        log_data("Unable to download contactlist export.. please check Purecloud. Updating the ContactList UUID may be required", "SMS_RUN_APP")
        return 0


def download_data(req):
      zillow_json = pandas.read_csv(io.StringIO(req))
    #   with open('.\contact_pull.json', 'a+') as f:
    #       json.dump(zillow_json, f)
      return zillow_json


def checking_timezonez_in_range(startTime, endTime, timezone):
    log_data('Verifying Timezone Within Range', 'SMS_RUN_APP')

    try:
        startTime = datetime.datetime.strptime(startTime, "%H:%M:%S").time()
        endTime = datetime.datetime.strptime(endTime, "%H:%M:%S").time()

        # get the standard UTC time 
        UTC = pytz.utc
        
        # it will get the time zone 
        # of the specified location
        IST = datetime.datetime.now(pytz.timezone(timezone))
        time_in_zone = datetime.datetime.strptime(IST.strftime('%T'), "%H:%M:%S").time()

        if startTime < endTime: 
            log_data(f"Timezone Within Range: \n\t{timezone}: {time_in_zone >= startTime and time_in_zone <= endTime}", 'SMS_RUN_APP')
            return time_in_zone >= startTime and time_in_zone <= endTime 
        else: 
            log_data(f"Timezone Within Range: \n\t{timezone}: {time_in_zone >= startTime and time_in_zone <= endTime}", 'SMS_RUN_APP')
            #Over midnight: 
            return time_in_zone >= startTime or time_in_zone <= endTime 
    except:
        return False


def parse_data(row):
    log_data(f"Parsing Data: {row}", 'SMS_RUN_APP')
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
        log_data(f"SMS - Sent:\n\t{data} - {api_response}", "Sent_SMS")
        return json_api_response['conversation_id'], json_api_response['timestamp'] 
    except:
        failed_record = {str(400):data}
        log_data(f"SMS - Failed:\n\t{failed_record}", "Failed_SMS")
        return 0, 0


def char_count(message):
    log_data('Checking Char Count', 'SMS_RUN_APP')
    message_segments = []
    a_string = message
    n = SMS_CHAR_LIMIT
    message_segments = [a_string[index : index + n] for index in range(0, len(a_string), n)]
    return message_segments


def compose_sms(contact, number):
    log_data('Composing Message', 'SMS_RUN_APP')
    sms_messages = []
    sms_message = []
    if contact['Type'] == 'Cell':
        contact['Type'] = 'sms'
    for key, value in contact['sms'].items():
        sms_message.append(value)
    message = f" {str(' '.join(sms_message))}"
    message_segments = char_count(message)
    for count, x in enumerate(message_segments):
        data = {
        "fromAddress": str(os.environ.get('Tricon_fromAddress')),
        "toAddress": ''.join(["+1", str(contact['Number'])]),
        "toAddressMessengerType": str(contact['Type']),
        "textBody": x,
        }
        sms_messages.append(data)
    return sms_messages


def check_status_of_sent_sms(apiclient, uuid):
    api_instance = PureCloudPlatformClientV2.ConversationsApi(apiclient)
    body = PureCloudPlatformClientV2.SendAgentlessOutboundMessageRequest()
    check = 0
    try:
        status = json.loads(api_instance.get_conversations_message(uuid).to_json())
        check = status['participants'][0]['messages'][0]['message_status']
        if check == 'sent':
            return 1
        elif check == 'failed':
            return 0
        
    except Exception as e:
        log_data(f"Failed - {uuid}", "Verify_Sent_SMS")
        return 0


def delete_contact_from_purecloud_list(apiclient, zillow_list_id, contact_uuid):
    api_instance = PureCloudPlatformClientV2.ConversationsApi(apiclient)
    body = PureCloudPlatformClientV2.SendAgentlessOutboundMessageRequest()
    response = api_instance.delete_outbound_contactlist_contacts(zillow_list_id, contact_uuid)


def check_contact_record_in_db(contact, cl_uuid):
    queryset = SMS_Successful.objects.filter(cl_uuid=cl_uuid, )
    queryset_2 = Sent_Call_List.objects.filter(cl_uuid=cl_uuid, )
    queryset_3 = SMS_Queued.objects.filter(cl_uuid=cl_uuid, )

    if len(queryset) + len(queryset_2) + len(queryset_3) > 0 :
        return 1
    return 0


def save_data(row, index, campaign_uuid, response='', status=''):

    sms_model = SMS_Queued()

    # Handle Na values
    df = pandas.DataFrame(row)
    df = df.fillna(0).to_dict()[index]

    record = check_contact_record_in_db(df, df['inin-outbound-id'])

    if record:
        return 0
    print(campaign_uuid)
    log_data(f"Saving Contact To DB: {df['inin-outbound-id']} - {df['First']} {df['Last']} - {df['Number']} - {df['Timezone']} - {df['PropertyID']} - {df['SMSMessage1']}", 'SMS_RUN_APP')
    sms_model.cl_uuid = df['inin-outbound-id']
    sms_model.Number = df['Number']
    sms_model.campaign = str(campaign_uuid).replace('-','')
    sms_model.Type = df['Type']
    sms_model.Timezone = df['Timezone']
    sms_model.First = df['First']
    sms_model.Last = df['Last']
    sms_model.Address = df['Address']
    sms_model.City = df['City']
    sms_model.State = df['State']
    sms_model.Zip = df['Zip']
    sms_model.PropertyID = df['PropertyID']
    sms_model.SMSMessage1 = df['SMSMessage1']
    sms_model.queued = 1
    sms_model.save()

    return df['inin-outbound-id']



def query(campaign_uuid):
    queryset = SMS_Queued.objects.all()
    queued = queryset.filter(campaign=str(campaign_uuid).replace('-',''), queued=1)
    print("Queued Non-Dict:",len(queued))
    return queued


def send_called_db(contact, timestamp):

    sent_call_list = Sent_Call_List()

    sent_call_list.campaign = contact.campaign
    sent_call_list.cl_uuid = contact.cl_uuid
    sent_call_list.Number = contact.Number
    sent_call_list.Type = contact.Type
    sent_call_list.Timezone = contact.Timezone
    sent_call_list.First = contact.First
    sent_call_list.Last = contact.Last
    sent_call_list.Address = contact.Address
    sent_call_list.City = contact.City
    sent_call_list.State = contact.State
    sent_call_list.Zip = contact.Zip
    sent_call_list.PropertyID = contact.PropertyID
    sent_call_list.UploadDate = timestamp
    sent_call_list.SMSMessage1 = contact.SMSMessage1
    sent_call_list.save()
    contact.delete()
    print('Record deleted and moved to failed db')


def send_successful_db(uuid, contact, timestamp):
    # if not len(q) == 0:
    #     q = q[0]
    print('Sent', contact)
    sms_successful= SMS_Successful()

    sms_successful.campaign = contact.campaign
    sms_successful.cl_uuid = contact.cl_uuid
    sms_successful.Number = contact.Number
    sms_successful.Type = contact.Type
    sms_successful.Timezone = contact.Timezone
    sms_successful.First = contact.First
    sms_successful.Last = contact.Last
    sms_successful.Address = contact.Address
    sms_successful.City = contact.City
    sms_successful.State = contact.State
    sms_successful.Zip = contact.Zip
    sms_successful.PropertyID = contact.PropertyID
    sms_successful.UploadDate = timestamp
    sms_successful.SMSMessage1 = contact.SMSMessage1
    sms_successful.save()
    contact.delete()
    print('Contact Deleted')


def send_contact_to_caller_list(contact_uuid, connection, campaign_uuid, contact_list_id, contact, timestamp):
    queryset = SMS_Queued.objects.all()
    # q = queryset.filter(campaign=campaign_uuid, cl_uuid=contact_uuid)
    # q = q[0]
    print(contact)
    body = [{
        "id": "",
        "contact_list_id": contact_list_id, 
        'data': {
            'Number': contact.Number,
            'Type': contact.Type,
            'Timezone': contact.Timezone,
            'First': contact.First,
            'Last': contact.Last,
            'Address': contact.Address,
            'City': contact.City,
            'State': contact.State,
            'Zip': contact.Zip,
            'PropertyID': contact.PropertyID,
            'UploadDate': datetime.datetime.utcnow().isoformat()[:18]+"Z"
        }
    }]
    
    send_called_db(contact, timestamp)
    try:
        if contact_list_id:
            log_data(f"Sending To Caller List- {body}", "Caller_List_Send")
            api_instance = PureCloudPlatformClientV2.OutboundApi(connection)
            api_response = api_instance.post_outbound_contactlist_contacts('88d6cd5f-28cb-42a4-9725-ea39c06892a5', body)
        return 1
    except:
        log_data(f'Failed To Send To Caller List - {body}', 'Caller_List_Send')
        return 0


def update_data(contact_uuid, status, q, response, timestamp, contact_list_id, connection, campaign_uuid, retainQueued):
    # try:
    contact = q
    queryset = SMS_Queued.objects.all()
    q = queryset.filter(campaign=campaign_uuid, cl_uuid=contact_uuid)
    print('QUERY', q)
    print('RESPONSE', response)
    if response == 0:
            # if contact_list_id:
            print('Prosessing failed record: contact_uuid')
            send_contact_to_caller_list(contact_uuid, connection, campaign_uuid, contact_list_id, contact, timestamp)
    print('Sending successful - ')
    print(q)
    if contact:
        print('Sending successful - ')

        if retainQueued:
            pass

        elif status == 1:
            send_successful_db(contact_uuid, contact, timestamp)
        return 1
        # except:
        #     pass
    # elif len(contact) > 1:
    #     for i in contact[1:]:
    #         i.delete()
    #     contact = contact[0]

    #     if retainQueued:
    #         pass

    #     elif status == 1:
    #         send_successful_db(contact_uuid, q)
    #     return 1


def cleanup(campaign_uuid):

    from . import models    

    # queryset = models.SMS_Successful.objects.all()
    queryset = models.SMS_Queued.objects.all()
    # queryset3 = models.Sent_Call_List.objects.all()

    q_list = []
    content = ''
    with open('cl_uuid.txt', 'r') as f:
        content = f.readlines()
    for c in content:
        q_list.append(c.replace('\n', ''))

    for count, query in enumerate(q_list):
        q = queryset.filter(campaign=campaign_uuid, cl_uuid=query)
   
        if len(q) > 1:
            for count, i in enumerate(q):
    
                if len(q) > 1:
                    log_data(i, 'deleted')
                    i.delete()


def downloadData(zillow_list_id, connection, campaign_uuid):
    log_data('Starting Run', 'SMS_RUN_APP')
    uri = grab_lead_data(connection, zillow_list_id)
    if uri:
        data = download_data(uri)
        # print(list(data.itterrows()))
        for count, (index, row) in enumerate(data.iterrows()):
            if count % 1000 == 0:
                print(f"{len(data)}\\{count}")
            # print(type(data.itterrows()))
            contact_uuid = save_data(row, count, campaign_uuid)
            #print(type(data))
            #print(dir(data))
            if contact_uuid:
                pass
                #delete_contact_from_purecloud_list(os.environ.get['Tricon_Zillow_Contact_ID'], contact_uuid)


def sendTexts(campaign_uuid, contact_list_id, startTime, endTime, connection, number):
    queued = query(campaign_uuid)
    # print(queued)
    for count, q in enumerate(queued):
        print('QQQQQ', q)
        log_data(f"Processing: Queued {len(queued)-1}\\{count}", "Queued")
        time.sleep(.05)
        if checking_timezonez_in_range(startTime, endTime, q.Timezone):
            q.in_range = True
            print('In range')
            queued_val = queued.values()
            parsed_Data = parse_data(q.__dict__)
            composed_message = compose_sms(parsed_Data, number)

            response = ''
            status = ''
            # if count > 800:
            for message in composed_message:
                
                response, timestamp = agentless_sms(connection, message)
                time.sleep(2)
                if response:
                    status = check_status_of_sent_sms(connection, response)
                    log_data(f"Checking SMS Status: UUID: {q.cl_uuid} - Status: {status} = Response: {response} = Timestamp: {timestamp}", 'SMS_RUN_APP')
            contact_uuid = update_data(contact_uuid=q.cl_uuid, status=status, response=response, timestamp=timestamp, contact_list_id=contact_list_id, connection=connection, campaign_uuid=campaign_uuid, q=q, retainQueued=0)
        else:
            print('Not in range')
            contact_uuid = update_data(contact_uuid=q.cl_uuid, q=q, contact_list_id=contact_list_id, campaign_uuid=campaign_uuid, status=0, response=0, timestamp=0, connection=connection, retainQueued=1)


class run():

    def __init__(self, event):
        print(event.job_id)
        campaign_uuid = event.job_id
        #try:
        campaign_model = Campaign.objects.filter(send_texts_scheduler_uuid=campaign_uuid).values()[0]
    

        self.campaign_model = campaign_model
        if campaign_model['Call_List_ID']:
            self.Call_List_ID = campaign_model['Call_List_ID']
        else:
            self.Call_List_ID = 0
        self.zillow_list_id = campaign_model['zillow_list_id']
        self.startTime = campaign_model['start']
        self.endTime = campaign_model['end']
        self.number = campaign_model['number']
        try:
            connection = connect_to_purecloud(campaign_model['purecloud_client_id'], campaign_model['purecloud_client_secret'])
        except Exception as e:
            log_data(f"Connection | Operational Error: {e}", 'SMS_RUN_APP')
        try:
            downloadData(self.zillow_list_id, connection, campaign_model['uuid'])
        except Exception as e:
            log_data(f"Data Pull | Operational Failure: {e}", 'SMS_RUN_APP')
        try:
            sendTexts(campaign_model['uuid'], self.Call_List_ID, self.startTime, self.endTime, connection, self.number)
        except Exception as e:
           log_data(f"Text Send | Operational Failure: {e}", 'SMS_RUN_APP')