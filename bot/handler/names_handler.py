from bot.handler.base import BaseMessageHandler
import hashlib
from datetime import date, datetime


class NamesHandler(BaseMessageHandler):
    def __init__(self, transport, loop, settings=None):
        super(NamesHandler, self).__init__(transport, loop, settings)
        self.scan = False

    def handle(self, message):
        super(NamesHandler, self).handle(message)
        print(message)
        if message.command == 'PRIVMSG':
            channel = message.channel
            content = message.text
            if content.find('!스캔 ') == 0:
                self.scan = True
                target_channel = content[len('!스캔 '):]
                self.raw_send('NAMES {}'.format(target_channel))
        if message.command == '353' and self.scan:
            channel = message.channel
            content = message.text
            self.send_message(channel, 'Users in {} : {}'.format(channel, content))
            self.scan = False


export_handler = NamesHandler
