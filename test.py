import csv
import json
import os
import re
import pandas
import PureCloudPlatformClientV2
import requests


zillow_list_id = os.environ.get('Tricon_Zillow_Contact_ID')

zillow_contact_list_url = os.environ.get('Tricon_Contact_List_URI')

# Set Purecloud region
region = PureCloudPlatformClientV2.PureCloudRegionHosts.us_west_2

# Get API Host for Purecloud region
PureCloudPlatformClientV2.configuration.host = region.get_api_host()

apiclient = PureCloudPlatformClientV2.api_client.ApiClient().get_client_credentials_token(os.environ.get('Tricon_SMS_Client_ID'), os.environ.get('Tricon_SMS_Client_Secret'))
api_instance = PureCloudPlatformClientV2.ConversationsApi(apiclient)
body = PureCloudPlatformClientV2.SendAgentlessOutboundMessageRequest()

data = {
  "fromAddress": os.environ.get('Tricon_fromAddress'),
  "toAddress": os.environ.get('Tricon_toAddress'),
  "toAddressMessengerType": "sms",
  "textBody": "Hi, this is Tamer",
}

api_response = api_instance.post_conversations_messages_agentless(data)

# # Grab Zillow_Master download URI
# exporturi = api_instance.get_outbound_contactlist_export(zillow_list_id).to_dict()
# print(exporturi)
# # # Grab CSV content by providing the download uri with authorization header
# # req = requests.get(exporturi['uri'], headers={'authorization': f'Bearer {apiclient.access_token}'}).text

req = requests.post("https://api.usw2.pure.cloud/api/v2/conversations/messages/agentless", data, headers={'authorization': f'Bearer {apiclient.access_token}'})



# # # print()
# # rows = '{}'.format(req.replace('"','')).splitlines()
# # # print(rows)
# # contact_list = []
# # for x in rows:
# #     contact_list.append(x.split(','))



# # # zillow_data = [str(req.content).split('\n')]
# # # print(dir(zillow_data))



# # for x, contact in enumerate(contact_list[0]):
# #     print(contact)
# #     print(contact_list[1][x])
# #     print('\n')
    
# zillow_master = pandas.read_csv('documentation/Zillow_Master2.csv')
# zillow_json = zillow_master.to_dict()

# # def text_limit(smsmessagelist):
# #     if not len(smsmessagelist) < 1:
# #       complete_message = ' '.join(smsmessagelist)
# #     print(smsmessagelist)
# #     print(complete_message)
# #     return len(complete_message)

# # def compose_sms(zillow_json):
      
# #       sms = []

# #       for x, i in zillow_json.items():
# #           if re.findall(r'^smsmessage', x.lower()):
# #               sms.append(i[0])

# #       print(sms)
# #       print(text_limit(sms))
        
#     # if type.lower() == 'cell':
#     #       type = 'sms'

#     # data = {
#     #     "fromAddress": os.environ.get('Tricon_fromAddress'),
#     #     "toAddress": number,
#     #     "toAddressMessengerType": type,
#     #     "textBody": f"",
#     #   }

# # compose_sms(zillow_json)