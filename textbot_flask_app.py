# a simple flask bot that can understand ESS messages from the Syniverse Developer Community and
# check whether it is from the SCG, and sends an SMS reply if the incoming SMS contains a magic word
 
from flask import Flask
from flask import request, json
import requests
  
def send_reply_sms(mo_contents): # check if mo sms contains key word, and if so send back matching message
    channel_id = 'PUT_YOUR_CHANNELID_HERE'
    url = 'https://api.syniverse.com/scg-external-api/api/v1/messaging/message_requests'
    access_token = 'PUT_YOUR_ACCESS_TOKEN_HERE'
    headers = {'Authorization': 'Bearer ' + access_token, 'Content-Type': 'application/json'}
    key_words = {'Hello?': 'Hello back!', 'Yummy': 'Pie https://www.youtube.com/watch?v=qPlKVgSjCyU'}
    mo_message_body = mo_contents['fld-val-list']['message_body']
    if mo_message_body in key_words:
        mobile_number = [mo_contents['fld-val-list']['from_address']]
        payload = {'from': 'channel:' + channel_id, 'to': mobile_number, 'body': key_words[mo_message_body]}
        response = requests.post(url, json=payload, headers=headers)
        return 'sms response sent with status code '+str(response.status_code)
    else:
        return 'no sms sent, didnt say the magic word'
 
app = Flask(__name__)
 
@app.route('/simplebot/v1/notification', methods=['POST'])
def process_notification():
    if not request.json or not 'topic' in request.json: # filter out requests that arent likely to be an ESS notification
        return 'hello test', '201'
    elif request.json['topic'] == 'SCG-Message' and request.json['event']['evt-tp'] == 'mo_message_received': # check whether it is MO SMS
        event_data = request.json['event']
        result = send_reply_sms(event_data)
        return result, 201
    else:
        return 'hello not an SMS', 201
