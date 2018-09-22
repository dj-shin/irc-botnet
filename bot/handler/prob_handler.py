from bot.handler.base import BaseMessageHandler
import hashlib
from datetime import date, datetime


class ProbHandler(BaseMessageHandler):
    def __init__(self, transport, loop, settings=None):
        super(ProbHandler, self).__init__(transport, loop, settings)

    def handle(self, message):
        super(ProbHandler, self).handle(message)
        print(message)
        if message.command == 'PRIVMSG':
            channel = message.channel
            content = message.text
            if content.find('!확률 ') == 0:
                content = content[len('!확률 '):]
                if not content:
                    return
                m = hashlib.md5()
                m.update(content.encode())
                m.update(datetime.now().strftime("%Y%m%d").encode())
                prob = int(m.hexdigest(), 16) % 10000
                self.send_message(channel, content + ' = ' + str(prob / 100.0) + '%')


export_handler = ProbHandler
