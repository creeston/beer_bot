import os
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.escape
import requests

URL = "https://api.telegram.org/bot%s/" % os.environ['BOT_TOKEN']
MyURL = "https://vast-depths-79763.herokuapp.com/hook"
api = requests.Session()

def send_reply(response):
    if 'text' in response:
        api.post(URL + "sendMessage", data=response)

CMD = {"/help": help_message}

def not_found(arguments, message):
    response = {'chat_id': message['chat']['id']}
    response['text'] = "Command not found"

def help_message(arguments, message):
    response = {'chat_id': message['chat']['id']}
    result = ["Hey, %s!" % message["from"].get("first_name"),
              "\rI can accept only these commands:"]
    for command in CMD:
        result.append(command)
    response['text'] = "\n\t".join(result)
    return response
 
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
                    command, *arguments = text.split(" ", 1)
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