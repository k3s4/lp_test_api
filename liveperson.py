import requests, json, time
from websocket import create_connection

url = 'https://lo.idp.liveperson.net/api/account/91200013/signup'
r = requests.post(url)
parsed_json = json.loads(r.content)
jwt = parsed_json['jwt']

ws = create_connection("wss://lo.msg.liveperson.net/ws_api/account/91200013/messaging/consumer?v=3")
authentication = "{\"kind\":\"req\",\"id\":\"0\",\"type\":\"InitConnection\",\"headers\":[{\"type\":\".ams.headers.ClientProperties\",\"deviceFamily\":\"MOBILE\",\"os\":\"ANDROID\"},{\"type\":\".ams.headers.ConsumerAuthentication\",\"jwt\":\""+jwt+"\"}]}"
ConsumerRequestConversation = "{\"kind\":\"req\",\"id\":1,\"type\":\"cm.ConsumerRequestConversation\"}"
ws.send(authentication)
result = ws.recv()
print("Received '%s'" % result)
ws.send(ConsumerRequestConversation)
result = ws.recv()
print("Received '%s'" % result)
parsed_json = json.loads(result)
conversationId = parsed_json['body']['conversationId']
SubscribeMessagingEvents = "{\"kind\":\"req\",\"id\":\"22\",\"body\":{\"fromSeq\":0,\"dialogId\":\""+conversationId+"\"},\"type\":\"ms.SubscribeMessagingEvents\"}"
ws.send(SubscribeMessagingEvents)

while True:
    result = ws.recv()
    parsed_json = json.loads(result)
    try:
        if 'message' in parsed_json['body']['changes'][0]['event']:
            print parsed_json['body']['changes'][0]['event']['message']
    except:
        pass 