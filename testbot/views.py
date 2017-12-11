import json
import requests

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

like_sticker_id = [369239263222822, 369239343222814, 369239383222810]
reply_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'
VERIFY_TOKEN = 'EAAERYE7SxhIBAE5iZCmnjymZAdFWQBDzN7QheEIo60pLL5siSTHZBatFLjfb8ODdVftd7Q5hZBygAohSTNJvte7RfumjOmMOz6xZBrNVzn3OatQ8Y1c2ZBPliJ0rRBsYaBNf6ZA8nIPHZBomRVGAQjAkoAaQZAWrFb9G1B1GPEYaeuQZDZD'


@csrf_exempt
def bot_test(request):
    """ Bot """

    # print ("get", request.GET)
    if request.method == 'GET':
        print("hai GET")
        verify_token = request.GET.get('hub.verify_token')
        hub_challenge = request.GET.get('hub.challenge')
        # print("verify token", verify_token)
        # print("hub challenge", hub_challenge)
        if verify_token == VERIFY_TOKEN:
            return HttpResponse(hub_challenge)
        else:
            return HttpResponse('Invalid Token')

    if request.method == 'POST':
        # print ("post", request.POST)
        if request.body:
            incoming_message = json.loads(request.body.decode('utf-8'))
            sender = incoming_message['entry'][0]['messaging'][0]['sender']['id']
            try:
                msg_text = incoming_message['entry'][0]['messaging'][0]['message']['text']
                print("message from user: ", msg_text)
                # joke_text = requests.get("http://api.icndb.com/jokes/random/").json()['value']['joke']
                user_details_url = "https://graph.facebook.com/v2.6/%s" % sender
                user_details_params = {'fields': 'first_name,last_name,profile_pic', 'access_token': VERIFY_TOKEN}
                user_details = requests.get(user_details_url, user_details_params).json()
                print("User :", user_details['first_name'])
                if 'hello' in msg_text:
                    msg_text = "Hai " + user_details['first_name'].title()+"\nHow can I help you ?"
                headers = {
                    'Content-Type': 'application/json',
                }
                data = {
                    "recipient": {
                        "id": sender
                    },
                    "message": {
                        "text": msg_text
                    }
                }
                json_data = json.dumps(data)
                if msg_text:
                    print("body", request.body)
                    requests.post(reply_url %( VERIFY_TOKEN), headers=headers, data=json_data)
                    return HttpResponse(True)

            except KeyError:
                pass

            try:
                # print(request.body)
                msg_emoji = incoming_message['entry'][0]['messaging'][0]['message']['sticker_id']
                print("sicker_id", msg_emoji)
                if msg_emoji in like_sticker_id:
                    msg_emoji = 'Like'
                print(msg_emoji)
                headers = {
                            'Content-Type': 'application/json',
                        }
                data = {
                        "recipient": {
                            "id": sender
                        },
                        "message": {
                            "text": msg_emoji
                            }
                        }
                json_data = json.dumps(data)
                requests.post(reply_url %( VERIFY_TOKEN), headers=headers, data=json_data)
                return HttpResponse(True)
            except KeyError:
                pass

    return HttpResponse(True)