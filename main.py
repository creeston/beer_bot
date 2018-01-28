import os
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.escape
import requests
import handlers
import inspect
# -*- coding: utf-8 -*- 


URL = "https://api.telegram.org/bot%s/" % os.environ['BOT_TOKEN']
MyURL = "https://vast-depths-79763.herokuapp.com/hook"
api = requests.Session()

def send_reply(response):
    if 'text' in response:
        api.post(URL + "sendMessage", data=response)


def process_response(handler_class, arguments, message):
    chat_id = message['chat']['id']
    response = {'chat_id': chat_id}
    try:
        handler = handler_class(arguments)
        response['text'] = handler.handle(chat_id)
    except Exception as e:
        response['text'] = str(e)
        return response
    return response


def build_handlers():
    cmd = {}
    for name, obj in inspect.getmembers(handlers):
        if inspect.isclass(obj) and hasattr(obj, 'command'):
            cmd["/%s" % obj.command] = obj
    return cmd


CMD = build_handlers()
 

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
                    сommand = command.split(u"@")[0]
                    command = command.split("@")[0]
                    handler = CMD.get(command, handlers.UnknownCommandHandler)
                    response = process_response(handler, arguments, message)
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