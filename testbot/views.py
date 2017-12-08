import json
import requests

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def bot_test(request):
    """ Bot """

    # print ("get", request.GET)
    VERIFY_TOKEN = 'EAAERYE7SxhIBAFqmNS0pQnJ5zreZBtR1xRH7PEzaStiNFHCtcC28oymKh4u3p4q3Xq4em6v8HI8k4x4C5ijUW3tXYZABUEd17LIEF1eNmftnvVxDJhhoHVeIscgyyWM22Fb4WTxoYmwnPD2YaNUzNXeTfiURWm2F9SsV6ZCIAZDZD'
    post_reply_url = 'https://graph.facebook.com/v2.6/%s/?access_token=%s'
    reply_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'
    if request.method == 'GET':
        verify_token = request.GET.get('hub.verify_token')
        print(verify_token)
        hub_challenge = request.GET.get('hub.challenge')
        if verify_token == VERIFY_TOKEN:
            return HttpResponse(hub_challenge)
        else:
            return HttpResponse('Invalid Token')

    if request.method == 'POST':
        print("body", request.body)
        # print ("post", request.POST)
        if request.body:
            incoming_message = json.loads(request.body.decode('utf-8'))
            try:
                msg_text = incoming_message['entry'][0]['messaging'][0]['message']['text']
                print("message from user: ", msg_text)
            except KeyError:
                msg_text = ''
            sender = incoming_message['entry'][0]['messaging'][0]['sender']['id']
            joke_text = requests.get("http://api.icndb.com/jokes/random/").json()['value']['joke']
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
                r = requests.post(reply_url %( VERIFY_TOKEN), headers=headers, data=json_data)
                print(r.json())
            return HttpResponse(True)
    # return HttpResponse(True)