from bot.connector import IRCProtocol
import bot.handler.notify_handler as handler
import asyncio
import signal
import functools


def signal_handler(protocols, loop):
    print('\r[+] Input command')
    action = input('>>> ').strip().split(' ')
    if action[0] == 'reload':
        for protocol in protocols:
            protocol.reload_handler()
    elif action[0] == 'quit':
        loop.stop()
    elif action[0] == 'invite':
        for protocol in protocols:
            protocol.handler.join_channel(action[1], action[2])


class IRCSetting:
    def __init__(self, botname, botnick):
        self.botname = botname
        self.botnick = botnick
        self.initial_commands = [
            'USER ' + (botname + ' ') * 3 + ':' + botnick + '\n',
            'NICK ' + botnick + '\n',
            'JOIN ' + '#maronet' + '\n',
        ]

if __name__ == '__main__':
    host = 'moe.uriirc.org'
    port = '16667'
    loop = asyncio.get_event_loop()
    protocol = IRCProtocol(loop, IRCSetting('notify-bot', 'notify-bot'), handler)
    conn = loop.create_connection(
        lambda: protocol,
        host=host,
        port=port)
    loop.add_signal_handler(signal.SIGINT, functools.partial(signal_handler, [protocol], loop))
    loop.run_until_complete(conn)
    loop.run_forever()
