import sys, json, requests
from flask import Flask, request
#import pyowm

'''try:
    import apiai
except ImportError:
    sys.path.append(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
    import apiai
'''
app = Flask(__name__)

PAT = 'EAAWULE9GScoBAAXEwWzIMP3Ldltm6qgUg0d576hJR6gOuPPdJKemmMdJ89yDcYl3GfINpRprFZCykERV5gZBrvZA5dXUDhvjIruoXXFxnjcDYZCW02utAES5FTaEuu6TsUwZAOlYDO4m8KaJ4uFzREBIQlrVYPLZAiMxxVSkNBkQZDZD'

CLIENT_ACCESS_TOKEN = 'your_api_access_key'

VERIFY_TOKEN = 'your_webhook_verification_token'

#ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

@app.route('/', methods=['GET'])
def handle_verification():
    '''
    Verifies facebook webhook subscription
    Successful when verify_token is same as token sent by facebook app
    '''
    if (request.args.get('hub.verify_token', '') == VERIFY_TOKEN):     
        print("succefully verified")
        return request.args.get('hub.challenge', ''), 403
    else:
        print("Wrong verification token!")
        return "Wrong validation token", 200


@app.route('/', methods=['POST'])
def handle_message():
    '''
    Handle messages sent by facebook messenger to the applicaiton
    '''
    data = request.get_json()

    if data["object"] == "page":
        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:
                if messaging_event.get("message"):  

                    sender_id = messaging_event["sender"]["id"]        
                    recipient_id = messaging_event["recipient"]["id"]  
                    message_text = messaging_event["message"]["text"]  
                    send_message_response(sender_id, parse_user_message(message_text)) 

    return "ok", 80


def send_message(sender_id, message_text):
    '''
    Sending response back to the user using facebook graph API
    '''
    r = requests.post("https://graph.facebook.com/v2.6/me/messages",

        params={"access_token": PAT},

        headers={"Content-Type": "application/json"}, 

        data=json.dumps({
        "recipient": {"id": sender_id},
        "message": {"text": message_text}
    }))


def parse_user_message(user_text):
    '''
    Send the message to API AI which invokes an intent
    and sends the response accordingly
    The bot response is appened with weaher data fetched from
    open weather map client
    '''

    print ("it's working")


def send_message_response(sender_id, message_text):

    sentenceDelimiter = ". "
    messages = message_text.split(sentenceDelimiter)
    
    for message in messages:
        send_message(sender_id, message)

if __name__ == '__main__':
    app.run()   
