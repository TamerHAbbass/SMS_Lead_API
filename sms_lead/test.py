import io
import pandas
import PureCloudPlatformClientV2
import requests
import time




def connect_to_purecloud(client_id, client_secret):
    # log_data('Connecting to PureCloud', 'SMS_RUN_APP')
    # Set Purecloud region
    region = PureCloudPlatformClientV2.PureCloudRegionHosts.us_west_2

    # Get API Host for Purecloud region
    PureCloudPlatformClientV2.configuration.host = region.get_api_host()

    # Create API Client and get client credentials with client ID and key
    apiclient = PureCloudPlatformClientV2.api_client.ApiClient().get_client_credentials_token(client_id, client_secret)

    return apiclient


def grab_lead_data(apiclient, contact_list_id):

    # log_data('Grabbing Lead Data', 'SMS_RUN_APP')
    zillow_list_id = contact_list_id

    try:
        api_instance = PureCloudPlatformClientV2.OutboundApi(apiclient)
        api_instance.post_outbound_contactlist_export(zillow_list_id)
        time.sleep(60)

        # Grab Zillow_Master download URI
        exporturi = api_instance.get_outbound_contactlist_export(zillow_list_id).to_dict()

        # Grab CSV content by providing the download uri with authorization header
        req = requests.get(exporturi['uri'], headers={'authorization': f'Bearer {apiclient.access_token}'}).text
        # log_data('Lead Data Extraction Successful', 'SMS_RUN_APP')
        return req
    except:
        # log_data("Unable to download contactlist export.. please check Purecloud. Updating the ContactList UUID may be required", "SMS_RUN_APP")
        return 0


def download_data(req):
      zillow_json = pandas.read_csv(io.StringIO(req))
    #   with open('.\contact_pull.json', 'a+') as f:
    #       json.dump(zillow_json, f)
      return zillow_json




region = PureCloudPlatformClientV2.PureCloudRegionHosts.us_west_2
# Get API Host for Purecloud region
PureCloudPlatformClientV2.configuration.host = region.get_api_host()
# Create API Client and get client credentials with client ID and key
apiclient = PureCloudPlatformClientV2.api_client.ApiClient().get_client_credentials_token(client_id, secret_id)

api_instance = PureCloudPlatformClientV2.OutboundApi(apiclient)
# api_instance.post_outbound_contactlist_export(zillow_list_id)
# time.sleep(60)

# Grab Zillow_Master download URI
exporturi = api_instance.get_outbound_contactlist_export(zillow_list_id).to_dict()

# Grab CSV content by providing the download uri with authorization header
req = requests.get(exporturi['uri'], headers={'authorization': f'Bearer {apiclient.access_token}'}).text

# connection = connect_to_purecloud(secret_id, client_id)
# req = grab_lead_data(connection, zillow_list_id)
zillow_json = download_data(req)
print(zillow_json)
print(dir(zillow_json))
print(type(zillow_json))
zilist = zillow_json.values.tolist().pop()
print(zilist)
# for count, (index, row) in enumerate(zillow_json.iterrows()):
#     print(row)
