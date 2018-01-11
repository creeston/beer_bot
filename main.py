import os
import tornado.httpserver
# -*- coding: utf-8 -*- 

import tornado.ioloop
import tornado.web
import tornado.escape
import requests
import datetime
from repository import EventRepository


URL = "https://api.telegram.org/bot%s/" % os.environ['BOT_TOKEN']
MyURL = "https://vast-depths-79763.herokuapp.com/hook"
api = requests.Session()

def send_reply(response):
    if 'text' in response:
        api.post(URL + "sendMessage", data=response)


def not_found(arguments, message):
    response = {'chat_id': message['chat']['id']}
    response['text'] = "Command not found"
    return response

def help_message(arguments, message):
    response = {'chat_id': message['chat']['id']}
    result = ["Hey, %s!" % message["from"].get("first_name"),
              "\rI can accept only these commands:"]
    for command in CMD:
        result.append(command)
    response['text'] = "\n\t".join(result)
    return response

def create_beer_message(arguments, message):
    print("arguments")
    print(arguments)
    response = {'chat_id': message['chat']['id']}
    try:
        with EventRepository() as rep:
            if len(arguments) != 3:
                response['text'] = 'USAGE: /create [place(without spaces)] d.m H:M'
            else:
                date = datetime.datetime.strptime("%s %s" % (arguments[1], arguments[2]), "%d.%m %H:%M")
                date = date.replace(year = datetime.datetime.now().year)
                rep.create("Beer", arguments[0], date, message['chat']['id'])
                response['text'] = 'Beer created successfully'
    except Exception as e:
        response['text'] = str(e)
    return response

def when_beer_message(arguments, message):
    response = {'chat_id': message['chat']['id']}
    try:
        with EventRepository() as rep:
            events = rep.list(message['chat']['id'])
            if not events:
                response['text'] = u'Нет пива в ближайшее время'
            else:
                event = events[0]
                response['text'] = u'Пиво будет в %s %s' % (event.place, str(event.date))
    except Exception as e:
        response['text'] = str(e)
        return response
    return response


CMD = {"/help": help_message, '/create': create_beer_message, '/when': when_beer_message}
 
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello world")


class HookHandler(tornado.web.RequestHandler):
    def post(self):
        try:
            print("Got request: %s" % self.request.body)
            update = tornado.escape.json_decode(self.request.body)
            message = update['message']
            text = message.get('text')
            if text:
                print("MESSAGE\t%s\t%s" % (message['chat']['id'], text))
                if text[0] == '/':
                    command, *arguments = text.split(" ")
                    response = CMD.get(command, not_found)(arguments, message)
                    print("REPLY\t%s\t%s" % (message['chat']['id'], response))
                    send_reply(response)
        except Exception as e:
            print(str(e))

 
def main():
    application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/hook", HookHandler)
    ])
    set_hook = api.get(URL + "setWebhook?url=%s" % MyURL)
    if set_hook.status_code != 200:
        print("Can't set webhook: %s. Quit" % set_hook.text)
        exit(1)
    http_server = tornado.httpserver.HTTPServer(application)
    port = int(os.environ.get("PORT", 5000))
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()
 
if __name__ == "__main__":
    main()