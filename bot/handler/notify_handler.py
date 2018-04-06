from bot.handler.base import BaseMessageHandler
from datetime import datetime
import functools
import re


class NotifyHandler(BaseMessageHandler):
    def __init__(self, transport, loop, settings=None):
        super(NotifyHandler, self).__init__(transport, loop, settings)

    def handle(self, message):
        super(NotifyHandler, self).handle(message)
        if message.command == 'PRIVMSG':
            channel = message.channel
            content = message.text
            nick = message.nick
            if content.find('일 추가:') == 0:
                content = content[len('일 추가:'):].strip()
                if not content:
                    return
                when_regex = re.compile('\((\d+)/(\d+)(?: (\d+)(?::(\d+)))?\)$')
                time_part = when_regex.search(content)
                if time_part:
                    print(content)
                    task_name = when_regex.sub('', content).strip()
                    month, date, hour, minute = time_part.groups()
                    month, date, hour, minute = int(month), int(date), 13 if hour is None else int(hour), 0 if minute is None else int(minute)
                    year = datetime.now().year
                    t = datetime(year, month, date, hour, minute)
                    delta = (t - datetime.now()).total_seconds()
                    print(task_name)
                    self.loop.call_later(delta, functools.partial(self.send_message, channel, '{nick}: [일] {task_name}'.format(nick=nick, task_name=task_name)))
                else:
                    self.send_message(channel, '올바른 포맷이 아닙니다. "일 추가: [제목] (월/일 시:분)"')


export_handler = NotifyHandler
