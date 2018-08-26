import requests, json, time

# Authorization
payload = {'username': '', 'appKey': '', 'secret': '', 'accessToken': '', 'accessTokenSecret': ''}
headers = {'Content-Type': 'application/json'}
login_url = 'https://lo.agentvep.liveperson.net/api/account/91200013/login??v=1&NC=true'
r = requests.post(login_url, headers=headers, data=json.dumps(payload))
parsed_json = json.loads(r.content)
bearer = parsed_json['bearer']
print "Auth bearer: ", bearer

# Start Agent Session
create_agent_session_url = 'https://lo.agentvep.liveperson.net/api/account/91200013/agentSession?v=1&NC=true'
headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': 'Bearer ' + bearer}
payload = {'loginData': ''}
r = requests.post(create_agent_session_url, headers=headers, data=json.dumps(payload))
parsed_json = json.loads(r.content)
agent_session_id = parsed_json['agentSessionLocation']['link']['@href'].rsplit('/', 1)[-1]
print "Agent Session ID: ", agent_session_id

# Take chat
while True:
    time.sleep(1)
    take_chat_url = 'https://lo.agentvep.liveperson.net/api/account/91200013/agentSession/'+agent_session_id+'/incomingRequests?v=1&NC=true'
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': 'Bearer ' + bearer}
    payload = {'': ''}
    r = requests.post(take_chat_url, headers=headers, data=json.dumps(payload))
    parsed_json = json.loads(r.content)
    try:
        chat_id = parsed_json['chatLocation']['link']['@href'].rsplit('/', 1)[-1]
        print "Chat ID: ", chat_id
        break
    except:
        print "No incoming chat session.."

def sendLine():
    send_line_url = 'https://lo.agentvep.liveperson.net/api/account/91200013/agentSession/'+agent_session_id+'/chat/'+chat_id+'/events?v=1&NC=true'
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': 'Bearer ' + bearer}
    payload = json.dumps({
        "event": {
            "@type": "line",
            "text": "<div dir='ltr' style='direction: ltr; text-align: left;'>Welcome to Chatterbot!</div>",
            "textType": "html"
        }
    })
    r = requests.post(send_line_url, headers=headers, data=payload)
    
sendLine()
    
# Retrieve Chat Events
init_id = 3
while True:
    take_chat_url = 'https://lo.agentvep.liveperson.net/api/account/91200013/agentSession/'+agent_session_id+'/chat/'+chat_id+'/events?v=1&NC=true'
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': 'Bearer ' + bearer}
    payload = {'': ''}
    r = requests.get(take_chat_url, headers=headers, data=json.dumps(payload))
    parsed_json = json.loads(r.content)
    #try:
    current_id = int(parsed_json['events']['event'][-1]['@id'])
    if init_id <> current_id:
        print "Text: " + parsed_json['events']['event'][-1]['text']
        init_id = init_id + 1
    #except:
       # pass
    