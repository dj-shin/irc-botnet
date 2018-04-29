from bot.handler.base import BaseMessageHandler
from datetime import datetime, timedelta
import functools
import re
import asyncio


class ReminderHandler(BaseMessageHandler):
    def __init__(self, transport, loop, settings=None):
        super(ReminderHandler, self).__init__(transport, loop, settings)
        self.set_reminder('12:00', '마로링: 점심 출석!', ['#maronet'])
        self.set_reminder('18:00', '마로링: 저녁 출석!', ['#maronet'])

    def set_reminder(self, time, message, channels, period=60*60*24):
        now = datetime.now()
        hour, minute = list(map(lambda x: int(x), time.split(':')))
        t = datetime(now.year, now.month, now.day, hour, minute)
        if t < datetime.now():
            t += timedelta(days=1)
        delta = (t - datetime.now()).total_seconds()

        def reminder(self, channels, message):
            for channel in channels:
                self.send_message(channel, message)
            self.loop.call_later(period, functools.partial(reminder, self, channels, message))

        print('Scheduled at : {} sec later'.format(delta))
        self.loop.call_later(delta, functools.partial(reminder, self, channels, message))


export_handler = ReminderHandler
