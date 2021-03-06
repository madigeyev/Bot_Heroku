# https://proglib.io/p/telegram-bot/

"""
Параметры бота
"""

token = "762529566:AAHAV4CmL_ffjPCmisPWLNV16UTZpQfu9BU"

"""
Конец определения параметров.
"""

import requests  
import datetime
 
class BotHandler:
 
    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)
 
    def get_updates(self, offset=None, timeout=30):
        method = 'getUpdates'
        if offset != None:
            params = {'timeout': timeout, 'offset': offset}
        else:
            params = {'timeout': timeout}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json
 
    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp
 
    def get_last_update(self, offset=None):
        get_result = self.get_updates(offset)
#        if len(get_result) > 0:
#            last_update = get_result[len(get_result)-1]
#        else:
#            last_update = get_result[-1]
        last_update = get_result[-1]
        return last_update

		
greet_bot = BotHandler(token)  
greetings = ('hello', 'hi', 'greetings', 'sup')  
now = datetime.datetime.now()
 
 
def main():  
    new_offset = None
    today = now.day
    hour = now.hour
 
    while True:
        greet_bot.get_updates(new_offset)
 
        last_update = greet_bot.get_last_update()
 
        last_update_id = last_update['update_id']
        last_chat_text = last_update['message']['text']
        last_chat_id = last_update['message']['chat']['id']
        last_chat_name = last_update['message']['chat']['first_name']
        msg = last_chat_text.lower()

        if msg in greetings:
            if today == now.day :    
                today += 1
                if 6 <= hour < 12:
                    greet_bot.send_message(last_chat_id, 'Good Morning  {}'.format(last_chat_name))
                elif 12 <= hour < 17:
                    greet_bot.send_message(last_chat_id, 'Good Afternoon {}'.format(last_chat_name))
                elif 17 <= hour < 23:
                    greet_bot.send_message(last_chat_id, 'Good Evening  {}'.format(last_chat_name))
        elif len(msg)>0:
            greet_bot.send_message(last_chat_id, 'Sorry. I don\'t understand: {}'.format(msg))
 
        new_offset = last_update_id + 1
 
if __name__ == '__main__':  
    try:
        main()
    except KeyboardInterrupt:
        exit()
